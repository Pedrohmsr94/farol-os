---
name: post
description: >
  Escreve um conteúdo da pauta na voz da marca do cliente — post, carrossel,
  legenda, roteiro de vídeo curto — e salva em `conteudo/fila/` pronto pra
  aprovação. Use quando o usuário disser "escreve o post de X", "faz o carrossel
  sobre Y", "cria a legenda", "/post", ou apontar uma linha do calendário.
---

# /post — Peça de texto

Escreve o que está na pauta, na voz da empresa, e joga na fila de aprovação.

Saída: `conteudo/fila/AAAA-MM-DD-tema-curto.md`, a partir de `templates/post.md`.

**A skill certa entre as três de produção:**

| Pedido | Skill |
|---|---|
| Legenda, post de texto, roteiro de reel, post de LinkedIn | `/post` — é aqui |
| Slides visuais em PNG | `/carrossel` |
| Artigo + carrossel + 3 legendas amarrados | `/publicar-tema` |

---

## Antes de escrever

Ler, sempre:

- `marca/guia-de-marca.md` — **obrigatório**
- `_memoria/empresa.md` — o que vende, prova disponível
- `conteudo/calendario.md` — a linha dessa pauta: objetivo, formato, canal

**Se o guia de marca estiver em branco:**

> "O guia de marca está vazio. Se eu escrever agora, vai sair com cara de
> qualquer empresa do setor — e o cliente vai dizer que não parece ele.
> Rodo o `/marca` primeiro? São uns 20 minutos e vale pro contrato inteiro."

Só escrever sem guia se o operador insistir, e avisar no arquivo que o texto
foi escrito sem voz definida.

---

## Passo 1 — Travar o objetivo

Antes da primeira frase, saber:

- **O que esse post tem que fazer.** Um objetivo só: ser salvo, gerar mensagem
  no WhatsApp, derrubar uma objeção, anunciar. "Engajamento" não é objetivo
- **Pra quem.** O recorte, não "todo mundo"
- **Que prova sustenta.** Se o post afirma algo, o que respalda
- **De qual pesquisa ele nasceu.** Briefing do `/radar`, documento de ângulos,
  tema de SEO. Peça sem raiz de pesquisa é reprovada no `/revisar`

Se faltar prova, perguntar antes de escrever — não preencher com número
plausível.

**Se o tema ainda não passou pelo `/angulos`**, oferecer:

> "Esse tema dá pra contar de uns cinco jeitos. Rodo o `/angulos` antes? O
> primeiro ângulo que vem à cabeça costuma ser o que todo mundo já publicou —
> e os quatro que sobram viram pauta do mês que vem."

Se o operador quiser seguir direto, seguir. Não travar.

---

## Passo 2 — Escrever

**A abertura.** Primeira linha carrega o post inteiro. Ela fala do problema de
quem lê, não da empresa. "Sua declaração pode estar na malha fina sem você
saber" ganha de "A Unitec é uma contabilidade com 15 anos de mercado".

**O corpo.** Uma ideia por bloco. Concreto — número, nome, situação real.
Se for carrossel, um bloco por card, numerado, cada card se sustentando sozinho.

**O fecho.** O que a pessoa faz agora, na voz da marca. Se o guia diz que a
empresa não usa CTA agressivo, não usar.

**Formatos:**

| Formato | O que muda |
|---|---|
| Carrossel | 5 a 8 cards. Card 1 = a fisgada. Último = o que fazer |
| Post único | texto curto, uma ideia só |
| Roteiro de vídeo | falas marcadas, 30-60s, primeira frase nos 3 primeiros segundos |
| Legenda | pode existir sozinha ou acompanhar o formato acima |

---

## Passo 3 — Testar antes de entregar

Três checagens, sempre, antes de mostrar:

1. **Genérico?** Se o texto pudesse estar no perfil de qualquer empresa do mesmo
   setor da mesma cidade, reescrever. Trocar adjetivo por fato concreto da
   empresa
2. **Sustenta?** Toda afirmação tem prova. Setor regulado: conferir a lista de
   assuntos proibidos do guia
3. **Soa como a empresa?** Ler contra o exemplo real colado no guia de marca.
   Se destoar, ajustar

Post que falha na 1 é o mais comum. Ele parece bom e não é.

Isso é auto-checagem, não revisão. A revisão de verdade é o `/revisar`, no
passo 5 — e ela roda com olhos frescos justamente porque quem escreveu não
enxerga o próprio vício.

---

## Passo 4 — Salvar e mostrar

Preencher `templates/post.md`, salvar em `conteudo/fila/`, atualizar o status
da linha no `conteudo/calendario.md` pra `escrito`.

Mostrar o texto na conversa — o operador precisa ler antes de mandar pro cliente.

```
Escrito: conteudo/fila/<arquivo>
Objetivo: <o que ele tem que fazer>
Preciso de você: <foto, dado, aprovação que falta>
```

## Passo 5 — Revisar

Antes de mandar pro cliente, rodar `/revisar`. Ele julga contra `criterios.md` e
devolve veredito.

**REPROVADO** volta pra reescrita, não vai pro cliente com ressalva. Mandar peça
reprovada dizendo "tem uns pontinhos" é como o padrão se perde.

## Passo 6 — Aprovação e publicação

Peça aprovada pelo cliente → `/aprovar-post`. Ele move pra `conteudo/publicados/`,
marca a data e atualiza o calendário.

Quando o cliente voltar com **correção**, aplicar — e perguntar:

> "Isso é gosto do dia ou é regra da marca? Se for regra, salvo no guia pra
> não acontecer de novo."

Regra vai pro `marca/guia-de-marca.md` **e** pro bloco "Bloqueios deste cliente"
em `.claude/skills/revisar/criterios.md`. É assim que o sistema para de errar a
mesma coisa duas vezes.

---

## Regras

- **Não inventar dado.** Nem número, nem depoimento, nem caso de cliente
- **Não prometer resultado** em setor regulado (saúde, direito, contabilidade,
  financeiro). Conferir o guia antes
- **Não usar o formato que a marca não usa.** Se o guia diz "sem emoji", é sem
  emoji, mesmo que o formato "peça"
- **Não escrever cinco posts de uma vez** sem o operador ver o primeiro. Se a
  voz estiver errada, erra nos cinco
- Se o cliente aprovar sem ler e depois reclamar, isso vira linha em
  `_memoria/operacao.md`, "Combinados que já custaram caro"
