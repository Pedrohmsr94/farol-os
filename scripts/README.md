# Scripts

| Script | O que faz | Precisa |
|---|---|---|
| `carrossel/gerar.py` | monta o `carrossel.html` da peça a partir do roteiro, com a marca de `identidade/` | `pyyaml` |
| `carrossel/modelo.css` | o desenho do carrossel. Cor e fonte vêm da marca, não daqui | — |
| `render-carrossel.js` | transforma o `carrossel.html` em PNGs 4:5, 1:1 ou 9:16 | `npm run setup` |
| `gerar-imagem.js` | gera imagem por IA pra fundo e cena genérica | `OPENAI_API_KEY` |
| `coletar-comentarios.py` | corpus de comentário real do YouTube, ordenado por relato em 1ª pessoa | `yt-dlp` |
| `reel-referencia.py` | baixa um reel, transcreve por tempo e deixa o esqueleto da análise | `yt-dlp`, `faster-whisper` |
| `perfil-de-desempenho.py` | o placar da própria conta: alcance, salvamento e abertura por formato | `META_ACCESS_TOKEN`, `META_IG_ACCOUNT_ID` |
| `transcrever.py` | áudio de reunião → texto com `[MM:SS]` em `_memoria/fontes/`, offline | `faster-whisper` |
| `coletores/` | números de perfil público e posts de referência (Playwright e Apify) | ver `coletores/README.md` |
| `radar-diario.ps1` · `agendar-radar.ps1` | roda o `/radar` sozinho, todo dia útil | Claude Code no PATH |

## Setup (uma vez por máquina)

Cada parte só precisa ser instalada se for usada.

**Node** — Playwright e o navegador que renderiza os PNGs e roda os coletores:

```powershell
npm run setup
```

**Python** — yt-dlp, faster-whisper, Pillow e PyYAML:

```powershell
py -m pip install -r requirements.txt
```

**ffmpeg** — quadros dos vídeos de referência e áudio de arquivo de vídeo:

```powershell
winget install Gyan.FFmpeg
```

Reabrir o terminal depois, pro PATH novo valer.

**Chaves de API** (opcional) — copiar `.env.exemplo` pra `.env` e preencher.
O `.env` está no `.gitignore` e nunca sobe. Todo script lê a chave da variável de
ambiente primeiro e do `.env` da raiz depois.

---

## Renderizar carrossel

```powershell
npm run carrossel -- conteudo/fila/2026-09-03-malha-fina
npm run carrossel -- conteudo/fila/2026-09-03-malha-fina --formato 9:16
```

Lê o `carrossel.html` da pasta e salva `slide-01.png`, `slide-02.png`... em
`instagram/` (ou `stories/` no 9:16).

Formatos: `4:5` (1080×1350, padrão) · `1:1` (1080×1080) · `9:16` (1080×1920).

**Um script pro projeto inteiro.** Não copiar pra dentro de cada pasta de peça —
quando o layout mudar, muda aqui e vale pras próximas.

## Gerar imagem por IA

```powershell
node scripts/gerar-imagem.js "PROMPT EM INGLES" conteudo/fila/<pasta>/foto-capa.png
```

Precisa de `OPENAI_API_KEY` no `.env`. Custa por imagem.

Foto real da empresa vem sempre na frente. Imagem gerada serve pra fundo, textura
e cena genérica — nunca pra fingir equipe, cliente ou resultado.

## Coletar comentários do YouTube

```powershell
py scripts/coletar-comentarios.py --busca "as palavras do publico" --videos 6
```

Ver a skill `/investigar`, modo `comentarios` — a escolha das palavras de busca é
o que decide se volta material ou lixo.

## Ler um reel de referência

```powershell
py scripts/reel-referencia.py https://www.instagram.com/reel/XXXX/
py scripts/reel-referencia.py https://www.instagram.com/reel/XXXX/ --cookies chrome
py scripts/reel-referencia.py C:\caminho\video.mp4 --slug gancho-numero
```

Sai em `pesquisa/investigacoes/reels/<slug>/`: `meta.json`, `transcricao.md` com
o esqueleto da análise (gancho, estrutura por tempo, ritmo, o que não copiar) e o
`video.mp4`, que fica fora do git. Instagram costuma barrar download anônimo:
`--cookies chrome` usa a sessão do navegador (fechar o Chrome antes), ou
`edge`/`firefox`. Analisar, nunca copiar.

## Placar da própria conta

```powershell
py scripts/perfil-de-desempenho.py --posts 40
py scripts/perfil-de-desempenho.py --posts 40 --excluir 17900000000000001,17900000000000002
```

Lê os últimos posts pela Graph API e escreve, em `pesquisa/investigacoes/desempenho/`,
a leitura datada (`perfil-AAAA-MM-DD.md` + `.json`) e a cópia mais recente
(`perfil-de-desempenho.md`, que o `/revisar`, o `/semana` e o `/relatorio` leem).
Post impulsionado vai em `--excluir` — a API não separa alcance pago do orgânico.
Métrica que a API não devolve fica `-`, nunca estimada. Rodar uma vez por mês.

## Transcrever reunião

```powershell
py scripts/transcrever.py "C:\Users\voce\Downloads\kickoff.m4a" --data 2026-10-01
```

Ver a skill `/transcrever` — transcrever é o meio; o que importa é a leitura e as
perguntas depois. O áudio fica fora do repo.

## Coletores

Ver `coletores/README.md`: tabela dos coletores, regras e o caminho do dado
(coleta → mídia no mesmo dia → fichas → padrões).

---

## Radar automático

Faz o `/radar` rodar sozinho, sem ninguém na frente. Todo dia útil o briefing de
pautas aparece em `pesquisa/radar/`, pronto pra abrir.

**Antes de agendar, duas condições:**

1. `pesquisa/fontes.md` precisa existir — a primeira rodada do `/radar` na mão é
   que monta o mapa de fontes do nicho. O script se recusa a rodar sem isso
2. Pelo menos **duas rodadas na mão aprovadas** pelo operador. Radar automático em
   cima de fontes erradas produz lixo todo dia, com pontualidade

**Agendar:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\agendar-radar.ps1
```

Pergunta o horário e cria a tarefa no Agendador do Windows: de segunda a sexta,
no horário escolhido. Se a máquina estiver desligada na hora, roda assim que
ligar. Não precisa de administrador.

**Testar sem esperar:**

```powershell
Start-ScheduledTask -TaskName "Farol OS - Radar <nome-da-pasta>"
```

**Rodar na mão:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\radar-diario.ps1
```

**Desagendar:**

```powershell
Unregister-ScheduledTask -TaskName "Farol OS - Radar <nome-da-pasta>" -Confirm:$false
```

## Frequência

Escolher pelo ritmo do setor, não pelo hábito:

| Setor | Frequência |
|---|---|
| Muda toda hora — tributário, crédito, jurídico, câmbio | diário |
| Ciclo mensal — varejo, serviço local, saúde | 2 a 3 vezes por semana |
| Ciclo lento — indústria, B2B de contrato longo | semanal |

Diário num setor parado gera briefing vazio, e briefing vazio treina o operador a
não abrir mais o arquivo. Aí a automação inteira vira ruído.

## Log

Cada rodada escreve em `pesquisa/radar/_log/AAAA-MM-DD.log`.

O script julga pela **entrega, não pelo código de saída**: se o briefing foi
gerado, a rodada é OK mesmo que o Claude tenha saído com erro no fim (acontece ao
bater limite de uso com o arquivo já salvo). Sem briefing na pasta é que é falha.

## Um detalhe que quebra tudo

Os `.ps1` são **ASCII puro**, sem acento e sem travessão, de propósito. O
PowerShell 5.1 lê arquivo sem BOM como ANSI, o travessão vira aspas curvas, e o
parser trata como fim de string. Ao editar, manter assim.
