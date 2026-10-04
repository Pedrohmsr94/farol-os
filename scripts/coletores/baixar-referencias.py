# -*- coding: utf-8 -*-
"""Baixa a mídia dos posts coletados pelo Apify — capa, slides e vídeo.

    py scripts/coletores/baixar-referencias.py --json pesquisa/coleta/raw/<nome>.json [--saida <pasta>]

Os links do CDN do Instagram expiram em poucos dias: rodar NO MESMO DIA da coleta.
Pra cada post: a capa (displayUrl), os slides (images, se carrossel) e o vídeo (videoUrl).
Vídeos ganham quadros com ffmpeg (1 s, 3 s, 1/3, 2/3 e final) pra leitura visual —
sem ffmpeg no PATH, o vídeo baixa e os quadros ficam de fora (o script avisa).

Saída padrão: pesquisa/referencias/midia/<owner>--<shortCode>/{capa.jpg, slide-01.jpg…, video.mp4, frame-*.jpg}
e pesquisa/referencias/coleta/indice-midia-<nome>.json com o que baixou.
A mídia é matéria-prima interna: fica fora do git (ver .gitignore). O índice entra.
"""
import argparse, io, json, os, shutil, subprocess, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TEM_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))

def baixar(url, caminho):
    if os.path.exists(caminho) and os.path.getsize(caminho) > 1000:
        return "cache"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            dados = r.read()
        with open(caminho, "wb") as f:
            f.write(dados)
        return "ok"
    except Exception as e:
        return f"erro: {type(e).__name__}"

def duracao(video):
    if not TEM_FFMPEG:
        return None
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", video], capture_output=True, text=True, timeout=60)
        return float(out.stdout.strip())
    except Exception:
        return None

def quadros(video, pasta):
    d = duracao(video)
    if not d:
        return []
    pontos = [("01-gancho", min(1.0, d/2)), ("02-3s", min(3.0, d*0.9)), ("03-terco", d/3), ("04-dois-tercos", 2*d/3), ("05-fim", max(d-1.5, 0))]
    feitos = []
    for nome, t in pontos:
        alvo = os.path.join(pasta, f"frame-{nome}.jpg")
        if os.path.exists(alvo):
            feitos.append(alvo); continue
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", "-q:v", "3", "-vf", "scale=540:-2", alvo],
                           capture_output=True, timeout=120)
        if r.returncode == 0 and os.path.exists(alvo):
            feitos.append(alvo)
    return feitos

def main():
    p = argparse.ArgumentParser(description="Baixa a mídia dos posts de um JSON do Apify.")
    p.add_argument("--json", required=True, help="JSON cru do apify.py (pesquisa/coleta/raw/<nome>.json)")
    p.add_argument("--saida", default=os.path.join(RAIZ, "pesquisa", "referencias", "midia"),
                   help="pasta da mídia (padrão: pesquisa/referencias/midia/, fora do git)")
    a = p.parse_args()
    if not os.path.exists(a.json):
        raise SystemExit(f"JSON não encontrado: {a.json}")
    itens = json.load(io.open(a.json, encoding="utf-8"))["itens"]
    os.makedirs(a.saida, exist_ok=True)
    if not TEM_FFMPEG:
        print("AVISO: ffmpeg/ffprobe fora do PATH — vídeos baixam, mas sem quadros. "
              "Instalar: winget install Gyan.FFmpeg (e reabrir o terminal).\n")
    indice = []; falhas = 0
    for i, it in enumerate(itens, 1):
        if it.get("error"):
            indice.append({"shortCode": it.get("shortCode"), "inputUrl": it.get("inputUrl"), "erro": it.get("error")}); continue
        code = it.get("shortCode") or f"item{i:03d}"; owner = it.get("ownerUsername") or "desconhecido"
        pasta = os.path.join(a.saida, f"{owner}--{code}"); os.makedirs(pasta, exist_ok=True)
        reg = {"shortCode": code, "owner": owner, "type": it.get("type"), "url": it.get("url"),
               "pasta": os.path.relpath(pasta, RAIZ).replace("\\", "/"), "capa": None, "slides": [],
               "video": None, "frames": [], "duracao": it.get("videoDuration")}
        if it.get("displayUrl"):
            r = baixar(it["displayUrl"], os.path.join(pasta, "capa.jpg")); reg["capa"] = "capa.jpg" if r in ("ok", "cache") else None
            if r.startswith("erro"): falhas += 1
        for n, url in enumerate(it.get("images") or [], 1):
            r = baixar(url, os.path.join(pasta, f"slide-{n:02d}.jpg"))
            if r in ("ok", "cache"): reg["slides"].append(f"slide-{n:02d}.jpg")
            else: falhas += 1
        if it.get("videoUrl"):
            v = os.path.join(pasta, "video.mp4"); r = baixar(it["videoUrl"], v)
            if r in ("ok", "cache"):
                reg["video"] = "video.mp4"; reg["duracao"] = reg["duracao"] or duracao(v)
                reg["frames"] = [os.path.basename(x) for x in quadros(v, pasta)]
            else: falhas += 1
        indice.append(reg)
        print(f"{i:2d}/{len(itens)} @{owner:26s} {code} {str(it.get('type')):7s} capa={'ok' if reg['capa'] else '--'} slides={len(reg['slides'])} video={'ok' if reg['video'] else '--'} frames={len(reg['frames'])}")
    pasta_indice = os.path.join(os.path.dirname(os.path.abspath(a.saida)), "coleta")
    os.makedirs(pasta_indice, exist_ok=True)
    nome = os.path.splitext(os.path.basename(a.json))[0]
    dest = os.path.join(pasta_indice, f"indice-midia-{nome}.json")
    json.dump(indice, io.open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(indice)} posts · falhas de download: {falhas} · índice: {os.path.relpath(dest, RAIZ)}")
    if falhas:
        print("Falha em massa costuma ser link expirado: coletar de novo e baixar no mesmo dia.")

if __name__ == "__main__":
    main()
