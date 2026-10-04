#!/usr/bin/env python3
"""Coletor via API do Apify. Lê APIFY_TOKEN do ambiente ou do .env da raiz do repo.

    py scripts/coletores/apify.py <ator> <nome> '<json de entrada>'
    py scripts/coletores/apify.py apify~instagram-scraper ig-perfil-posts "{\"directUrls\":[\"https://www.instagram.com/HANDLE/\"],\"resultsType\":\"posts\",\"resultsLimit\":60}"

No PowerShell 5.1 as aspas internas do JSON precisam de barra (\"), como acima.
Alternativa mais limpa: salvar a entrada num arquivo e passar @caminho.json:

    py scripts/coletores/apify.py apify~instagram-scraper ig-perfil-posts @pesquisa/coleta/entrada.json

Roda o ator, espera terminar, salva os itens do dataset em
pesquisa/coleta/raw/<nome>.json e imprime custo (USD) e nº de itens.
Origem nos relatórios: `observado (Apify <ator>, data)`.

Apify cobra por execução. Volume pequeno, um alvo por chamada — ver
scripts/coletores/README.md.
"""
import io, json, os, re, sys, time, urllib.error, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(RAIZ, "pesquisa", "coleta", "raw")

USO = ("uso: py scripts/coletores/apify.py <ator> <nome> '<json de entrada>' | @arquivo.json\n"
       "ex.: py scripts/coletores/apify.py apify~instagram-scraper ig-perfil-posts @entrada.json")


def token():
    t = os.environ.get("APIFY_TOKEN", "").strip()
    if t:
        return t
    p = os.path.join(RAIZ, ".env")
    if os.path.exists(p):
        env = io.open(p, encoding="utf-8-sig").read()
        m = re.search(r"^APIFY_TOKEN=(.+)$", env, re.M)
        if m and m.group(1).strip().strip('"').strip("'"):
            return m.group(1).strip().strip('"').strip("'")
    raise SystemExit("APIFY_TOKEN não encontrado. Pôr no .env da raiz (ver .env.exemplo) "
                     "ou na variável de ambiente. A chave fica em console.apify.com > "
                     "Settings > API & Integrations.")


def _req(path, body=None, method=None):
    url = "https://api.apify.com" + path + ("&" if "?" in path else "?") + "token=" + token()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")[:400]
        raise SystemExit(f"Apify devolveu HTTP {e.code} em {path.split('?')[0]}: {corpo}")


def run(ator, nome, entrada, timeout_s=900, memoria_mb=None):
    os.makedirs(RAW, exist_ok=True)
    q = f"?memory={memoria_mb}" if memoria_mb else ""
    r = _req(f"/v2/acts/{ator}/runs{q}", entrada)["data"]
    rid, ds = r["id"], r["defaultDatasetId"]
    t0 = time.time(); status = r["status"]
    while status in ("READY", "RUNNING"):
        if time.time() - t0 > timeout_s:
            _req(f"/v2/actor-runs/{rid}/abort", {}, "POST"); status = "TIMEOUT"; break
        time.sleep(8)
        r = _req(f"/v2/actor-runs/{rid}")["data"]; status = r["status"]
    itens = _req(f"/v2/datasets/{ds}/items?clean=true&format=json")
    dest = os.path.join(RAW, nome + ".json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump({"ator": ator, "entrada": entrada, "run": rid, "status": status,
                   "custo_usd": r.get("usageTotalUsd"), "coletado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "origem": "observado", "itens": itens}, f, ensure_ascii=False, indent=1)
    print(f"[{nome}] {ator} status={status} itens={len(itens)} custo=US$ {r.get('usageTotalUsd')} -> {os.path.relpath(dest, RAIZ)}")
    return itens


def ler_entrada(arg):
    if arg.startswith("@"):
        with io.open(arg[1:], encoding="utf-8-sig") as f:
            return json.load(f)
    return json.loads(arg)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(USO)
    token()  # falha cedo, antes de qualquer chamada, se a chave não existir
    ator, nome = sys.argv[1], sys.argv[2]
    if not re.fullmatch(r"[A-Za-z0-9._-]+", nome):
        raise SystemExit(f"nome inválido: {nome!r}. Usar só letra, número, ponto, hífen e _ (vira nome de arquivo).")
    try:
        entrada = ler_entrada(sys.argv[3])
    except (json.JSONDecodeError, OSError) as e:
        raise SystemExit(f"entrada inválida ({e}). No PowerShell, preferir @arquivo.json.")
    run(ator, nome, entrada)
