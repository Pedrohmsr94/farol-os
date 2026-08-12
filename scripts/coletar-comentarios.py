"""
Coleta comentarios reais do YouTube sobre um tema e monta um corpus de linguagem
do publico — a materia-prima que o /radar nao consegue capturar sozinho.

Usado pela skill /investigar (modo comentarios).

    python scripts/coletar-comentarios.py --busca "nao consigo pagar meu contador"
    python scripts/coletar-comentarios.py --url https://youtube.com/watch?v=XXXX
    python scripts/coletar-comentarios.py --busca "abri empresa e me arrependi" --min-chars 60

Saida: pesquisa/investigacoes/comentarios/<slug>-<AAAA-MM-DD>.md

Nao transcreve nem baixa video: so metadados e comentarios. Requer yt-dlp
(pip install yt-dlp).

O vocabulario concreto do nicho vem de pesquisa/vocabulario.md, ou de --concreto.
Sem nenhum dos dois o script roda, mas a ordenacao fica pior.
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ruido tipico de secao de comentarios: elogio curto, saudacao, agradecimento.
# Nao carregam linguagem util e poluem o corpus. Vale pra qualquer nicho.
RUIDO = re.compile(
    r"^(muito bom|otimo|ótimo|excelente|parabens|parabéns|obrigado|obrigada|"
    r"boa tarde|bom dia|boa noite|top|show|perfeito|gratidao|gratidão|"
    r"adorei|amei|sensacional|maravilhoso|de acordo|isso mesmo|exato)\b",
    re.IGNORECASE,
)

# Ordenar por curtidas parece obvio e e uma armadilha: o YouTube premia indignacao,
# entao o topo enche de briga politica e moralismo. O que presta pro nosso uso e
# relato em primeira pessoa sobre a propria situacao. Vale pra qualquer nicho.
EXPERIENCIA = re.compile(
    r"\b(meu|minha|eu |perdi|estou|tou|tô|fiquei|tenho|passei|paguei|devo|"
    r"comprei|vendi|contratei|abri|fechei|meu pai|meu socio|meu sócio|"
    r"meu vizinho|meu irmao|meu irmão|aconteceu comigo|no meu caso|sofri|consegui)\b",
    re.IGNORECASE,
)

POLITICA = re.compile(
    r"\b(lula|bolsonaro|trump|governo|politico|político|politica|política|"
    r"esquerda|direita|comunista|petista|\bpt\b|ladrao|ladrão|corrupcao|"
    r"corrupção|eleicao|eleição|voto|votar|presidente)\b",
    re.IGNORECASE,
)


def raiz_projeto() -> Path:
    return Path(__file__).resolve().parent.parent


def carregar_vocabulario(extra: list[str] | None) -> tuple[re.Pattern | None, str]:
    """Monta o regex de vocabulario concreto do nicho.

    Le pesquisa/vocabulario.md (linhas que comecam com '-') e junta com --concreto.
    """
    palavras: list[str] = []
    origem = "nenhuma"

    arquivo = raiz_projeto() / "pesquisa" / "vocabulario.md"
    if arquivo.exists():
        for linha in arquivo.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if linha.startswith("-"):
                termo = linha.lstrip("-").strip().strip("*`")
                if termo and not termo.startswith("("):
                    palavras.append(termo)
        if palavras:
            origem = "pesquisa/vocabulario.md"

    if extra:
        palavras.extend(extra)
        origem = "--concreto" if origem == "nenhuma" else f"{origem} + --concreto"

    if not palavras:
        return None, origem

    alternativas = "|".join(re.escape(p) for p in palavras)
    return re.compile(rf"\b({alternativas})\b", re.IGNORECASE), origem


def sinal(texto: str, curtidas: int, concreto: re.Pattern | None) -> int:
    """Quanto esse comentario serve como materia-prima de linguagem do publico."""
    s = 0
    if EXPERIENCIA.search(texto):
        s += 6
    if concreto:
        s += min(len(concreto.findall(texto)), 4) * 2
    if POLITICA.search(texto):
        s -= 10
    if len(texto) > 180:
        s += 1
    return s * 100 + min(curtidas, 99)


def slug(texto: str, limite: int = 45) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t[:limite].strip("-") or "coleta"


def rodar_ytdlp(alvo: str, destino: Path, max_comentarios: int) -> list[Path]:
    """Baixa so os metadados (com comentarios) e devolve os .info.json gerados."""
    cmd = [
        sys.executable, "-m", "yt_dlp", alvo,
        "--skip-download",
        "--write-comments",
        "--ignore-errors",
        "--no-warnings",
        "--extractor-args",
        f"youtube:comment_sort=top;max_comments={max_comentarios},all,{max_comentarios}",
        "-o", str(destino / "%(id)s"),
    ]
    subprocess.run(cmd, check=False, capture_output=True, text=True, encoding="utf-8")
    return sorted(destino.glob("*.info.json"))


def util(texto: str, min_chars: int) -> bool:
    t = texto.strip()
    return len(t) >= min_chars and not RUIDO.match(t)


def main() -> int:
    p = argparse.ArgumentParser(description="Coleta comentarios do YouTube por tema.")
    grupo = p.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--busca", nargs="+",
                       help="Um ou mais termos de busca. Use as palavras do PUBLICO "
                            "('nao consigo pagar meu contador'), nao as do especialista "
                            "('planejamento tributario') — muda tudo no que volta")
    grupo.add_argument("--url", nargs="+", help="URL(s) de video especifico")
    p.add_argument("--videos", type=int, default=5, help="Quantos videos analisar (com --busca)")
    p.add_argument("--comentarios", type=int, default=60, help="Maximo de comentarios por video")
    p.add_argument("--min-chars", type=int, default=45,
                   help="Descarta comentario menor que isso (corta elogio solto)")
    p.add_argument("--concreto", nargs="*", default=None,
                   help="Palavras concretas do nicho, alem das de pesquisa/vocabulario.md")
    args = p.parse_args()

    concreto, origem_vocab = carregar_vocabulario(args.concreto)
    if concreto is None:
        print("AVISO: sem vocabulario do nicho (pesquisa/vocabulario.md nao existe "
              "e --concreto nao foi passado). A ordenacao vai ficar pior.")
    else:
        print(f"vocabulario do nicho: {origem_vocab}")

    if args.url:
        alvos = args.url
        rotulo = "videos-escolhidos"
    else:
        alvos = [f"ytsearch{args.videos}:{termo}" for termo in args.busca]
        rotulo = args.busca[0] if len(args.busca) == 1 else f"{args.busca[0]} +{len(args.busca)-1}"

    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        arquivos: list[Path] = []
        for alvo in alvos:
            print(f"buscando: {alvo}")
            arquivos.extend(rodar_ytdlp(alvo, destino, args.comentarios))

        if not arquivos:
            print("Nada retornou. Verifique o termo, a conexao, ou rode "
                  "'python -m pip install --upgrade yt-dlp'.")
            return 1

        videos = []
        for arq in arquivos:
            try:
                d = json.loads(arq.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            brutos = d.get("comments") or []
            uteis = [c for c in brutos if util(c.get("text", ""), args.min_chars)]
            uteis.sort(
                key=lambda c: sinal(c.get("text", ""), c.get("like_count") or 0, concreto),
                reverse=True,
            )
            videos.append({
                "titulo": d.get("title", "sem titulo"),
                "canal": d.get("uploader", "-"),
                "url": d.get("webpage_url", ""),
                "views": d.get("view_count") or 0,
                "data": d.get("upload_date", ""),
                "total": len(brutos),
                "comentarios": uteis,
            })

    videos.sort(key=lambda v: len(v["comentarios"]), reverse=True)
    hoje = dt.date.today().isoformat()
    pasta = raiz_projeto() / "pesquisa" / "investigacoes" / "comentarios"
    pasta.mkdir(parents=True, exist_ok=True)
    saida = pasta / f"{slug(rotulo)}-{hoje}.md"

    total_uteis = sum(len(v["comentarios"]) for v in videos)
    total_brutos = sum(v["total"] for v in videos)

    linhas = [
        f"# Comentarios reais — {rotulo}",
        "",
        f"Coletado em {hoje} · {len(videos)} videos · "
        f"{total_uteis} comentarios uteis de {total_brutos} lidos "
        f"(descartado o que tem menos de {args.min_chars} caracteres ou e so elogio).",
        f"Vocabulario do nicho: {origem_vocab}.",
        "",
        "> Transcricao literal, sem corrigir gramatica. E assim que o publico escreve",
        "> e e por isso que serve: e a linguagem dele, nao a do especialista.",
        "",
        "> **Ordem:** relato em primeira pessoa primeiro, briga politica por ultimo —",
        "> nao por curtidas. O YouTube premia indignacao, e ordenar por curtida",
        "> enterra a dor real embaixo de discussao de eleicao.",
        "",
    ]
    for v in videos:
        if not v["comentarios"]:
            continue
        data = v["data"]
        data_fmt = f"{data[6:8]}/{data[4:6]}/{data[:4]}" if len(data) == 8 else "-"
        linhas += [
            "---", "",
            f"## {v['titulo']}",
            f"{v['canal']} · {v['views']:,} views · {data_fmt}".replace(",", "."),
            f"{v['url']}",
            "",
        ]
        for c in v["comentarios"]:
            texto = " ".join(c.get("text", "").split())
            curtidas = c.get("like_count") or 0
            marca = f" `({curtidas} curtidas)`" if curtidas else ""
            linhas.append(f"- {texto}{marca}")
        linhas.append("")

    saida.write_text("\n".join(linhas), encoding="utf-8")
    print(f"\nOK: {total_uteis} comentarios uteis de {len(videos)} videos")
    print(f"Salvo em {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
