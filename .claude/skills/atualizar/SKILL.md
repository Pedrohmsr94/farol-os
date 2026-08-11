---
name: atualizar
description: >
  Varre o repositório inteiro e compara com a memória, achando o que está
  desatualizado, contraditório ou nunca foi registrado. Propõe as correções e
  aplica depois de aprovação. Use quando o usuário disser "atualizar",
  "/atualizar", "revisa a memória", ou quando bater dúvida se o contexto ainda
  bate com a realidade.
---

# /atualizar — Varredura de contexto

O `/fechar` destila a **conversa**. Esse aqui varre o **repositório**.

Roda quando bater dúvida, ou uma vez por mês.

## Workflow

### 1. Ler a memória

`_memoria/empresa.md`, `_memoria/operacao.md`, `_memoria/estrategia.md`,
`marca/guia-de-marca.md`, `indice.md`, `CLAUDE.md`.

### 2. Varrer o estado real

- `conteudo/publicados/` — o que saiu desde o último registro. Tem post sem
  resultado preenchido?
- `conteudo/fila/` — tem coisa parada há semanas esperando aprovação?
- `conteudo/calendario.md` — o mês corrente está preenchido? O anterior ficou
  com pauta sem status?
- `relatorios/` — qual foi o último? Está atrasado?
- `dados/` — chegou export que ninguém leu?
- `_memoria/fontes/` — tem fonte bruta que nunca virou memória?
- `notas/` — nota sem tag de status, ou órfã (nenhum link aponta pra ela)?
- `.claude/skills/` — skill nova que o `CLAUDE.md` não menciona?

### 3. Cruzar

Procurar três coisas:

**Desatualizado** — a memória diz uma coisa e o repo mostra outra.
Ex: `estrategia.md` fala em "objetivo do trimestre" de um trimestre que já
passou.

**Contraditório** — dois arquivos afirmam coisas incompatíveis.
Ex: `operacao.md` diz 8 posts/mês, o calendário tem 4 há três meses.

**Não registrado** — aconteceu e ninguém escreveu.
Ex: campanha rodou, teve resultado, e não existe nota nem linha no índice.

### 4. Mostrar antes de aplicar

```
Varri o repo. <n> coisas fora do lugar:

1. [desatualizado] estrategia.md fala do objetivo de abril-junho; estamos em setembro
   → atualizar a fase e o objetivo do trimestre  (preciso te perguntar o novo)

2. [contradição] operacao.md: 8 posts/mês · calendário: 4 em jul, 4 em ago
   → qual vale? mudou o combinado ou está atrasado?

3. [não registrado] 6 posts em publicados/ sem seção "Resultado" preenchida
   → sem isso o /calendario do mês que vem decide no escuro

4. [órfã] notas/campanha-dia-das-maes.md sem tag de status e sem link
   → arquivar e citar no índice?

Aplico tudo, algumas ou nenhuma?
```

Uma linha por item, com o tipo entre colchetes e a consequência.

### 5. Aplicar

- Editar com cirurgia — só a linha relevante, nunca reformatar o arquivo
- O que depende de resposta do operador, perguntar. Não decidir por ele
- Atualizar `indice.md` no fim
- Mostrar o diff de cada mudança

## Regras

- **Contradição não se resolve sozinha.** Mostrar os dois lados e perguntar
- **Não apagar nada** sem aprovação explícita. Arquivar (`#status/arquivado`)
  em vez de deletar
- Se estiver tudo em ordem, dizer "nada fora do lugar" e parar. Não inventar
  problema pra parecer útil
