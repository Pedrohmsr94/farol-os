"""
Perfil de desempenho do Instagram — o placar da própria conta.

Puxa os últimos posts pela Graph API (dado real: alcance, salvamento,
compartilhamento, interações por post), separa por formato, lê os 25% melhores
e os 25% piores e escreve o padrão. É o placar que o /revisar, o /semana e o
/relatorio consultam — formato e abertura que entregam NESSA conta.

Uso:
    py scripts/perfil-de-desempenho.py [--posts 40] [--excluir ID,ID,...]
                                      [--env caminho/.env]

Lê META_ACCESS_TOKEN e META_IG_ACCOUNT_ID da variável de ambiente ou do .env da
raiz (ou do arquivo passado em --env). Ambiente vence arquivo. Aceita também os
nomes do /aprovar-post (META_PAGE_ACCESS_TOKEN, META_IG_USER_ID) — é a mesma conta.
O token precisa das permissões instagram_basic e instagram_manage_insights.
Só leitura: o script não publica nem altera nada.

Saída (em pesquisa/investigacoes/desempenho/):
    perfil-<AAAA-MM-DD>.md     leitura datada, fica como histórico
    perfil-<AAAA-MM-DD>.json   os números crus
    perfil-de-desempenho.md    cópia do mais recente — é este que o /revisar lê

Limites que o relatório declara:
  - alcance de post impulsionado inclui o pago. A Graph API não separa por
    post; passar os IDs em --excluir (os impulsionamentos estão no Gerenciador
    de Anúncios). Sem isso, o número do reel impulsionado sobe e o do formato
    junto.
  - métrica que a API não devolve pra um post fica como "-" e não entra na
    mediana. Nunca é preenchida com estimativa.
"""

import argparse
import json
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

VERSAO = "v21.0"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "pesquisa", "investigacoes", "desempenho")

# Conjuntos de métricas por formato, do mais completo pro mínimo. A API muda de
# versão em versão (plays virou views, impressions saiu); tenta o primeiro que
# ela aceitar.
METRICAS = {
    "reel": [
        ["reach", "saved", "shares", "total_interactions", "views"],
        ["reach", "saved", "shares", "total_interactions", "plays"],
        ["reach", "saved", "shares"],
        ["reach", "saved"],
    ],
    "carrossel": [
        ["reach", "saved", "shares", "total_interactions"],
        ["reach", "saved", "shares"],
        ["reach", "saved"],
    ],
    "imagem": [
        ["reach", "saved", "shares", "total_interactions"],
        ["reach", "saved", "shares"],
        ["reach", "saved"],
    ],
}


def ler_env(caminho):
    env = {}
    if not os.path.exists(caminho):
        return env
    with open(caminho, encoding="utf-8-sig") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            k, v = linha.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def get(url, params):
    url = f"{url}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        try:
            corpo = json.load(e)
        except Exception:
            corpo = {"error": {"message": str(e)}}
        return None, corpo.get("error", corpo)


def formato_de(m):
    if m.get("media_product_type") == "REELS" or m.get("media_type") == "VIDEO":
        return "reel"
    if m.get("media_type") == "CAROUSEL_ALBUM":
        return "carrossel"
    return "imagem"


def listar_posts(ig_id, token, quantos):
    posts = []
    url = f"https://graph.facebook.com/{VERSAO}/{ig_id}/media"
    params = {
        "fields": "id,caption,media_type,media_product_type,timestamp,permalink,"
                  "like_count,comments_count",
        "limit": min(quantos, 50),
        "access_token": token,
    }
    while url and len(posts) < quantos:
        dados, erro = get(url, params)
        if erro:
            sys.exit(f"erro ao listar posts: {erro.get('message')}")
        posts += dados.get("data", [])
        prox = dados.get("paging", {}).get("next")
        url, params = (prox, {}) if prox else (None, None)
    return posts[:quantos]


def insights(media_id, formato, token):
    url = f"https://graph.facebook.com/{VERSAO}/{media_id}/insights"
    for conjunto in METRICAS[formato]:
        dados, erro = get(url, {"metric": ",".join(conjunto), "access_token": token})
        if not erro:
            out = {}
            for item in dados.get("data", []):
                valores = item.get("values") or [{}]
                out[item["name"]] = valores[0].get("value")
            return out
    return {}


def abertura(caption):
    if not caption:
        return "(sem legenda)"
    primeira = caption.strip().splitlines()[0].strip()
    return (primeira[:90] + "…") if len(primeira) > 90 else primeira


def tipo_abertura(caption):
    """Classificação grossa da primeira linha — quem lê o perfil refina."""
    p = abertura(caption).lower()
    if p == "(sem legenda)":
        return "sem legenda"
    if p.endswith("?"):
        return "pergunta"
    if re.search(r"\d", p):
        return "número"
    if re.match(r"^(quando|ontem|hoje|em 20\d\d|a família|meu|minha|fui|eu )", p):
        return "história"
    if re.search(r"\b(lei|norma|regra|resolução|decreto|portaria|prazo)\b", p):
        return "norma"
    return "afirmação"


def mediana(valores):
    v = [x for x in valores if isinstance(x, (int, float))]
    return int(statistics.median(v)) if v else None


def fmt(n):
    return "-" if n is None else f"{n:,}".replace(",", ".")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--posts", type=int, default=40)
    p.add_argument("--excluir", default="",
                   help="IDs de post impulsionado, separados por vírgula")
    p.add_argument("--env", help="arquivo .env com o token (padrão: .env da raiz)")
    args = p.parse_args()

    arquivo_env = args.env or os.path.join(RAIZ, ".env")
    if args.env and not os.path.exists(args.env):
        sys.exit(f"arquivo passado em --env não existe: {args.env}")
    env = ler_env(arquivo_env)
    env = {**env, **{k: v for k, v in os.environ.items() if k.startswith("META_") and v}}

    # META_ACCESS_TOKEN / META_IG_ACCOUNT_ID são os nomes do .env.exemplo. Os do
    # /aprovar-post (META_PAGE_ACCESS_TOKEN / META_IG_USER_ID) servem de reserva.
    token = env.get("META_ACCESS_TOKEN") or env.get("META_PAGE_ACCESS_TOKEN")
    ig_id = env.get("META_IG_ACCOUNT_ID") or env.get("META_IG_USER_ID")
    if not token or not ig_id:
        sys.exit("token e id da conta do Instagram não encontrados. Esperado "
                 "META_ACCESS_TOKEN e META_IG_ACCOUNT_ID na variável de ambiente ou em "
                 f"{arquivo_env} (ver .env.exemplo).")

    excluidos = {x.strip() for x in args.excluir.split(",") if x.strip()}

    print(f"listando até {args.posts} posts…", flush=True)
    brutos = listar_posts(ig_id, token, args.posts)
    print(f"{len(brutos)} posts. puxando insights…", flush=True)

    posts = []
    for m in brutos:
        formato = formato_de(m)
        ins = insights(m["id"], formato, token)
        posts.append({
            "id": m["id"],
            "data": m.get("timestamp", "")[:10],
            "formato": formato,
            "permalink": m.get("permalink"),
            "abertura": abertura(m.get("caption")),
            "tipo_abertura": tipo_abertura(m.get("caption")),
            "palavras_legenda": len((m.get("caption") or "").split()),
            "curtidas": m.get("like_count"),
            "comentarios": m.get("comments_count"),
            "alcance": ins.get("reach"),
            "salvamentos": ins.get("saved"),
            "compartilhamentos": ins.get("shares"),
            "interacoes": ins.get("total_interactions"),
            "views": ins.get("views", ins.get("plays")),
            "impulsionado": m["id"] in excluidos,
        })
        print(f"  {m.get('timestamp','')[:10]}  {formato:<9} alcance {fmt(ins.get('reach')):>6}  "
              f"salv {fmt(ins.get('saved')):>3}  comp {fmt(ins.get('shares')):>3}", flush=True)

    organicos = [x for x in posts if not x["impulsionado"] and x["alcance"] is not None]
    if len(organicos) < 4:
        sys.exit("menos de 4 posts com alcance — não dá pra ler padrão")

    por_alcance = sorted(organicos, key=lambda x: x["alcance"], reverse=True)
    corte = max(3, len(por_alcance) // 4)
    melhores, piores = por_alcance[:corte], por_alcance[-corte:]

    def resumo_formato(f):
        grupo = [x for x in organicos if x["formato"] == f]
        if not grupo:
            return None
        alc = [x["alcance"] for x in grupo]
        return {
            "n": len(grupo),
            "mediana_alcance": mediana(alc),
            "min_alcance": min(alc),
            "max_alcance": max(alc),
            "salvamentos": sum(x["salvamentos"] or 0 for x in grupo),
            "compartilhamentos": sum(x["compartilhamentos"] or 0 for x in grupo),
            "com_zero_salvamento": sum(1 for x in grupo if not x["salvamentos"]),
        }

    formatos = {f: resumo_formato(f) for f in ("reel", "carrossel", "imagem")}
    formatos = {f: r for f, r in formatos.items() if r}

    def contagem(lista, chave):
        c = {}
        for x in lista:
            c[x[chave]] = c.get(x[chave], 0) + 1
        return dict(sorted(c.items(), key=lambda kv: -kv[1]))

    hoje = date.today().isoformat()
    periodo = f"{organicos[-1]['data']} a {organicos[0]['data']}"
    zero_salv = sum(1 for x in organicos if not x["salvamentos"])

    perfil = {
        "gerado_em": hoje,
        "conta": ig_id,
        "posts_lidos": len(posts),
        "posts_organicos": len(organicos),
        "excluidos_impulsionados": sorted(excluidos),
        "periodo": periodo,
        "por_formato": formatos,
        "melhores": melhores,
        "piores": piores,
        "abertura_melhores": contagem(melhores, "tipo_abertura"),
        "abertura_piores": contagem(piores, "tipo_abertura"),
        "palavras_melhores": mediana([x["palavras_legenda"] for x in melhores]),
        "palavras_piores": mediana([x["palavras_legenda"] for x in piores]),
        "posts_zero_salvamento": zero_salv,
        "posts": posts,
    }

    # ---------- markdown ----------
    L = []
    L.append(f"# Perfil de desempenho — Instagram\n")
    L.append(f"Gerado em {hoje} por `scripts/perfil-de-desempenho.py`, Graph API {VERSAO}. "
             f"{len(posts)} posts lidos, {len(organicos)} entram na conta "
             f"(período {periodo}).")
    if excluidos:
        L.append(f"Excluídos por impulsionamento: {len(excluidos)} post(s).")
    else:
        L.append("**Nenhum post excluído por impulsionamento.** Se algum dos posts abaixo "
                 "foi impulsionado, o alcance dele inclui o pago — rodar de novo com "
                 "`--excluir ID,ID` (IDs no JSON ao lado).")
    L.append("\nDado real da conta. Onde a API não devolveu métrica, está `-` e não entrou "
             "na mediana. Nada aqui é estimativa.\n")

    L.append("## Por formato\n")
    L.append("| Formato | Posts | Alcance mediano | Faixa | Salvamentos | Compartilh. | Com zero salv. |")
    L.append("|---|---:|---:|---|---:|---:|---:|")
    for f, r in sorted(formatos.items(), key=lambda kv: -(kv[1]["mediana_alcance"] or 0)):
        L.append(f"| {f} | {r['n']} | {fmt(r['mediana_alcance'])} | "
                 f"{fmt(r['min_alcance'])}–{fmt(r['max_alcance'])} | "
                 f"{r['salvamentos']} | {r['compartilhamentos']} | "
                 f"{r['com_zero_salvamento']} de {r['n']} |")

    if len(formatos) > 1:
        ordenado = sorted(formatos.items(), key=lambda kv: -(kv[1]["mediana_alcance"] or 0))
        (f1, r1), (f2, r2) = ordenado[0], ordenado[-1]
        if r2["mediana_alcance"]:
            razao = r1["mediana_alcance"] / r2["mediana_alcance"]
            L.append(f"\n**{f1} entrega {razao:.1f}x o alcance mediano de {f2} nessa conta.**")

    L.append(f"\n**Salvamento:** {zero_salv} de {len(organicos)} posts com zero. "
             f"Salvamento é o placar do conteúdo útil — enquanto não sai do chão, o que "
             f"a marca ensina não está sendo guardado.\n")

    def tabela(titulo, lista):
        L.append(f"## {titulo}\n")
        L.append("| Data | Formato | Alcance | Salv. | Comp. | Abertura | Tipo |")
        L.append("|---|---|---:|---:|---:|---|---|")
        for x in lista:
            L.append(f"| {x['data']} | {x['formato']} | {fmt(x['alcance'])} | "
                     f"{fmt(x['salvamentos'])} | {fmt(x['compartilhamentos'])} | "
                     f"{x['abertura'].replace('|', '/')} | {x['tipo_abertura']} |")
        L.append("")

    tabela(f"Os {corte} melhores por alcance", melhores)
    tabela(f"Os {corte} piores por alcance", piores)

    L.append("## Como abrem\n")
    L.append(f"- Melhores: {perfil['abertura_melhores']} — mediana de "
             f"{perfil['palavras_melhores']} palavras de legenda")
    L.append(f"- Piores: {perfil['abertura_piores']} — mediana de "
             f"{perfil['palavras_piores']} palavras de legenda")
    L.append("\nA classificação de abertura é grossa (primeira linha da legenda). "
             "Quem lê o perfil refina: o que os melhores têm em comum de verdade — "
             "história, número, pergunta do público — é leitura, não regex.\n")

    L.append("## Como usar\n")
    L.append("- `/revisar`: comparar o formato e a abertura da peça com as medianas "
             "acima. Formato abaixo da mediana pede justificativa, com o número.")
    L.append("- `/semana` e `/relatorio`: o resultado de cada peça se lê contra a "
             "mediana do formato dela, não contra número absoluto.")
    L.append("- Atualizar todo mês, ou quando entrar formato novo. O arquivo datado "
             "fica; `perfil-de-desempenho.md` é sempre o mais recente.")
    L.append("- Cruzar com `conteudo/arquitetura-editorial.md` — se a regra de formato de "
             "lá divergir disto aqui, o dado novo manda e a nota é que envelheceu.")

    os.makedirs(SAIDA, exist_ok=True)
    md = "\n".join(L) + "\n"
    for nome in (f"perfil-{hoje}.md", "perfil-de-desempenho.md"):
        with open(os.path.join(SAIDA, nome), "w", encoding="utf-8") as f:
            f.write(md)
    with open(os.path.join(SAIDA, f"perfil-{hoje}.json"), "w", encoding="utf-8") as f:
        json.dump(perfil, f, ensure_ascii=False, indent=2)

    print(f"\nperfil salvo em pesquisa/investigacoes/desempenho/perfil-{hoje}.md "
          f"(e perfil-de-desempenho.md)")
    for f, r in formatos.items():
        print(f"  {f:<9} n={r['n']:<3} alcance mediano {fmt(r['mediana_alcance'])}")
    print(f"  zero salvamento: {zero_salv} de {len(organicos)}")


if __name__ == "__main__":
    main()
