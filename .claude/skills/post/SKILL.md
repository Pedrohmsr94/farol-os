---
name: post
description: >
  Escreve um conteúdo da pauta na voz da marca do cliente — post, carrossel,
  legenda, roteiro de vídeo curto — e salva em `conteudo/fila/` pronto pra
  aprovação. Use quando o usuário disser "escreve o post de X", "faz o carrossel
  sobre Y", "cria a legenda", "/post", ou apontar uma linha do calendário.
---

# /post — Produção de conteúdo

Escreve o que está na pauta, na voz da empresa, e joga na fila de aprovação.

Saída: `conteudo/fila/AAAA-MM-DD-tema-curto.md`, a partir de `templates/post.md`.

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

Se faltar prova, perguntar antes de escrever — não preencher com número
plausível.

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

## Passo 5 — Aprovação

Quando o operador voltar dizendo que o cliente aprovou:

- Mover o arquivo de `conteudo/fila/` pra `conteudo/publicados/`
- Marcar `status: publicado` e a data
- Atualizar a linha no calendário

Quando voltar com **correção do cliente**, aplicar — e perguntar:

> "Isso é gosto do dia ou é regra da marca? Se for regra, salvo no guia pra
> não acontecer de novo."

É assim que o guia melhora sozinho ao longo do contrato.

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
