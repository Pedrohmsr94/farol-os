# Scripts

## Setup (uma vez por cliente)

Só precisa se for usar carrossel ou coleta de comentários.

**Carrossel** — instala o Playwright e o navegador que renderiza os PNGs:

```powershell
npm run setup
```

**Coleta de comentários** — instala o yt-dlp:

```powershell
pip install yt-dlp
```

**Chaves de API** (opcional) — copiar `.env.exemplo` pra `.env` e preencher.
O `.env` está no `.gitignore` e nunca sobe.

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
python scripts/coletar-comentarios.py --busca "as palavras do publico" --videos 6
```

Ver a skill `/investigar`, modo `comentarios` — a escolha das palavras de busca é
o que decide se volta material ou lixo.

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
