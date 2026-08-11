---
name: marca
description: >
  Extrai a voz da marca do cliente — como soa, pra quem fala, quais palavras usa
  e quais não usa — a partir de material real que a empresa já produziu, e escreve
  `marca/guia-de-marca.md`, que todas as skills de conteúdo leem antes de escrever.
  Use quando o usuário disser "definir a voz", "guia de marca", "tom de voz do
  cliente", "o conteúdo está saindo genérico", "/marca".
---

# /marca — A voz da empresa

Roda depois do `/diagnostico`, antes de produzir qualquer conteúdo.

Sem esse arquivo, todo texto sai com cara de qualquer empresa do mesmo setor da
mesma cidade. É o defeito mais caro do marketing terceirizado — e o motivo do
cliente dizer "não parece a gente".

Saída: `marca/guia-de-marca.md`.

---

## O princípio

**Voz não se inventa, se extrai.** A empresa já fala de algum jeito — no
WhatsApp, no atendimento, no áudio que o dono manda. O trabalho é achar esse
jeito e escrever a regra dele.

Descrição sem exemplo não calibra nada. "Tom profissional e acessível" não
serve pra escrever uma linha. Um print de como o dono responde um cliente
chateado serve pra escrever cem.

---

## Passo 1 — Pedir o material

Antes de qualquer pergunta:

> "Me manda material real da empresa, do jeito que saiu. Quanto mais cru,
> melhor:
>
> - 3 a 5 conversas de WhatsApp com cliente *(print ou copiado)*
> - legendas que a empresa já publicou
> - áudio do dono explicando o serviço — transcrito, ou o arquivo
> - texto do site, se tiver
>
> Joga em `dados/` ou `_memoria/fontes/`. Se não tiver nada disso, a gente
> extrai por conversa — mas fica mais fraco, e eu vou te dizer onde."

Se o material chegar, **ler antes de perguntar qualquer coisa**. Metade das
perguntas abaixo já vai estar respondida.

---

## Passo 2 — Extrair do material

Do que foi lido, tirar:

**Como soa.** Frase curta ou longa? Formal ou de conversa? Usa gíria da região?
Trata por "você", "vocês", "senhor"? Emoji — quais e quantos? Como começa e
como termina uma mensagem?

**Repetições.** Palavra ou expressão que aparece várias vezes. Isso é a marca
falando sem saber.

**Como explica o que vende.** A frase que o dono usa pra explicar o serviço pra
quem não é do ramo. Quase sempre é melhor que qualquer coisa que uma agência
escreveria.

**Do que ele reclama.** Quando o dono reclama do concorrente ou do mercado,
aparece o que a empresa acredita. Isso vira território de palavras.

Anotar cada achado **com a citação junto**. O guia sem exemplo é inútil.

---

## Passo 3 — Perguntar o que o material não responde

Uma por vez. Pular as que o material já respondeu.

1. "Se um cliente satisfeito descrevesse a empresa pra um amigo, o que ele
   diria? Não o que você queria que ele dissesse — o que ele realmente diz."
2. "Que jeito de falar te dá ranço? Coisa que concorrente escreve e você acha
   ridículo."
3. "Tem palavra que a empresa não usa? Termo técnico que confunde, ou palavra
   que ficou queimada no setor."
4. "Tem assunto proibido? Política, religião, concorrente pelo nome, promessa
   de resultado."
5. "O setor tem regra de publicidade? Conselho, órgão, código de ética."
6. "O que a empresa pode afirmar sem mentir? Caso real, número, tempo de
   mercado, depoimento."

A 5 e a 6 não são detalhe. Setor regulado com conteúdo errado dá multa. E marca
sem prova só consegue produzir promessa vaga.

---

## Passo 4 — Escrever o guia

Preencher `marca/guia-de-marca.md`. Como escrever cada parte:

**Em uma frase** — a frase do dono, não uma reescrita bonita dela.

**Pra quem fala** — o recorte real. E o que essa pessoa já ouviu de todo
concorrente e não acredita mais.

**Como soa** — 3 a 5 frases, cada uma amarrada num exemplo do material.
Colar o exemplo real embaixo, inteiro.

**Palavras da casa** — o que a empresa já repete naturalmente. Não inventar
vocabulário de marca; catalogar o que existe.

**Palavras proibidas** — do ranço da pergunta 2, dos termos queimados da 3.
Ser específico: "não escrever 'soluções'", não "evitar corporativês".

**Regras de escrita** — tamanho de frase, emoji, tratamento, como convida sem
soar vendedor de curso.

**Prova** — só o que se sustenta.

**Visual** — se houver. Se não, deixar em branco e avisar; não é bloqueante.

---

## Passo 5 — Testar antes de entregar

Escrever **duas legendas curtas** sobre um assunto qualquer da empresa usando o
guia, e mostrar pro operador:

> "Escrevi duas coisas usando o guia. Soa como a empresa, ou soa como agência?"

Se ele disser que não soa, o guia está errado — voltar e ajustar. Esse teste é
o que separa guia que funciona de guia que fica bonito na pasta.

---

## Passo 6 — Fechar

Marcar `**Status:** preenchido em AAAA-MM-DD` no topo do arquivo.

> "Guia pronto. Toda skill que escreve lê ele antes agora.
>
> Quando o cliente reclamar de algum texto, me fala — a correção vira linha
> nova aqui em vez de virar retrabalho toda vez."

---

## Regras

- **Extrair, não inventar.** Nenhuma característica de voz entra sem exemplo do
  material ou fala do cliente
- **Nunca preencher com genérico.** "Profissional e acessível", "próximo e
  humano", "leve e descontraído" — são ausência de voz. Se não deu pra extrair,
  escrever "não extraído — falta material" e dizer o que falta
- Marca pessoal do dono e marca da empresa podem divergir. Se divergirem,
  perguntar qual vai ao ar — não fundir as duas
- Não fazer arquétipo, moodboard, mapa de empatia ou qualquer camada conceitual
  que não muda uma linha do que vai ser escrito amanhã
