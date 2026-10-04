# -*- coding: utf-8 -*-
"""Gera um carrossel (HTML pronto pra renderizar) a partir de uma ficha em YAML.

    py scripts/carrossel/gerar.py <ficha.yaml> [--saida pasta] [--render] [--marca outro.yaml]

Modelo "editorial" (v2): layouts nomeados, o desenho em scripts/carrossel/modelo.css e a
marca em identidade/marca-visual.yaml (cores, fontes, logo, @, motivos decorativos). O
gerador lê o YAML da marca e injeta as variáveis CSS no HTML: cliente novo = editar o YAML
e trocar o logo, sem mexer em código. Vocabulário de cada layout: identidade/carrossel.md.

A ficha:
    slug: tres-erros-no-orcamento
    serie: "Nome da linha editorial"   # olho do cabeçalho (padrão: `serie` da marca)
    edicao: "nº 01 · out 2026"         # opcional
    handle: "@perfil"                  # opcional (padrão: `handle` da marca)
    limpo: true                        # opcional: cabeça só com o logo, pé sem o @
    fotos: fotos                       # opcional; pasta das fotos (relativa à ficha ou à raiz)
    slides:
      - layout: capa | texto | numero | metade | cartoes | prova | secao | comparativo | ...
        ...campos do layout (ver identidade/carrossel.md)

Saída: <saida>/carrossel.html (+ modelo.css, logo e fotos copiados) e, com --render, os PNGs
em <saida>/instagram/ via scripts/render-carrossel.js e a folha de contato <saida>/_previa.png.
Regras que o gerador aplica sozinho: alternância escuro/claro nos slides internos, contador,
seta nos internos, motivos decorativos conforme a marca, e os avisos de slide com mais de 60
palavras, foto não encontrada, logo ausente e contraste de cor abaixo do mínimo.
"""
import argparse, html, io, math, os, re, shutil, subprocess, sys
try:
    import yaml
except ImportError:
    sys.exit("Falta o PyYAML. Instale com:  py -m pip install pyyaml")
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AQUI = os.path.dirname(os.path.abspath(__file__))
MARCA_PADRAO = os.path.join(RAIZ, "identidade", "marca-visual.yaml")

# O visual neutro: vale quando identidade/marca-visual.yaml não existe ou deixa um campo vazio.
NEUTRO = {
    "nome": "Sua Empresa",
    "handle": "",
    "serie": "",
    "logo": "identidade/logo.png",
    "logo_escuro": "",
    "logo_no_escuro": "branco",
    "logo_largura": 150,
    "cores": {"escuro": "#16202E", "claro": "#F5F3EE", "destaque": "#C2410C", "texto": "#3B3F45",
              "titulo": "", "destaque_texto": "", "sobre_destaque": ""},
    "fontes": {"corpo": {"familia": "Inter", "pesos": "300;400;600;700;800", "reserva": "'Segoe UI', system-ui, sans-serif"},
               "titulo": {"familia": "", "pesos": "", "reserva": ""}},
    "peso_titulo": 300,
    "cantos": 3,
    "motivos": {"halftone": True, "curva": False},
    "seta": "arraste",
    "metodo": [],
}


# ---------- marca ----------
def mesclar(base, novo):
    out = dict(base)
    for k, v in (novo or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = mesclar(out[k], v)
        elif v not in (None, ""):
            out[k] = v
    return out


def hex_rgb(h):
    h = str(h).strip().lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise SystemExit(f"cor inválida no marca-visual.yaml: {h!r} (use #RRGGBB)")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(x))) for x in c)


def luminancia(c):
    def canal(v):
        v /= 255
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = (canal(x) for x in c)
    return .2126 * r + .7152 * g + .0722 * b


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + .05) / (lb + .05)


def escurecer(c, f):
    return tuple(x * (1 - f) for x in c)


def carregar_marca(caminho, avisos):
    if os.path.exists(caminho):
        dado = yaml.safe_load(io.open(caminho, encoding="utf-8")) or {}
    else:
        dado = {}
        avisos.append(f"marca: {os.path.relpath(caminho, RAIZ)} não existe — usando o visual neutro padrão")
    m = mesclar(NEUTRO, dado)
    c = m["cores"]
    esc_, cla, des, txt = (hex_rgb(c[k]) for k in ("escuro", "claro", "destaque", "texto"))
    tit = hex_rgb(c["titulo"]) if c.get("titulo") else esc_
    # destaque usado como TEXTO sobre o claro: se a cor da marca não tem contraste, escurece até ter
    if c.get("destaque_texto"):
        dtx = hex_rgb(c["destaque_texto"])
    else:
        dtx, f = des, 0.0
        while contraste(dtx, cla) < 4.5 and f < .9:
            f += .05; dtx = escurecer(des, f)
    sob = hex_rgb(c["sobre_destaque"]) if c.get("sobre_destaque") else (
        (255, 255, 255) if contraste((255, 255, 255), des) >= contraste(esc_, des) else esc_)
    m["_rgb"] = {"escuro": esc_, "claro": cla, "destaque": des, "texto": txt, "titulo": tit, "destaque_texto": dtx, "sobre_destaque": sob}
    # régua de contraste (WCAG AA, 4,5:1 pra texto corrido)
    for nome, a, b in (("branco sobre a cor escura", (255, 255, 255), esc_), ("texto sobre o claro", txt, cla),
                       ("título sobre o claro", tit, cla), ("texto sobre o destaque (selo, botão)", sob, des)):
        r = contraste(a, b)
        if r < 4.5: avisos.append(f"contraste baixo: {nome} = {r:.1f}:1 (mínimo 4,5:1) — revisar as cores no marca-visual.yaml")
    return m


def fontes_marca(m):
    """Família de corpo e de título, o <link> do Google Fonts e a pilha CSS de cada uma."""
    corpo, titulo = m["fontes"]["corpo"], m["fontes"].get("titulo") or {}
    if not titulo.get("familia"): titulo = corpo
    familias, link = [], ""
    for f in (corpo, titulo):
        if f.get("familia") and f.get("google", True) and f["familia"] not in [x[0] for x in familias]:
            pesos = f.get("pesos") or "300;400;600;700;800"
            if isinstance(pesos, (list, tuple)): pesos = ";".join(str(p) for p in pesos)
            familias.append((f["familia"], str(pesos).replace(",", ";").replace(" ", "")))
    if familias:
        q = "&".join(f"family={nome.replace(' ', '+')}:wght@{pesos}" for nome, pesos in familias)
        link = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                f'<link href="https://fonts.googleapis.com/css2?{q}&display=swap" rel="stylesheet">')
    pilha = lambda f: (f"'{f['familia']}', " if f.get("familia") else "") + (f.get("reserva") or "'Segoe UI', system-ui, sans-serif")
    return link, pilha(corpo), pilha(titulo)


def css_marca(m):
    r = m["_rgb"]
    trip = lambda c: ",".join(str(round(x)) for x in c)
    _, fc, ft = fontes_marca(m)
    v = {"--escuro": rgb_hex(r["escuro"]), "--escuro-2": rgb_hex(escurecer(r["escuro"], .22)), "--escuro-rgb": trip(r["escuro"]),
         "--claro": rgb_hex(r["claro"]), "--claro-rgb": trip(r["claro"]),
         "--destaque": rgb_hex(r["destaque"]), "--destaque-txt": rgb_hex(r["destaque_texto"]), "--sobre-destaque": rgb_hex(r["sobre_destaque"]),
         "--texto": rgb_hex(r["texto"]), "--texto-rgb": trip(r["texto"]), "--titulo": rgb_hex(r["titulo"]),
         "--fonte": fc, "--fonte-titulo": ft, "--peso-titulo": str(int(m.get("peso_titulo", 300))),
         "--raio": f"{int(m.get('cantos', 3))}px", "--logo-largura": f"{int(m.get('logo_largura', 150))}px"}
    return "<style>:root{" + ";".join(f"{k}:{val}" for k, val in v.items()) + "}</style>"


# ---------- texto ----------
def esc(s):
    return html.escape(str(s if s is not None else ""), quote=False)


def rich(s):
    """Texto com marcação leve: **negrito** vira <b>, [palavra] vira destaque, quebras viram <br>."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s, flags=re.S)  # o negrito pode atravessar uma quebra de linha
    s = re.sub(r"\[(.+?)\]", r'<span class="dest">\1</span>', s)
    s = s.replace("&lt;small&gt;", "<small>").replace("&lt;/small&gt;", "</small>")
    return s.replace("\n", "<br>")


def palavras(*textos):
    return sum(len(re.findall(r"\S+", str(t or ""))) for t in textos)


# ---------- peças comuns ----------
def curva(ctx, y=0, flip=False):
    if not ctx["motivos"].get("curva"): return ""
    d = "M -20 160 C 260 40, 620 40, 1100 150" if not flip else "M -20 60 C 260 190, 620 190, 1100 70"
    return f'<svg class="curva" style="top:{y}px" viewBox="0 0 1080 220" preserveAspectRatio="none"><path d="{d}"/></svg>'


def cab(logo, serie, n, total, edicao=None, limpo=False):
    if limpo or not serie and not edicao and total == 1:
        return f'<div class="cab">{logo}</div>'
    cont = "" if total == 1 else f" · {n:02d}/{total:02d}"   # card único: sem contador
    olho = esc(serie) + (f'<span class="n">{esc(edicao)}{cont}</span>' if edicao else (f'<span class="n">{cont[3:]}</span>' if cont else ""))
    return f'<div class="cab">{logo}<div class="olho">{olho}</div></div>'


def pe(handle, ultimo, texto_seta="arraste"):
    seta = "" if ultimo or not texto_seta else f'<span class="seta">{esc(texto_seta)}</span>'
    return f'<div class="pe"><span>{esc(handle)}</span>{seta}</div>'


def foto_url(f, ctx):
    """Acha a foto (pasta `fotos` da ficha, pasta da ficha, raiz), agenda a cópia pra saída e devolve o
    nome. Foto que não existe vira aviso e o slide sai com a cor escura no lugar."""
    if not f: return ""
    f = str(f)
    if f in ctx["fotos_ok"]: return ctx["fotos_ok"][f]
    for base in ctx["bases_foto"]:
        src = f if os.path.isabs(f) else os.path.join(base, f)
        if os.path.exists(src):
            ctx["copiar"][os.path.basename(f)] = src
            ctx["fotos_ok"][f] = esc(os.path.basename(f))
            return ctx["fotos_ok"][f]
    ctx["avisos"].append(f"foto não encontrada: {f} (procurei em: {', '.join(os.path.relpath(b, RAIZ) for b in ctx['bases_foto'])})")
    ctx["fotos_ok"][f] = ""
    return ""


def bg(f, ctx, extra=""):
    u = foto_url(f, ctx)
    return (f"background-image:url('{u}')" if u else "background-image:none") + extra


def corpo_html(itens):
    if not itens: return ""
    if isinstance(itens, str): itens = [itens]
    out = []
    for t in itens:
        cls = "corpo"
        if isinstance(t, dict):
            if t.get("destaque"): cls += " destaque"
            if t.get("seta"): cls += " seta"
            t = t.get("texto", "")
        out.append(f'<p class="{cls}">{rich(t)}</p>')
    return "".join(out)


def credito(s, cls="credito-foto"):
    """Crédito da imagem: foto oficial com licença, ou o aviso de imagem gerada por IA."""
    return f'<div class="{cls}">{esc(s["credito"])}</div>' if s.get("credito") else ""


def olho_secao(s):
    return f'<div class="olho-secao">{esc(s["olho"])}</div>' if s.get("olho") else ""


def tam(tag, s, chave):
    return f' style="font-size:{int(s[chave])}px"' if s.get(chave) else ""


# ---------- layouts ----------
def slide_capa(s, ctx):
    if s.get("estilo") == "noticia":
        # card de notícia: tag à esquerda com filete, edição à direita, sem logo e sem rodapé
        cabn = f'<div class="cab cab-noticia"><div class="tag">{esc(s.get("tag", "Notícias"))}</div><div class="ed">{esc(s.get("edicao", ""))}</div></div>'
        return (f'<div class="slide foto noticia{" topo" if s.get("topo") else ""}"><div class="bg" style="{bg(s.get("foto"), ctx)}"></div>'
                f'{cabn}<main>{("<div class=selo-capa>" + esc(s["selo"]) + "</div>") if s.get("selo") else ""}'
                f'<h1{tam("h1", s, "h1")}>{rich(s["titulo"])}</h1>'
                f'{("<p class=sub>" + rich(s["sub"]) + "</p>") if s.get("sub") else ""}</main></div>')
    sem = "" if s.get("foto") else ctx["halftone_capa"]
    selo = (f'<div class="selo-capa{" grande" if s.get("selo_grande") else ""}">{esc(s["selo"])}</div>') if s.get("selo") else olho_secao(s)
    return (f'<div class="slide foto{" topo" if s.get("topo") else ""}{" leve" if s.get("degrade") == "leve" else ""}">'
            f'{"<div class=barra></div>" if s.get("barra") else ""}<div class="bg" style="{bg(s.get("foto"), ctx)}"></div>{sem}'
            f'{curva(ctx, 470, True) if s.get("linha", True) else ""}'
            f'{ctx["cab"]}<main class="{"centro" if s.get("alinha") == "centro" else ""}">{selo}<h1{tam("h1", s, "h1")}>{rich(s["titulo"])}</h1>'
            f'{("<p class=sub>" + rich(s["sub"]) + "</p>") if s.get("sub") else ""}</main>{credito(s)}{pe(ctx["handle"], False, s.get("seta", ctx["seta"]))}</div>')


def slide_capa_dupla(s, ctx):
    a, b = s["a"], s["b"]
    lado = lambda x: (f'<div class="lado" style="{bg(x.get("foto"), ctx)}"><div class="rot">'
                      f'<div class="k">{esc(x.get("k", ""))}</div><div class="t">{rich(x["t"])}</div></div></div>')
    return (f'<div class="slide dupla-capa escuro"><div class="dupla">{lado(a)}{lado(b)}<div class="vs">{esc(s.get("vs", "×"))}</div></div>'
            f'{ctx["cab"]}<main><h1>{rich(s["titulo"])}</h1></main>{pe(ctx["handle"], False, ctx["seta"])}</div>')


def slide_texto(s, ctx):
    fonte = f'<div class="fonte">Fonte: {rich(s["fonte"])}</div>' if s.get("fonte") else ""
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main class="{s.get("alinha", "")}">{olho_secao(s)}'
            f'{("<h2" + tam("h2", s, "h2") + ">" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}{corpo_html(s.get("corpo"))}{fonte}</main>{ctx["pe"]}</div>')


def slide_numero(s, ctx):
    fonte = f'<div class="prova"><div class="k">Fonte</div><div class="t">{rich(s["fonte"])}</div></div>' if s.get("fonte") else ""
    if s.get("fonte") and ctx.get("limpo"):  # ficha limpa: a fonte vira uma linha, sem o cartão
        fonte = f'<div class="fonte">Fonte: {rich(s["fonte"])}</div>'
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{olho_secao(s)}'
            f'<div class="numero">{rich(s["numero"])}</div><div class="rotulo">{rich(s.get("rotulo", ""))}</div>{corpo_html(s.get("corpo"))}{fonte}</main>{ctx["pe"]}</div>')


def slide_metade(s, ctx):
    """Metade foto, metade texto. `alto` é a altura da foto (padrão 640); o texto começa 60 px abaixo dela."""
    fonte = f'<div class="fonte">{rich(s["fonte"])}</div>' if s.get("fonte") else ""
    alto = int(s.get("alto", 640))
    pos = f';background-position:{esc(s["pos"])}' if s.get("pos") else ""
    return (f'<div class="slide metade {ctx["fundo"]}">{ctx["halftone"]}<main>'
            f'<div class="foto-half" style="height:{alto}px;{bg(s.get("foto"), ctx, pos)}">{credito(s, "credito-half")}</div>{marcas_svg(s.get("marcas"))}{curva(ctx, 510, True) if s.get("linha", True) else ""}'
            f'<div class="texto-half" style="top:{alto + 60}px">{("<div class=numero>" + rich(s["numero"]) + "</div>") if s.get("numero") else ""}'
            f'<div class="rotulo">{rich(s.get("rotulo", ""))}</div>{corpo_html(s.get("corpo"))}{fonte}</div></main>{ctx["cab"]}{ctx["pe"]}</div>')


def slide_cartoes(s, ctx):
    fonte = f'<div class="fonte">{rich(s["fonte"])}</div>' if s.get("fonte") else ""
    its = []
    for i, it in enumerate(s["itens"], 1):
        selo = '<div class="selo check"></div>' if s.get("check") else f'<div class="selo">{esc(it.get("n", i))}</div>'
        its.append(f'<div class="cartao">{selo}<div><div class="t">{rich(it["t"])}</div>{("<div class=d>" + rich(it["d"]) + "</div>") if it.get("d") else ""}</div></div>')
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{olho_secao(s)}'
            f'{("<h2" + tam("h2", s, "h2") + ">" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}<div class="cartoes">{"".join(its)}</div>{corpo_html(s.get("corpo"))}{fonte}</main>{ctx["pe"]}</div>')


def slide_prova(s, ctx):
    c = s["cartao"]
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{olho_secao(s)}'
            f'{("<h2" + tam("h2", s, "h2") + ">" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}{corpo_html(s.get("antes"))}'
            f'<div class="prova"><div class="k">{esc(c.get("k", "Fonte"))}</div><div class="t">{rich(c["t"])}</div>'
            f'{("<div class=fonte>" + rich(c["fonte"]) + "</div>") if c.get("fonte") else ""}</div>{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


def slide_secao(s, ctx):
    foto = f'<div class="foto-cartao" style="{bg(s["foto"], ctx)}"></div>' if s.get("foto") else ""
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{curva(ctx, 120)}{ctx["cab"]}<main>'
            f'<div class="selo-secao"><div class="n">{esc(s.get("n", ""))}</div><div class="t">{esc(s.get("olho", ""))}</div></div>'
            f'<h2{tam("h2", s, "h2")}>{rich(s["titulo"])}</h2>{corpo_html(s.get("corpo"))}{foto}</main>{ctx["pe"]}</div>')


def slide_comparativo(s, ctx):
    a, b = s["a"], s["b"]
    fa = f' com-foto" style="{bg(a["foto"], ctx)}' if a.get("foto") else '"'
    fb = f' com-foto" style="{bg(b["foto"], ctx)}' if b.get("foto") else '"'
    seta = "" if ctx["ultimo"] or not ctx["seta"] else f'<span class=seta>{esc(ctx["seta"])}</span>'
    return (f'<div class="slide comp"><main><div class="metade-a{fa}><div class="txt"><div class="k">{esc(a.get("k", ""))}</div><div class="t">{rich(a["t"])}</div></div></div>'
            f'<div class="divisor"></div><div class="metade-b{fb}><div class="txt"><div class="k">{esc(b.get("k", ""))}</div><div class="t">{rich(b["t"])}</div></div></div></main>'
            f'{ctx["cab"]}<div class="pe" style="color:rgba(255,255,255,.62)"><span>{esc(ctx["handle"])}</span>{seta}</div></div>')


def slide_diagrama(s, ctx):
    """Círculos conectados. `alto` (altura do diagrama, padrão 700), `raio` (distância dos satélites ao
    centro, padrão 265) e `girar` (graus somados ao ângulo inicial: com 4 satélites, `girar: 45` põe os
    círculos nas diagonais e o diagrama cabe em 600 px, sobrando lugar pro corpo)."""
    sats = s["satelites"]; n = len(sats)
    alto = int(s.get("alto", 700)); cx, cy, r = 444, alto // 2, int(s.get("raio", 265))
    gira = math.radians(float(s.get("girar", 0)))
    nos, linhas = [], []
    for i, it in enumerate(sats):
        ang = -math.pi / 2 + gira + 2 * math.pi * i / n
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        linhas.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}"/>')
        nos.append(f'<div class="no sat" style="left:{x:.0f}px;top:{y:.0f}px"><div class="t">{rich(it["t"])}</div>{("<div class=d>" + rich(it["d"]) + "</div>") if it.get("d") else ""}</div>')
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>'
            f'{("<h2 style=margin-bottom:10px>" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}'
            f'<div class="diagrama" style="height:{alto}px"><svg viewBox="0 0 888 {alto}">{"".join(linhas)}</svg>{"".join(nos)}<div class="no centro" style="left:{cx}px;top:{cy}px">{rich(s["centro"])}</div></div>'
            f'{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


def slide_fecho(s, ctx):
    metodo = ""
    etapas = s.get("metodo") if isinstance(s.get("metodo"), list) else (ctx["metodo"] if s.get("metodo", True) else [])
    if etapas:
        metodo = '<div class="metodo">' + "<i>→</i>".join(f"<span>{esc(e)}</span>" for e in etapas) + "</div>"
    # `largo: true`: a foto ocupa a largura toda no alto (foto de grupo) e o texto vem embaixo; `pos` enquadra
    largo = " largo" if s.get("largo") else ""
    sem = "" if s.get("foto") else " sem-foto"
    pos = f';background-position:{esc(s["pos"])}' if s.get("pos") else ""
    alto = f';height:{int(s["alto"])}px' if s.get("largo") and s.get("alto") else ""
    topo = f' style="top:{int(s["alto"]) - 50}px"' if alto else ""
    pessoa = f'<div class="pessoa" style="{bg(s.get("foto"), ctx, pos + alto)}"></div>' if s.get("foto") else ""
    ht = '<div class="halftone" style="right:auto;left:-140px"></div>' if ctx["motivos"].get("halftone") else ""
    return (f'<div class="slide fecho escuro{largo}{sem}">{ht}{pessoa}{curva(ctx, 150) if s.get("linha", True) else ""}{ctx["cab"]}<main{topo}>'
            f'{olho_secao(s)}<h2{tam("h2", s, "h2")}>{rich(s["titulo"])}</h2>{corpo_html(s.get("corpo"))}'
            f'{("<div class=nome>" + esc(s["nome"]) + "</div>") if s.get("nome") else ""}{("<div class=cargo>" + rich(s["cargo"]) + "</div>") if s.get("cargo") else ""}'
            f'{("<div class=cta>" + esc(s["cta"]) + "</div>") if s.get("cta") else ""}{metodo}</main>{pe(ctx["handle"], True)}</div>')


def slide_notas(s, ctx):
    """Dois documentos lado a lado (nota, orçamento, recibo): a{k, linhas[{t,v,destaque|apagado}], veredito}, b{...}."""
    def nota(x, foco):
        lins = "".join(f'<div class="lin{" on" if l.get("destaque") else ""}{" off" if l.get("apagado") else ""}"><span>{esc(l["t"])}</span><span>{esc(l.get("v", ""))}</span></div>' for l in x["linhas"])
        return f'<div class="nota{" foco" if foco else ""}"><div class="cabn">{esc(x["k"])}</div>{lins}<div class="veredito">{rich(x["veredito"])}</div></div>'
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{olho_secao(s)}'
            f'{("<h2>" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}'
            f'<div class="notas">{nota(s["a"], False)}{nota(s["b"], True)}</div>{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


# ---------- reação: quadro de vídeo, print de manchete, extrato ----------
def slide_capa_reacao(s, ctx):
    """Capa de reação a uma fala pública: quadro do vídeo sangrando, selo com ponto, a frase em h1,
    a pergunta da casa sob um filete e o botão como pílula."""
    leg = f'<div class="legenda-foto">{esc(s["legenda"])}</div>' if s.get("legenda") else ""
    return (f'<div class="slide foto reacao{" topo" if s.get("topo") else ""}"><div class="bg" style="{bg(s.get("foto"), ctx)}"></div>'
            f'{curva(ctx, 470, True) if s.get("linha", False) else ""}{ctx["cab"]}<main>{leg}'
            f'{("<div class=selo-capa-ponto>" + esc(s["selo"]) + "</div>") if s.get("selo") else ""}'
            f'<h1{tam("h1", s, "h1")}>{rich(s["titulo"])}</h1>'
            f'{("<div class=pergunta>" + rich(s["pergunta"]) + "</div>") if s.get("pergunta") else ""}</main>'
            f'{pe(ctx["handle"], False, s.get("seta", ctx["seta"]))}</div>')


def slide_frame(s, ctx):
    """Quadro de vídeo como player (imagem 16:9, minutagem, fonte, barra de progresso), a frase dita em
    aspas grandes e o comentário da casa com filete. Campos: foto, tempo, fonte, progresso (0-100),
    frase, comentario, olho."""
    chips = (f'{("<span class=chip-t>" + esc(s["tempo"]) + "</span>") if s.get("tempo") else ""}'
             f'{("<span class=chip-f>" + esc(s["fonte"]) + "</span>") if s.get("fonte") else ""}')
    prog = f'<div class="barra-play"><i style="width:{int(s.get("progresso", 84))}%"></i></div>'
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{olho_secao(s)}'
            f'<div class="player"><img src="{foto_url(s.get("foto"), ctx)}" alt="">{chips}{prog}</div>'
            f'{("<div class=aspas>" + rich(s["frase"]) + "</div>") if s.get("frase") else ""}'
            f'{("<div class=coment><span>" + rich(s["comentario"]) + "</span></div>") if s.get("comentario") else ""}{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


def slide_print(s, ctx):
    """Print de manchete (capturado em tela de celular) em cartão com sombra, um ou dois lado a lado, com a
    fonte no rodapé do cartão. Campos: olho, titulo, itens[{foto, fonte}], largura, altura, comentario, corpo."""
    its = s["itens"]; n = len(its)
    largura = s.get("largura") or (640 if n == 1 else (888 - 26 * (n - 1)) // n)
    altura = s.get("altura") or (700 if n == 1 else 640)
    cards = "".join(f'<div class="print" style="width:{largura}px;height:{altura}px"><img src="{foto_url(it.get("foto"), ctx)}" alt="">'
                    f'{("<div class=fonte-print>" + esc(it["fonte"]) + "</div>") if it.get("fonte") else ""}</div>' for it in its)
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{olho_secao(s)}'
            f'{("<h2>" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}<div class="prints">{cards}</div>'
            f'{("<div class=coment><span>" + rich(s["comentario"]) + "</span></div>") if s.get("comentario") else ""}{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


def slide_extrato(s, ctx):
    """A conta como extrato: cabeçalho, linhas (rótulo à esquerda, valor à direita; `destaque` pinta o valor,
    `apagado` apaga, `small` põe a memória de cálculo), veredito e fonte. Campos: olho, titulo,
    cab{a,b}, linhas[{t,v,destaque,apagado,small}], veredito, k, fonte, corpo. (Não usar `on`/`off` como
    chave: o YAML lê como booleano.)"""
    c = s.get("cab") or {}
    lins = "".join(f'<div class="lin{" on" if l.get("destaque") else ""}{" off" if l.get("apagado") else ""}"><span>{esc(l["t"])}'
                   f'{("<small>" + esc(l["small"]) + "</small>") if l.get("small") else ""}</span><span>{esc(l.get("v", ""))}</span></div>' for l in s["linhas"])
    ver = f'<div class="veredito"><span class="k">{esc(s.get("k", "Saldo"))}</span><span>{rich(s["veredito"])}</span></div>' if s.get("veredito") else ""
    fonte = f'<div class="fonte">{rich(s["fonte"])}</div>' if s.get("fonte") else ""
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{olho_secao(s)}'
            f'{("<h2>" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}'
            f'<div class="extrato"><div class="cabn"><span>{esc(c.get("a", ""))}</span><span>{esc(c.get("b", ""))}</span></div>{lins}{ver}</div>{fonte}{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


# ---------- traço à mão: cena, roda do ano, ciclo, dois lados, mosaico ----------
MESES = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
RABISCO = ('<defs><filter id="rabisco" x="-5%" y="-5%" width="110%" height="110%">'
           '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/>'
           '<feDisplacementMap in="SourceGraphic" scale="5"/></filter></defs>')


def traco(cx, cy, rx, ry, a0=-100.0, volta=372.0, seed=0.0, ondula=0.025, girar=0.0):
    """Elipse de caneta: não fecha certinho, passa um pouco do ponto e o raio ondula de leve."""
    pts, n, g = [], 140, math.radians(girar)
    for i in range(n + 1):
        a = math.radians(a0 + volta * i / n)
        k = 1 + ondula * math.sin(3 * a + seed) + ondula * .6 * math.sin(5 * a + 2 * seed)
        x, y = rx * k * math.cos(a), ry * k * math.sin(a)
        pts.append((cx + x * math.cos(g) - y * math.sin(g), cy + x * math.sin(g) + y * math.cos(g)))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def marcas_svg(marcas):
    """Marcações de caneta (cor de destaque) sobre a imagem: `elipse: [cx, cy, rx, ry]` (+ `girar`) ou `linha: "<path d>"`."""
    if not marcas: return ""
    out = []
    for i, m in enumerate(marcas):
        if m.get("elipse"):
            cx, cy, rx, ry = m["elipse"]
            out.append(f'<path d="{traco(cx, cy, rx, ry, seed=i * 1.7, girar=m.get("girar", 0))}"/>')
        elif m.get("linha"):
            out.append(f'<path d="{esc(m["linha"])}"/>')
    return f'<svg class="marcas" viewBox="0 0 1080 1350">{RABISCO}<g filter="url(#rabisco)">{"".join(out)}</g></svg>'


def slide_cena(s, ctx):
    """Imagem sangrando com um texto no topo e outro na base, e marcações de caneta por cima.
    Campos: foto, pos (background-position), topo{t, corpo, y, cor, fonte}, base{...}, marcas[], ceu, sombra."""
    def bloco(b, cls):
        if not b: return ""
        pos = f' style="top:{int(b["y"])}px"' if b.get("y") is not None else ""  # `y`: topo do bloco em px
        cor = " txt-escuro" if b.get("cor") == "escuro" else ""
        fonte = f'<div class="fonte">{rich(b["fonte"])}</div>' if b.get("fonte") else ""
        return f'<div class="cena-txt {cls}{cor}"{pos}>{("<div class=t>" + rich(b["t"]) + "</div>") if b.get("t") else ""}{corpo_html(b.get("corpo"))}{fonte}</div>'
    # `ceu: true` tira o escuro do topo, pra imagem com o assunto lá em cima;
    # `sombra: topo` estende o escuro de cima até o meio, pra um bloco de texto maior no alto
    sombra = " sombra-topo" if s.get("sombra") == "topo" else ""
    return (f'<div class="slide foto cena{" ceu" if s.get("ceu") else ""}{sombra}"><div class="bg" style="{bg(s.get("foto"), ctx, ";background-position:" + esc(s.get("pos", "center")))}"></div>'
            f'{marcas_svg(s.get("marcas"))}{ctx["cab"]}{bloco(s.get("topo"), "topo")}{bloco(s.get("base"), "base")}{ctx["pe"]}</div>')


def slide_ano(s, ctx):
    """Roda do ano: os doze meses em círculo, a linha de destaque passando por todos em traço de caneta,
    e uma seta que chega de novo em janeiro. `marcados: [{m: 5, t: "IR"}]` acende os meses marcados.
    Campos: titulo, centro, marcados, corpo, alto (560), raio (225), no (34)."""
    alto = int(s.get("alto", 560)); r = int(s.get("raio", 225)); cx, cy = 444, alto // 2; rn = int(s.get("no", 34))
    marc = {int(m["m"]): m.get("t", "") for m in (s.get("marcados") or [])}
    fim = -90 + 345  # a linha sai de janeiro e chega de volta nele, com a seta no vão entre dezembro e janeiro
    ae = math.radians(fim); px, py = cx + r * math.cos(ae), cy + r * math.sin(ae)
    tx, ty = -math.sin(ae), math.cos(ae)
    seta = "".join(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px - 26 * (tx * math.cos(d) - ty * math.sin(d)):.1f}" y2="{py - 26 * (tx * math.sin(d) + ty * math.cos(d)):.1f}"/>'
                   for d in (math.radians(32), math.radians(-32)))
    anel = (f'<g filter="url(#rabisco)" class="anel"><path d="{traco(cx, cy, r, r, a0=-90, volta=345, ondula=.012)}"/>{seta}</g>'
            f'<g filter="url(#rabisco)" class="anel-eco"><path d="{traco(cx, cy, r + 9, r + 9, a0=-60, volta=300, seed=2.1, ondula=.018)}"/></g>')
    nos = []
    for i, nome in enumerate(MESES, 1):
        a = math.radians(-90 + 30 * (i - 1)); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        on = i in marc
        nos.append(f'<g class="mes{" on" if on else ""}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{rn}"/>'
                   f'<text x="{x:.1f}" y="{y + 5.5:.1f}" text-anchor="middle">{nome}</text></g>')
        if on and marc[i]:
            lx, ly = cx + (r + rn + 36) * math.cos(a), cy + (r + rn + 36) * math.sin(a)
            nos.append(f'<text class="rot-mes" x="{lx:.1f}" y="{ly + 8:.1f}" text-anchor="middle">{esc(marc[i])}</text>')
    centro = f'<div class="centro-ano" style="left:{cx}px;top:{cy}px">{rich(s.get("centro", ""))}</div>' if s.get("centro") else ""
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>'
            f'{("<h2 class=h2-ano>" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}'
            f'<div class="ano" style="height:{alto}px"><svg viewBox="0 0 888 {alto}">{RABISCO}{anel}{"".join(nos)}</svg>{centro}</div>'
            f'{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


def slide_ciclo(s, ctx):
    """Framework em ciclo, visão 360: N nós em volta de um anel geométrico com seta de giro no meio de cada
    trecho, um centro e, em cada nó, um selo opcional (ex.: "?" = ainda a medir). Campos: titulo, h2,
    centro, nos[{t, selo}], alto (660), raio (222), no (86), corpo."""
    alto = int(s.get("alto", 660)); r = int(s.get("raio", 222)); rn = int(s.get("no", 86)); cx, cy = 444, alto // 2
    nos = s["nos"]; n = len(nos)
    els = [f'<circle class="ciclo-anel" cx="{cx}" cy="{cy}" r="{r}"/>']
    for i in range(n):  # seta de giro (horário) no meio do arco entre dois nós
        a = math.radians(-90 + 360 * (i + .5) / n)
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        tx, ty = -math.sin(a), math.cos(a)          # tangente no sentido horário
        nx, ny = math.cos(a), math.sin(a)           # normal (para fora)
        p1 = (px + tx * 13, py + ty * 13); p2 = (px - tx * 9 + nx * 11, py - ty * 9 + ny * 11); p3 = (px - tx * 9 - nx * 11, py - ty * 9 - ny * 11)
        els.append(f'<polygon class="ciclo-seta" points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}"/>')
    for i, no in enumerate(nos):
        a = math.radians(-90 + 360 * i / n); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        linhas = str(no["t"]).split("\n")
        txt = "".join(f'<tspan x="{x:.1f}" dy="{0 if j == 0 else 26}">{esc(l)}</tspan>' for j, l in enumerate(linhas))
        els.append(f'<g class="ciclo-no"><circle cx="{x:.1f}" cy="{y:.1f}" r="{rn}"/>'
                   f'<text x="{x:.1f}" y="{y + 8 - 13 * (len(linhas) - 1):.1f}" text-anchor="middle">{txt}</text></g>')
        if no.get("selo"):
            sx, sy = x, y + rn
            els.append(f'<g class="ciclo-selo"><circle cx="{sx:.1f}" cy="{sy:.1f}" r="22"/><text x="{sx:.1f}" y="{sy + 9:.1f}" text-anchor="middle">{esc(no["selo"])}</text></g>')
    centro = f'<div class="centro-ano" style="left:{cx}px;top:{cy}px">{rich(s.get("centro", ""))}</div>' if s.get("centro") else ""
    h2 = (f'<h2 class="h2-ano"{tam("h2", s, "h2")}>{rich(s["titulo"])}</h2>') if s.get("titulo") else ""
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{h2}'
            f'<div class="ano ciclo" style="height:{alto}px"><svg viewBox="0 0 888 {alto}">{"".join(els)}</svg>{centro}</div>'
            f'{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


ICONES = {
    "retrovisor": '<svg class="ico" viewBox="0 0 40 28"><line x1="20" y1="2" x2="20" y2="9"/><rect x="3" y="9" width="34" height="16" rx="8"/></svg>',
    "para-brisa": '<svg class="ico" viewBox="0 0 40 28"><path d="M3 24 L9 4 L31 4 L37 24 Z"/><line x1="13" y1="24" x2="16" y2="16"/></svg>',
    "x": '<svg class="ico" viewBox="0 0 40 28"><line x1="10" y1="4" x2="30" y2="24"/><line x1="30" y1="4" x2="10" y2="24"/></svg>',
    "check": '<svg class="ico" viewBox="0 0 40 28"><path d="M8 14 L17 23 L33 5"/></svg>',
}


def slide_dois_lados(s, ctx):
    """A mesma situação vista de dois jeitos, linha a linha: o lado A apagado, o lado B em destaque.
    Campos: titulo, cab{a, b, ico_a, ico_b}, linhas[{k, a, b}], corpo. Ícones: retrovisor, para-brisa, x, check."""
    c = s.get("cab") or {}
    ico = lambda nome: ICONES.get(nome or "", "")
    cabs = (f'<div class="lados-cab"><span class="ca">{ico(c.get("ico_a"))}{esc(c.get("a", ""))}</span>'
            f'<span class="cb">{ico(c.get("ico_b"))}{esc(c.get("b", ""))}</span></div>')
    lins = "".join(f'<div class="lados-lin"><div class="k">{rich(l.get("k", ""))}</div><div class="a">{rich(l.get("a", ""))}</div>'
                   f'<div class="b">{rich(l.get("b", ""))}</div></div>' for l in s["linhas"])
    return (f'<div class="slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>'
            f'{("<h2" + tam("h2", s, "h2") + ">" + rich(s["titulo"]) + "</h2>") if s.get("titulo") else ""}<div class="lados">{cabs}{lins}</div>'
            f'{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


def slide_mosaico(s, ctx):
    """Grade de 3 a 5 fotos sangrando no topo e o texto embaixo. Cada foto pode ser o nome do arquivo
    ou {foto, pos}. Campos: fotos[], alto (800), rotulo, corpo."""
    fotos = s["fotos"]; alto = int(s.get("alto", 800))
    tiles = "".join(f'<div class="tile" style="{bg(f if isinstance(f, str) else f["foto"], ctx, ";background-position:" + esc("center" if isinstance(f, str) else f.get("pos", "center")))}"></div>' for f in fotos)
    return (f'<div class="slide mosaico {ctx["fundo"]}"><div class="grade n{len(fotos)}" style="height:{alto}px">{tiles}</div>'
            f'<div class="texto-half" style="top:{alto + 60}px"><div class="rotulo">{rich(s.get("rotulo", ""))}</div>{corpo_html(s.get("corpo"))}</div>'
            f'{ctx["cab"]}{ctx["pe"]}</div>')


def grafico_svg(g):
    """Infográfico em cartão branco: `tipo: linha` (a trajetória) ou `tipo: barras` (a escalada).
    pontos[{k, v, rot, destaque}]: k = rótulo do eixo, v = número, rot = o que se escreve sobre o
    ponto/barra, destaque = cor de destaque. Opcionais: titulo, nota, fonte, alto."""
    W, H = 888, int(g.get("alto", 360))
    pts = g["pontos"]; n = len(pts)
    vs = [float(p["v"]) for p in pts]
    pe_, pd_, pt_, pb_ = 70, 70, 64, 62  # margens esquerda, direita, topo, base
    xs = [pe_ + (W - pe_ - pd_) * (i / (n - 1) if n > 1 else .5) for i in range(n)]
    out = []
    if g.get("tipo", "barras") == "linha":
        lo, hi = min(vs), max(vs); folga = (hi - lo) * .25 or 1
        lo, hi = lo - folga, hi + folga
        y = lambda v: pt_ + (H - pt_ - pb_) * (1 - (v - lo) / (hi - lo))
        out.append(f'<line class="g-base" x1="{pe_ - 30}" y1="{H - pb_ + 10}" x2="{W - pd_ + 30}" y2="{H - pb_ + 10}"/>')
        out.append('<polyline class="g-linha" points="' + " ".join(f"{x:.0f},{y(v):.0f}" for x, v in zip(xs, vs)) + '"/>')
        for x, v, p in zip(xs, vs, pts):
            cls = " on" if p.get("destaque") else ""
            out.append(f'<circle class="g-pt{cls}" cx="{x:.0f}" cy="{y(v):.0f}" r="10"/>')
            out.append(f'<text class="g-val{cls}" x="{x:.0f}" y="{y(v) - 24:.0f}" text-anchor="middle">{esc(p.get("rot", v))}</text>')
            out.append(f'<text class="g-k" x="{x:.0f}" y="{H - pb_ + 46}" text-anchor="middle">{esc(p["k"])}</text>')
    else:
        hi = max(vs) * 1.12
        larg = min(150, (W - pe_ - pd_) / n * .62)
        for x, v, p in zip(xs, vs, pts):
            h = (H - pt_ - pb_) * v / hi; cls = " on" if p.get("destaque") else ""
            out.append(f'<rect class="g-barra{cls}" x="{x - larg / 2:.0f}" y="{H - pb_ - h:.0f}" width="{larg:.0f}" height="{h:.0f}" rx="3"/>')
            out.append(f'<text class="g-val{cls}" x="{x:.0f}" y="{H - pb_ - h - 16:.0f}" text-anchor="middle">{esc(p.get("rot", v))}</text>')
            out.append(f'<text class="g-k" x="{x:.0f}" y="{H - pb_ + 42}" text-anchor="middle">{esc(p["k"])}</text>')
    tit = f'<div class="g-tit">{rich(g["titulo"])}</div>' if g.get("titulo") else ""
    nota = f'<div class="g-nota">{rich(g["nota"])}</div>' if g.get("nota") else ""
    fonte = f'<div class="g-fonte">Fonte: {rich(g["fonte"])}</div>' if g.get("fonte") else ""
    return f'<div class="graf-card">{tit}<svg viewBox="0 0 {W} {H}">{"".join(out)}</svg>{nota}{fonte}</div>'


def slide_proposta(s, ctx):
    """Item numerado com prova: selo numerado + título, a explicação, o print da matéria (ou um gráfico)
    em cartão com sombra e o "Na prática" com filete. `bg: {foto, pos, tam}` põe a foto sangrando atrás,
    coberta pela cor escura (o slide vira escuro). Campos: n, titulo, corpo[], print, grafico, pratica, fonte, bg."""
    fundo_bg = s.get("bg")
    fundo = "escuro" if fundo_bg else ctx["fundo"]
    bgh = (f'<div class="bg-prop" style="{bg(fundo_bg["foto"], ctx, ";background-position:" + esc(fundo_bg.get("pos", "center")) + ";background-size:" + esc(fundo_bg.get("tam", "cover")))}"></div>') if fundo_bg else ctx["halftone"]
    prt = f'<div class="print-card"><img src="{foto_url(s["print"], ctx)}" alt=""></div>' if s.get("print") else ""
    if s.get("grafico"): prt = grafico_svg(s["grafico"]) + prt
    prat = f'<div class="pratica"><p>{rich(s["pratica"])}</p></div>' if s.get("pratica") else ""
    rod = f'<div class="fonte-rodape">Fontes: {rich(s["fonte"])}</div>' if s.get("fonte") else ""  # as fontes da tela, letra pequena
    return (f'<div class="slide proposta {fundo}{" com-bg" if fundo_bg else ""}">{bgh}{ctx["cab"]}<main>'
            f'<div class="tit-prop">{("<div class=selo-n>" + esc(s["n"]) + "</div>") if s.get("n") not in (None, "") else ""}<h2{tam("h2", s, "h2")}>{rich(s["titulo"])}</h2></div>'
            f'{corpo_html(s.get("corpo"))}{prt}{prat}</main>{rod}{ctx["pe"]}</div>')


def slide_paginas(s, ctx):
    """Páginas reais de um documento em leque, cada uma com selo numerado e etiqueta.
    Campos: titulo, h2, paginas[{foto, n, k}] (3), corpo[]."""
    cards = "".join(
        f'<div class="pag p{i}"><img src="{foto_url(p.get("foto"), ctx)}" alt="">'
        f'<div class="pag-tag"><span class="n">{esc(p.get("n", i))}</span>{esc(p.get("k", ""))}</div></div>'
        for i, p in enumerate(s["paginas"], 1))
    h2 = (f'<h2{tam("h2", s, "h2")}>{rich(s["titulo"])}</h2>') if s.get("titulo") else ""
    return (f'<div class="slide paginas-slide {ctx["fundo"]}">{ctx["halftone"]}{ctx["cab"]}<main>{h2}'
            f'<div class="leque">{cards}</div>{corpo_html(s.get("corpo"))}</main>{ctx["pe"]}</div>')


def com_recorte(h, r, ctx):
    """Figura recortada (PNG sem fundo) por cima do slide. `x` pode passar da borda: com o mesmo recorte em
    dois slides seguidos (x no primeiro, x − 1080 no segundo), a figura atravessa a divisa entre eles.
    `lado` (dir|esq) abre espaço pro texto do outro lado. Campos: foto, x, y, h, lado, brilho."""
    img = (f'<img class="recorte" src="{foto_url(r.get("foto"), ctx)}" alt="" '
           f'style="left:{int(r.get("x", 600))}px;top:{int(r.get("y", 300))}px;height:{int(r.get("h", 1050))}px">')
    if r.get("brilho"):  # `brilho: [cx, cy]`: halo claro atrás da figura, pra roupa escura não sumir no fundo escuro
        cx, cy = r["brilho"]
        img = f'<div class="brilho-rec" style="left:{int(cx) - 470}px;top:{int(cy) - 470}px"></div>' + img
    h = h.replace('<div class="slide ', f'<div class="slide com-recorte-{r.get("lado", "dir")} ', 1)
    return h[: h.rfind("</div>")] + img + "</div>"


LAYOUTS = {"capa": slide_capa, "capa-dupla": slide_capa_dupla, "capa-reacao": slide_capa_reacao,
           "texto": slide_texto, "numero": slide_numero, "metade": slide_metade, "cartoes": slide_cartoes,
           "prova": slide_prova, "secao": slide_secao, "comparativo": slide_comparativo, "diagrama": slide_diagrama,
           "notas": slide_notas, "frame": slide_frame, "print": slide_print, "extrato": slide_extrato,
           "cena": slide_cena, "ano": slide_ano, "ciclo": slide_ciclo, "dois-lados": slide_dois_lados,
           "mosaico": slide_mosaico, "proposta": slide_proposta, "paginas": slide_paginas, "fecho": slide_fecho}
SEM_ALTERNANCIA = ("capa", "capa-reacao", "capa-dupla", "fecho", "comparativo", "cena")


def contar(s):
    blocos = [b for b in (s.get("topo"), s.get("base")) if isinstance(b, dict)]  # cena
    return palavras(s.get("titulo"), s.get("sub"), s.get("rotulo"), s.get("pratica"), s.get("pergunta"), s.get("frase"),
                    s.get("comentario"), s.get("veredito"), s.get("centro"),
                    *((t.get("texto") if isinstance(t, dict) else t) for t in (s.get("corpo") or []) if not isinstance(s.get("corpo"), str)),
                    s.get("corpo") if isinstance(s.get("corpo"), str) else "",
                    *(str(it.get("t", "")) + " " + str(it.get("d", "")) for it in (s.get("itens") or []) if isinstance(it, dict)),
                    *(str(it.get("t", "")) + " " + str(it.get("d", "")) for it in (s.get("satelites") or []) if isinstance(it, dict)),
                    *(" ".join(str(l.get(c, "")) for c in ("t", "v", "small", "k", "a", "b")) for l in (s.get("linhas") or [])),
                    *(b.get("t", "") for b in blocos),
                    *((t.get("texto") if isinstance(t, dict) else t) for b in blocos for t in (b.get("corpo") or [])))


def gerar(ficha, saida, pasta_ficha, caminho_marca):
    avisos = []
    marca = carregar_marca(caminho_marca, avisos)
    slides = ficha["slides"]; total = len(slides)
    os.makedirs(saida, exist_ok=True)
    shutil.copy(os.path.join(AQUI, "modelo.css"), os.path.join(saida, "modelo.css"))

    # logo: positivo + (opcional) versão pra fundo escuro; sem arquivo, vira o nome da empresa em texto
    nome = marca.get("nome") or "Sua Empresa"
    def achar(p):
        if not p: return None
        p = p if os.path.isabs(p) else os.path.join(RAIZ, p)
        return p if os.path.exists(p) else None
    logo_src, logo_esc_src = achar(marca.get("logo")), achar(marca.get("logo_escuro"))
    corpo_cls = ""
    if logo_src:
        ext = os.path.splitext(logo_src)[1].lower()
        shutil.copy(logo_src, os.path.join(saida, "logo" + ext))
        if logo_esc_src:
            ext2 = os.path.splitext(logo_esc_src)[1].lower()
            shutil.copy(logo_esc_src, os.path.join(saida, "logo-escuro" + ext2))
            logo = (f'<img class="logo logo-pos" src="logo{ext}" alt="{esc(nome)}">'
                    f'<img class="logo logo-esc" src="logo-escuro{ext2}" alt="{esc(nome)}">')
        else:
            logo = f'<img class="logo" src="logo{ext}" alt="{esc(nome)}">'
            if marca.get("logo_no_escuro", "branco") == "branco": corpo_cls = ' class="logo-filtro"'
    else:
        logo = f'<div class="logo-txt">{esc(nome)}</div>'
        avisos.append(f"logo não encontrado ({marca.get('logo') or 'campo vazio'}) — saiu o nome \"{nome}\" em texto. "
                      "Pôr o PNG em identidade/logo.png ou ajustar `logo` no marca-visual.yaml")

    # fotos: pasta `fotos` da ficha (relativa à ficha ou à raiz), depois a pasta da ficha, depois a raiz
    bases = []
    if ficha.get("fotos"):
        pf = ficha["fotos"]
        bases += [pf] if os.path.isabs(pf) else [os.path.join(pasta_ficha, pf), os.path.join(RAIZ, pf)]
    bases += [pasta_ficha, RAIZ]
    bases = [b for i, b in enumerate(bases) if os.path.isdir(b) and b not in bases[:i]]

    limpo = bool(ficha.get("limpo"))  # sem olho de série, contador e @ no pé: só logo, texto e "arraste"
    handle = "" if limpo else (ficha.get("handle") or marca.get("handle") or "")
    serie = ficha.get("serie") or marca.get("serie") or ""
    seta = ficha.get("seta", marca.get("seta", "arraste"))
    motivos = marca.get("motivos") or {}
    estado = {"fotos_ok": {}, "copiar": {}, "avisos": avisos, "bases_foto": bases}
    html_slides = []
    fundo = "escuro"  # o primeiro interno depois da capa é escuro; alterna
    for i, s in enumerate(slides, 1):
        lay = s.get("layout")
        if lay not in LAYOUTS: raise SystemExit(f"slide {i}: layout {lay!r} não existe. Use: {', '.join(LAYOUTS)}")
        if lay not in SEM_ALTERNANCIA:
            fundo = s.get("fundo") or ("claro" if fundo == "escuro" else "escuro")
        ctx = {**estado, "handle": handle, "fundo": fundo, "ultimo": i == total, "limpo": limpo, "seta": seta,
               "motivos": motivos, "metodo": marca.get("metodo") or [],
               "cab": cab(logo, serie, i, total, ficha.get("edicao"), limpo), "pe": pe(handle, i == total, seta),
               "halftone": '<div class="halftone"></div>' if motivos.get("halftone") and fundo == "escuro" else "",
               "halftone_capa": '<div class="halftone"></div>' if motivos.get("halftone") else ""}
        h = LAYOUTS[lay](s, ctx)
        if s.get("recorte"): h = com_recorte(h, s["recorte"], ctx)
        html_slides.append(h)
        n = contar(s)
        if n > 60: avisos.append(f"slide {i:02d} ({lay}): {n} palavras — o modelo pede no máximo 60")

    for nome_arq, src in estado["copiar"].items():
        dst = os.path.join(saida, nome_arq)
        if os.path.abspath(src) != os.path.abspath(dst): shutil.copy(src, dst)

    link_fontes, _, _ = fontes_marca(marca)
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{esc(nome)} · {esc(ficha.get('slug', 'carrossel'))}</title>
{link_fontes}
<link rel="stylesheet" href="modelo.css">{css_marca(marca)}</head><body{corpo_cls}>{''.join(html_slides)}</body></html>"""
    dest = os.path.join(saida, "carrossel.html")
    io.open(dest, "w", encoding="utf-8").write(doc)
    print(f"HTML: {os.path.relpath(dest, RAIZ)} ({total} slides)")
    for a in avisos: print("  aviso:", a)
    return dest


def previa(pasta_png, destino, colunas=5, largura=270):
    """Folha de contato: todos os slides em miniatura numa imagem só, pra conferir o ritmo do carrossel."""
    try:
        from PIL import Image
    except ImportError:
        print("  (sem Pillow: pulei a folha de contato. Instale com  py -m pip install pillow)")
        return
    pngs = sorted(f for f in os.listdir(pasta_png) if re.fullmatch(r"slide-\d+\.png", f))
    if not pngs: return
    alt = round(largura * 1350 / 1080); gap = 16
    col = min(colunas, len(pngs)); lin = math.ceil(len(pngs) / col)
    folha = Image.new("RGB", (col * largura + (col + 1) * gap, lin * alt + (lin + 1) * gap), (23, 26, 34))
    for k, f in enumerate(pngs):
        im = Image.open(os.path.join(pasta_png, f)).convert("RGB").resize((largura, alt), Image.LANCZOS)
        folha.paste(im, (gap + (k % col) * (largura + gap), gap + (k // col) * (alt + gap)))
    folha.save(destino)
    print(f"Prévia: {os.path.relpath(destino, RAIZ)}")


def main():
    ap = argparse.ArgumentParser(description="Ficha YAML → carrossel.html (+ PNGs com --render)")
    ap.add_argument("ficha"); ap.add_argument("--saida", help="pasta de saída (padrão: a pasta da ficha)")
    ap.add_argument("--render", action="store_true", help="renderiza os PNGs 1080x1350 e a folha de contato")
    ap.add_argument("--marca", help="outro YAML de marca (padrão: identidade/marca-visual.yaml)")
    a = ap.parse_args()
    ficha = yaml.safe_load(io.open(a.ficha, encoding="utf-8"))
    pasta_ficha = os.path.dirname(os.path.abspath(a.ficha))
    saida = os.path.abspath(a.saida) if a.saida else pasta_ficha
    caminho_marca = os.path.abspath(a.marca) if a.marca else (os.path.join(pasta_ficha, ficha["marca"]) if ficha.get("marca") else MARCA_PADRAO)
    dest = gerar(ficha, saida, pasta_ficha, caminho_marca)
    if a.render:
        if not os.path.isdir(os.path.join(RAIZ, "node_modules", "playwright")):
            sys.exit("Falta o Playwright. Rode uma vez na raiz do projeto:  npm run setup")
        pasta_png = os.path.join(saida, "instagram")
        r = subprocess.run(["node", os.path.join(RAIZ, "scripts", "render-carrossel.js"), dest, pasta_png], cwd=RAIZ,
                           env={**os.environ, "NODE_PATH": os.path.join(RAIZ, "node_modules")})
        if r.returncode == 0: previa(pasta_png, os.path.join(saida, "_previa.png"))
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
