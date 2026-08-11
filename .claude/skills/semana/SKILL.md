---
name: semana
description: >
  Fecha a semana de trabalho: o que saiu, o que rendeu, o que travou e o que
  fazer segunda. Preenche o resultado dos posts publicados e escreve o registro
  semanal em `relatorios/`. Use quando o usuário disser "fechar a semana",
  "revisão semanal", "o que rolou essa semana", "/semana", ou na sexta.
---

# /semana — Fechamento de semana

Uso interno do operador. Pode ser cru — não vai pro cliente.

Duas funções: dizer o que fazer na segunda, e **preencher o resultado dos posts**.
Essa segunda parte é a que faz o sistema aprender. Sem ela, o `/calendario` do
mês seguinte decide no escuro e o `/relatorio` do mês vira arqueologia.

Saída: `relatorios/AAAA-Snn-semana.md`.

---

## Passo 1 — Puxar o resultado dos posts

Listar os posts em `conteudo/publicados/` que foram ao ar há **7 dias ou mais**
e estão com a seção "Resultado" vazia.

Pra cada um, pedir os números que fazem sentido no canal — alcance,
salvamento, compartilhamento, comentário, mensagem gerada, clique.

Se o operador tiver os exports em `dados/`, ler de lá em vez de perguntar.

Preencher o rodapé do próprio arquivo do post:

```markdown
## Resultado

**Publicado em:** 03/09/2026
**Números:** 1.240 alcance · 38 salvamentos · 4 mensagens no WhatsApp
**O que aprendi:** carrossel de dúvida prática rende 3x mais salvamento que
post institucional. Terceiro seguido com o mesmo padrão.
```

O "o que aprendi" é uma frase. Se não deu pra aprender nada, escrever "nada
conclusivo" — é honesto e evita conclusão inventada em cima de um post só.

---

## Passo 2 — Varrer a semana

- **Saiu o que estava previsto?** Comparar com `conteudo/calendario.md`
- **Fila parada.** O que está em `conteudo/fila/` há mais de 5 dias esperando
  aprovação. Isso é atraso do cliente e precisa ser registrado com data
- **Pendências.** O que está em "Em aberto" no `indice.md` e não andou
- **Fora do escopo.** Pedido que chegou e não está no contrato

---

## Passo 3 — Escrever

```markdown
# Semana <nn> — <dd/mm> a <dd/mm>

## Saiu
- <post, data, canal>

## Rendeu
- <o que os números mostraram, com o número junto>

## Travou
- <o que não andou, desde quando, esperando quem>

## Segunda
- <3 a 5 coisas, concretas>

## Pro cliente
- <o que precisa ser cobrado dele, com quanto tempo está parado>
```

A seção "Travou" é a mais útil do arquivo. Semana sem nada travado é raro — se
estiver vazia, conferir de novo antes de aceitar.

---

## Passo 4 — Fechar

```
Semana <nn> fechada.
<n> posts com resultado preenchido · <n> travados
Cobrar do cliente: <o item mais velho, parado há <n> dias>
```

Se algo da semana virou aprendizado durável (padrão que se repetiu três vezes,
decisão do cliente, combinado novo), oferecer o `/fechar`.

---

## Regras

- **Número só de export ou da boca do cliente.** Nunca estimar alcance
- **Um post não é padrão.** Só escrever "funciona" quando o mesmo padrão
  apareceu três vezes. Antes disso, é sinal
- Não transformar isso em relatório bonito. É rascunho de trabalho
- Se a semana não teve publicação nenhuma, registrar por quê. Três semanas
  assim é problema de contrato, não de conteúdo
