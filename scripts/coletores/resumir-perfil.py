# -*- coding: utf-8 -*-
"""Resume um perfil coletado pelo Apify (posts) e monta a folha top-12.

    py scripts/coletores/resumir-perfil.py <handle> <nome-do-json> [<handle> <nome-do-json> ...]
    py scripts/coletores/resumir-perfil.py perfil-referencia ig-perfil-referencia-posts

<nome-do-json> é o <nome> usado no apify.py, sem extensão: lê pesquisa/coleta/raw/<nome>.json.

Pra cada perfil:
  - ranqueia os posts por engajamento (curtidas + 3×comentários) e baixa a capa dos 12 melhores
  - baixa os slides inteiros dos carrosséis entre os 6 melhores
  - monta _top12.jpg, a folha de contato pra leitura visual do formato
  - mede ritmo (posts/dia), mix de formato e medianas de curtida, comentário e view

Saída: pesquisa/referencias/perfis/<handle>/ e o consolidado
pesquisa/referencias/perfis/resumo-perfis.json (acumula entre rodadas).

Rodar no mesmo dia da coleta: os links do CDN do Instagram expiram.
Requer Pillow (py -m pip install pillow).
"""
import datetime, io, json, os, statistics as st, sys, urllib.request
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow não instalado: py -m pip install pillow")

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(RAIZ, "pesquisa", "coleta", "raw")
PERFIS = os.path.join(RAIZ, "pesquisa", "referencias", "perfis")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

try:
    FONTE = ImageFont.truetype("arial.ttf", 16)
except Exception:
    FONTE = ImageFont.load_default()


def baixar(url, caminho):
    if not url:
        return False
    if os.path.exists(caminho):
        return True
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            dados = r.read()
        with open(caminho, "wb") as f:
            f.write(dados)
        return True
    except Exception:
        return False


def resumir(h, nome_json):
    raw = os.path.join(RAW, nome_json + ".json")
    if not os.path.exists(raw):
        print(f"@{h}: JSON não encontrado ({os.path.relpath(raw, RAIZ)})"); return None
    it = [i for i in json.load(io.open(raw, encoding="utf-8"))["itens"] if not i.get("error")]
    it = [i for i in it if i.get("timestamp")]
    if not it:
        print(f"@{h}: vazio (nenhum post com data no JSON)"); return None
    pasta = os.path.join(PERFIS, h); os.makedirs(pasta, exist_ok=True)
    datas = sorted(i["timestamp"][:10] for i in it)
    for i in it:
        i["_eng"] = (i.get("likesCount") or 0) + 3 * (i.get("commentsCount") or 0)
    top = sorted(it, key=lambda i: -i["_eng"])[:12]
    ims = []
    for n, i in enumerate(top, 1):
        cap = os.path.join(pasta, f"top{n:02d}-{i.get('shortCode')}.jpg")
        if baixar(i.get("displayUrl", ""), cap):
            try:
                im = Image.open(cap).convert("RGB"); H = 360
                ims.append((im.resize((int(im.width * H / im.height), H)),
                            f"{n}. {str(i.get('type'))[:5]} {i.get('likesCount') or 0} curt. {i.get('commentsCount') or 0} com."))
            except Exception:
                pass
        if n <= 6 and i.get("type") == "Sidecar":
            for k, u in enumerate(i.get("images") or [], 1):
                baixar(u, os.path.join(pasta, f"top{n:02d}-{i.get('shortCode')}-slide{k:02d}.jpg"))
    if ims:
        cols = 6; rows = (len(ims) + cols - 1) // cols; wmax = max(im.width for im, _ in ims); W = cols * (wmax + 10) + 10
        folha = Image.new("RGB", (W, rows * 400 + 40), "white"); d = ImageDraw.Draw(folha)
        d.text((10, 8), f"@{h} · top 12 por engajamento (curtidas + 3×comentários) · {len(it)} posts coletados", fill="black", font=FONTE)
        for k, (im, leg) in enumerate(ims):
            x = 10 + (k % cols) * (wmax + 10); y = 40 + (k // cols) * 400
            folha.paste(im, (x, y)); d.text((x, y + 362), leg, fill="black", font=FONTE)
        folha.save(os.path.join(pasta, "_top12.jpg"), quality=82)
    else:
        print(f"@{h}: nenhuma capa baixou — link expirado? Coletar de novo e rodar no mesmo dia.")
    likes = [i.get("likesCount") or 0 for i in it]
    com = [i.get("commentsCount") or 0 for i in it]
    views = [i.get("videoPlayCount") or i.get("videoViewCount") for i in it if i.get("type") == "Video"]
    views = [v for v in views if v is not None]  # view ausente não vira zero
    dias = max(1, (datetime.date.fromisoformat(datas[-1]) - datetime.date.fromisoformat(datas[0])).days)
    r = {"posts_coletados": len(it), "periodo": [datas[0], datas[-1]], "posts_por_dia": round(len(it) / dias, 2),
         "mix": dict(Counter(i.get("type") for i in it)), "likes_mediana": st.median(likes),
         "comentarios_mediana": st.median(com), "views_mediana": st.median(views) if views else None,
         "fonte": os.path.relpath(raw, RAIZ).replace("\\", "/"),
         "top12": [{"n": n, "code": i.get("shortCode"), "tipo": i.get("type"), "data": i["timestamp"][:10],
                    "likes": i.get("likesCount"), "comentarios": i.get("commentsCount"),
                    "views": i.get("videoPlayCount") or i.get("videoViewCount"), "url": i.get("url"),
                    "legenda": (i.get("caption") or "")[:300], "slides": len(i.get("images") or [])}
                   for n, i in enumerate(top, 1)],
         "folha": os.path.relpath(os.path.join(pasta, "_top12.jpg"), RAIZ).replace("\\", "/") if ims else None}
    print(f"@{h:26s} posts={len(it)} {datas[0]}→{datas[-1]} ({r['posts_por_dia']}/dia) mix={r['mix']} "
          f"likes med={r['likes_mediana']} com med={r['comentarios_mediana']} views med={r['views_mediana']}")
    return r


if __name__ == "__main__":
    pares = sys.argv[1:]
    if not pares or len(pares) % 2:
        raise SystemExit("uso: py scripts/coletores/resumir-perfil.py <handle> <nome-do-json> [<handle> <nome-do-json> ...]")
    os.makedirs(PERFIS, exist_ok=True)
    p = os.path.join(PERFIS, "resumo-perfis.json")
    res = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {}
    for k in range(0, len(pares), 2):
        handle = pares[k].lstrip("@")
        r = resumir(handle, pares[k + 1])
        if r:
            res[handle] = r
    json.dump(res, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nconsolidado: {os.path.relpath(p, RAIZ)}")
