---
name: transcrever
description: >
  Transcreve áudio de reunião, ligação, entrevista ou áudio de WhatsApp para texto com timestamp,
  usando Whisper local (offline, sem enviar nada pra nuvem). Depois lê a transcrição, extrai o que
  importa pro marketing da empresa e pergunta o que ficou ambíguo. Use quando o operador disser
  "transcreve esse áudio", "subi a gravação da reunião", "/transcrever", ou quando ele mandar
  arquivo .m4a, .mp3, .ogg, .wav ou um zip com áudio dentro.
---

# /transcrever — Áudio de reunião para contexto

Transcrever é meio, não fim. O objetivo é transformar uma conversa gravada em
contexto confiável sobre a empresa e a voz dela. A transcrição automática
**sempre** erra nome próprio, número e termo técnico — por isso a etapa de
perguntar não é opcional.

Uma reunião gravada com o dono é a melhor fonte de voz que existe. É daqui que
o `/marca` e o `/investigar` (modo voz) tiram como a empresa fala de verdade.

## Antes de começar

Se o operador mandou um **zip**, extrair primeiro, para uma pasta temporária
fora do projeto. Atenção: nomes vindos de zip (principalmente do WeTransfer no
Windows) podem vir em Unicode decomposto — `Reunião` com o til como caractere
separado. **Nunca casar nome de arquivo por string literal; sempre varrer a
pasta com glob.** O script já faz isso.

## Passo 1 — Levantar o que tem

Listar os áudios e medir a duração de cada um antes de qualquer coisa:

```powershell
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<arquivo>"
```

Informar ao operador o que encontrou e a estimativa de tempo. Referência de
CPU sem GPU, com `faster-whisper` e modelo `small`: **cerca de 4x tempo real**
(50 min de áudio ≈ 13 min de processamento).

Sem `ffprobe`, seguir mesmo assim — o script informa a duração no fim.

## Passo 2 — Garantir as ferramentas

```powershell
py -c "import faster_whisper"
```

Se der erro: `py -m pip install faster-whisper` (ou `py -m pip install -r requirements.txt`,
que instala tudo dos scripts). Na primeira execução o modelo é baixado (~500 MB
no `small`); depois roda offline.

`ffmpeg` só é obrigatório pra arquivo de vídeo (`.mp4`, `.webm`). Instalar com
`winget install Gyan.FFmpeg` e reabrir o terminal.

## Passo 3 — Escolher o modelo

| Modelo | Velocidade (CPU) | Quando usar |
|---|---|---|
| `base` | ~10x tempo real | Só pra rascunho; erra muito nome e número |
| `small` | ~4x tempo real | **Padrão.** Boa qualidade em português |
| `medium` | ~1,5x tempo real | Áudio ruim, muita gente falando, ou quando o conteúdo é crítico |

Começar com `small`. Se o resultado sair muito corrompido, oferecer reprocessar
os trechos críticos com `medium`.

## Passo 4 — Transcrever

```powershell
py scripts/transcrever.py "<arquivo ou pasta>" --data AAAA-MM-DD
```

- `--data` é a data **da conversa**, não a de hoje. Perguntar se não estiver
  óbvia no nome do arquivo
- `--modelo medium` quando o áudio for ruim
- `--saida <pasta>` só se o operador pedir outro lugar

O script escreve `[MM:SS] texto` por segmento — o timestamp é o que permite ao
operador conferir no áudio o trecho duvidoso. Grava linha a linha: se cair no
meio, a parte transcrita já está salva.

Rodar em background quando passar de ~5 minutos de áudio, e avisar o operador.

## Passo 5 — Onde fica cada coisa

- **Transcrição** → `_memoria/fontes/AAAA-MM-DD-<slug>.md` (versionada). É dump
  bruto: não reescrever, não corrigir no arquivo. O que importa sobe destilado
- **Áudio** → fica onde estava, **fora do repositório**. Nunca copiar pra dentro
  do projeto. O `.gitignore` barra `*.m4a`, `*.mp3`, `*.wav`, `*.ogg`, `*.opus`
  por garantia — conferir antes de salvar

Se o nome do arquivo de áudio for sujo (`WhatsApp Audio 2026-10-01 at 14.32.11`),
renomear a transcrição pra algo que diga o assunto: `2026-10-01-kickoff-com-dono.md`.

Conversa com dado sensível (faturamento, sócio, problema com funcionário,
opinião crua sobre o cliente) vai pra `notas/privado/`, que não sobe pro git —
usar `--saida notas/privado`.

## Passo 6 — Ler e extrair (a parte que importa)

Ler a transcrição inteira e organizar o que apareceu, por tema. O que procurar
numa conversa sobre o marketing de uma empresa:

- O que vende, o que **não** vende, e o que faz sob demanda
- Pra quem: perfil de cliente, como chega, o que mais pergunta, por que fecha
- Diferenciais — de preferência nas palavras do próprio dono
- Números: ticket, volume, prazo, sazonalidade, meta
- Concorrentes citados e o que o dono pensa deles
- Objeções que ouve de quem não fecha
- Casos e histórias concretas que podem virar conteúdo
- **Vocabulário próprio** — palavra que o dono usa e o setor não usa, expressão
  que repete, o que ele nunca falaria

## Passo 7 — Perguntar (obrigatório)

Montar uma lista **numerada, com timestamp em cada item**, separando:

1. **Nomes próprios que o Whisper provavelmente errou** — marca, produto,
   cidade, pessoa. É o erro mais comum e o mais caro, porque vai parar em post
   publicado
2. **Números que vão virar comunicação** — se o número parece inconsistente com
   o resto da conversa, dizer isso e pedir confirmação. Não publicar número
   que a pessoa chutou com hesitação
3. **Fatos que mudam o que vai ser escrito** — datas, tempo de mercado,
   o que é promessa e o que já acontece
4. **Quem falou o quê**, se a conversa tinha mais de duas pessoas. O Whisper
   **não separa falantes**. Avisar isso ao operador desde o começo

Só depois das respostas, atualizar a memória.

## Passo 8 — Atualizar a memória

Seguir o fluxo normal do Farol OS:

- Fatos da empresa (produto, preço, público, concorrente) → `_memoria/empresa.md`
- Voz, vocabulário, palavra proibida → `marca/guia-de-marca.md`
- Prioridade ou meta que mudou → `_memoria/estrategia.md`
- Combinado de trabalho (ritmo, quem aprova, canal) → `_memoria/operacao.md`
- Pergunta real de cliente que o dono repetiu → banco do `/ideias`

Mostrar ao operador o que mudou e destacar **as decisões de julgamento que ele
deve conferir** — não só listar arquivos alterados. Registrar no `indice.md`, em
"Em aberto", o que ficou sem resposta.

## Regras

- Nunca apagar o áudio original
- Nunca tratar transcrição automática como fonte literal: é rascunho até o
  operador confirmar
- Nunca inventar o que não deu pra entender — perguntar, sempre com timestamp
- Se a pessoa hesitou ao dar um número, isso é informação: relatar a hesitação
- Áudio de reunião costuma ter conteúdo sensível. Tudo local: nada sobe pra
  serviço externo de transcrição
