"""
Transcreve audio para texto com timestamp, usando faster-whisper local (offline).

Usado pela skill /transcrever.

    py scripts/transcrever.py <entrada> [--saida _memoria/fontes] [--data AAAA-MM-DD] [--modelo small]
    py scripts/transcrever.py "C:\\Users\\voce\\Downloads\\reuniao-kickoff.m4a" --data 2026-10-01

<entrada> pode ser um arquivo de audio ou uma pasta (varre m4a/mp3/ogg/wav/opus/mp4/webm).

Saida: <saida>/<data>-<slug-do-arquivo>.md — padrao _memoria/fontes/, que e onde
mora o dump bruto do repo. --data e a data da conversa (padrao: hoje). Nunca
sobrescreve: se o arquivo ja existe, ganha sufixo -2, -3...

O audio NAO entra no repo: fica onde estava (Downloads, pasta fora do projeto).
O .gitignore barra m4a/mp3/wav/ogg/opus por garantia.

Requer: py -m pip install faster-whisper. Na primeira vez baixa o modelo (~500 MB
no small); depois roda offline. Arquivo de video (mp4/webm) precisa de ffmpeg.

Notas de implementacao:
  - Varre a pasta com glob em vez de casar nome literal: arquivo vindo de zip
    no Windows costuma ter acentuacao em Unicode decomposto (a + til separado),
    o que quebra comparacao de string.
  - Escreve e da flush linha a linha, entao a transcricao parcial ja e legivel
    se o processo for interrompido.
  - vad_filter pula silencio (acelera bastante em reuniao com pausa).
  - condition_on_previous_text=False evita que um erro contamine o resto.
"""

import argparse
import datetime as dt
import glob
import os
import re
import sys
import time
import unicodedata

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTENSOES = ("m4a", "mp3", "ogg", "wav", "opus", "mp4", "webm")


def slugificar(nome):
    base = os.path.splitext(os.path.basename(nome))[0]
    base = unicodedata.normalize("NFKD", base)
    base = base.encode("ascii", "ignore").decode("ascii")
    base = re.sub(r"[^\w\s-]", "", base).strip().lower()
    return re.sub(r"[\s_]+", "-", base) or "audio"


def coletar(entrada):
    if os.path.isfile(entrada):
        return [entrada]
    encontrados = []
    for ext in EXTENSOES:
        encontrados += glob.glob(os.path.join(entrada, f"*.{ext}"))
    return sorted(encontrados)


def destino_livre(pasta, nome):
    caminho = os.path.join(pasta, nome + ".md")
    n = 2
    while os.path.exists(caminho):
        caminho = os.path.join(pasta, f"{nome}-{n}.md")
        n += 1
    return caminho


def main():
    p = argparse.ArgumentParser(description="Transcreve audio local com faster-whisper.")
    p.add_argument("entrada", help="arquivo de audio ou pasta")
    p.add_argument("--saida", default=os.path.join(RAIZ, "_memoria", "fontes"),
                   help="pasta onde salvar (padrao: _memoria/fontes/)")
    p.add_argument("--data", default=dt.date.today().isoformat(),
                   help="data da conversa, AAAA-MM-DD (padrao: hoje)")
    p.add_argument("--modelo", default="small",
                   help="tiny | base | small | medium | large-v3 (padrao: small)")
    args = p.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.data):
        sys.exit(f"--data invalida: {args.data} (usar AAAA-MM-DD)")

    arquivos = coletar(args.entrada)
    if not arquivos:
        print(f"nenhum audio encontrado em: {args.entrada}")
        sys.exit(1)

    os.makedirs(args.saida, exist_ok=True)
    print(f"arquivos: {[os.path.basename(a) for a in arquivos]}", flush=True)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper nao instalado: py -m pip install faster-whisper")

    try:
        import torch
        tem_gpu = torch.cuda.is_available()
    except ImportError:
        tem_gpu = False

    device = "cuda" if tem_gpu else "cpu"
    compute = "float16" if tem_gpu else "int8"
    print(f"carregando modelo {args.modelo} em {device}/{compute}...", flush=True)
    model = WhisperModel(args.modelo, device=device, compute_type=compute,
                         cpu_threads=os.cpu_count())

    for src in arquivos:
        t0 = time.time()
        destino = destino_livre(args.saida, f"{args.data}-{slugificar(src)}")
        print(f"\n=== {os.path.basename(src)} -> {os.path.basename(destino)} ===", flush=True)

        segments, info = model.transcribe(
            src,
            language="pt",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            condition_on_previous_text=False,
        )

        with open(destino, "w", encoding="utf-8") as f:
            f.write(f"# Transcricao bruta — {os.path.basename(src)}\n\n")
            f.write(f"- Data da conversa: {args.data}\n")
            f.write(f"- Duracao: {info.duration/60:.1f} min · modelo: {args.modelo}"
                    f" · gerado automaticamente (Whisper local)\n")
            f.write("- **Rascunho.** Nome proprio, numero e termo tecnico precisam de"
                    " conferencia humana. O Whisper nao separa quem fala.\n\n")
            ultimo_aviso = -120
            for seg in segments:
                m, s = divmod(int(seg.start), 60)
                f.write(f"[{m:02d}:{s:02d}] {seg.text.strip()}\n\n")
                f.flush()
                if seg.start - ultimo_aviso >= 120:
                    ultimo_aviso = seg.start
                    print(f"  ... {m:02d}:{s:02d}", flush=True)

        print(f"OK ({time.time() - t0:.0f}s) -> {os.path.relpath(destino, RAIZ)}", flush=True)

    print("\nTRANSCRICAO CONCLUIDA", flush=True)


if __name__ == "__main__":
    main()
