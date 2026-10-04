"""
Reel de referência → transcrição com tempo, pronta pra ler a estrutura.

Baixa um reel público (Instagram, TikTok, YouTube Shorts — o que o yt-dlp
abrir), transcreve com faster-whisper local (offline, nada vai pra nuvem) e
escreve um markdown com metadados, transcrição marcada por segundo e o
esqueleto da análise que o /investigar preenche.

Uso:
    py scripts/reel-referencia.py <url ou arquivo.mp4> [--slug nome]
                                 [--modelo small] [--cookies chrome]

    --cookies chrome   quando o Instagram bloquear o download anônimo, usa a
                       sessão do navegador (yt-dlp --cookies-from-browser).
                       Chrome aberto trava o arquivo de cookies no Windows:
                       fechar o navegador antes, ou usar edge/firefox

Saída: pesquisa/investigacoes/reels/<slug>/
    video.mp4          o reel (matéria-prima interna, não republicar; fora do git)
    meta.json          o que a plataforma devolveu (views, curtidas, duração…)
    transcricao.md     transcrição por tempo + esqueleto da análise

Requer: py -m pip install yt-dlp faster-whisper. O yt-dlp é chamado como módulo
do mesmo Python (sys.executable -m yt_dlp), então não precisa estar no PATH.
Pra juntar vídeo e áudio de algumas plataformas o yt-dlp usa ffmpeg. Na primeira
vez o faster-whisper baixa o modelo (~500 MB no small); depois roda offline.

Regras que o arquivo já carrega:
  - concorrente direto não entra pelo nome — o script grava o @ em meta.json,
    e quem escreve a análise decide se cita ou descreve ("escritório da região")
  - analisar, nunca copiar: o produto é padrão de gancho e estrutura, não frase
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "pesquisa", "investigacoes", "reels")


def slugificar(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^\w\s-]", "", texto).strip().lower()
    return re.sub(r"[\s_]+", "-", texto)[:60] or "reel"


def slug_da_url(url):
    m = re.search(r"/(reel|reels|p|video|shorts)/([A-Za-z0-9_-]+)", url)
    if m:
        return m.group(2)
    return slugificar(url.rstrip("/").rsplit("/", 1)[-1])


def baixar(url, pasta, cookies):
    cmd = [sys.executable, "-m", "yt_dlp", url,
           "-o", os.path.join(pasta, "video.%(ext)s"),
           "--no-warnings", "--no-playlist", "--print-json",
           "-f", "mp4/best", "--merge-output-format", "mp4"]
    if cookies:
        cmd += ["--cookies-from-browser", cookies]
    print("baixando…", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stderr.strip()[-800:])
        sys.exit("\ndownload falhou. Se for Instagram: tentar de novo com --cookies chrome "
                 "(ou edge/firefox), ou baixar o arquivo na mão e passar o .mp4 no lugar da URL.")
    meta = {}
    for linha in r.stdout.splitlines():
        if linha.startswith("{"):
            try:
                meta = json.loads(linha)
            except json.JSONDecodeError:
                pass
    campos = ("id", "title", "description", "uploader", "uploader_id", "channel",
              "duration", "view_count", "like_count", "comment_count", "repost_count",
              "upload_date", "webpage_url", "extractor")
    meta = {k: meta.get(k) for k in campos if meta.get(k) is not None}
    for nome in sorted(os.listdir(pasta)):
        # resto de download interrompido (.part, .ytdl) não é vídeo
        if nome.startswith("video.") and not nome.endswith((".part", ".ytdl", ".json")):
            return os.path.join(pasta, nome), meta
    sys.exit("download terminou sem arquivo de vídeo")


def transcrever(caminho, modelo):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper não instalado: py -m pip install faster-whisper")
    try:
        import torch
        gpu = torch.cuda.is_available()
    except ImportError:
        gpu = False
    print(f"transcrevendo com {modelo} ({'gpu' if gpu else 'cpu'})…", flush=True)
    m = WhisperModel(modelo, device="cuda" if gpu else "cpu",
                     compute_type="float16" if gpu else "int8",
                     cpu_threads=os.cpu_count())
    segmentos, info = m.transcribe(caminho, language="pt", vad_filter=True,
                                   condition_on_previous_text=False)
    saida = []
    for s in segmentos:
        saida.append((s.start, s.end, s.text.strip()))
    return saida, info.duration


def mmss(seg):
    return f"{int(seg // 60):02d}:{int(seg % 60):02d}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("origem", help="URL do reel ou caminho de um .mp4 local")
    p.add_argument("--slug")
    p.add_argument("--modelo", default="small")
    p.add_argument("--cookies", help="chrome | edge | firefox")
    args = p.parse_args()

    eh_url = args.origem.startswith("http")
    slug = args.slug or (slug_da_url(args.origem) if eh_url
                         else slugificar(os.path.splitext(os.path.basename(args.origem))[0]))
    pasta = os.path.join(SAIDA, slug)
    os.makedirs(pasta, exist_ok=True)

    if eh_url:
        video, meta = baixar(args.origem, pasta, args.cookies)
    else:
        if not os.path.isfile(args.origem):
            sys.exit(f"arquivo não encontrado: {args.origem}")
        video = os.path.join(pasta, "video" + os.path.splitext(args.origem)[1])
        shutil.copy(args.origem, video)
        meta = {"origem": "arquivo local", "arquivo": os.path.basename(args.origem)}

    with open(os.path.join(pasta, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    segs, duracao = transcrever(video, args.modelo)
    palavras = sum(len(t.split()) for _, _, t in segs)

    L = [f"# Reel de referência — {slug}\n",
         f"Coletado em {date.today().isoformat()} por `scripts/reel-referencia.py`. "
         f"Matéria-prima interna: não republicar, não citar autor no conteúdo.\n",
         "## Ficha\n"]
    L.append(f"- Origem: {meta.get('webpage_url') or meta.get('arquivo') or args.origem}")
    if meta.get("uploader") or meta.get("channel"):
        L.append(f"- Conta: {meta.get('uploader') or meta.get('channel')} "
                 f"(se for concorrente direto, não citar pelo nome na análise)")
    L.append(f"- Duração: {mmss(duracao)} · {palavras} palavras faladas "
             f"({palavras / max(duracao, 1) * 60:.0f} palavras/min)")
    for rot, chave in (("Views", "view_count"), ("Curtidas", "like_count"),
                       ("Comentários", "comment_count"), ("Compartilhamentos", "repost_count")):
        if meta.get(chave) is not None:
            L.append(f"- {rot}: {meta[chave]:,}".replace(",", "."))
    if meta.get("upload_date"):
        d = meta["upload_date"]
        L.append(f"- Publicado: {d[6:8]}/{d[4:6]}/{d[:4]}")
    if meta.get("description"):
        L.append(f"- Legenda: {meta['description'][:300].strip()}")

    L.append("\n## Transcrição por tempo\n")
    for ini, fim, texto in segs:
        L.append(f"`{mmss(ini)}–{mmss(fim)}` {texto}")

    L.append("""
## Análise — preencher (`/investigar`)

**Gancho (0–3s):** o que é dito, literalmente, e que mecanismo usa — número,
contradição, pergunta do público, cena, confissão. O gancho segura ou o vídeo
morre aqui.

**Estrutura por bloco de tempo:** onde muda de assunto, quanto dura cada bloco,
o que vem primeiro (fato ou implicação). Comparar com o molde do `/angulos`:
0–3 gancho · 3–10 fato · 10–35 desenvolvimento · 35–50 implicação · 50–60 fecho.

**Ritmo:** palavras por minuto, tamanho de frase, pausa. Texto na tela?

**Por que funcionou (hipótese, com a evidência):** views/curtidas/comentários da
ficha contra a mediana da conta de origem, não contra número absoluto.

**O que serve pra essa marca:** o padrão estrutural que dá pra aplicar no ângulo X —
nunca a frase.

**O que NÃO copiar:** promessa, alarmismo, tom de guru, ataque. Se aparecer, vira
entrada em `criterios.md` do `/revisar`.
""")

    destino = os.path.join(pasta, "transcricao.md")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"\npronto: {os.path.relpath(destino, RAIZ)}  ({mmss(duracao)}, {len(segs)} trechos)")


if __name__ == "__main__":
    main()
