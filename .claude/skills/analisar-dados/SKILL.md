---
name: analisar-dados
description: >
  Analisa um arquivo de dados (CSV, Excel, TXT, JSON, PDF) e devolve um resumo
  executivo com o que os números mostram, o que está funcionando, o que merece
  atenção e recomendações. Use quando o usuário disser "analisa esse arquivo",
  "o que mostram esses dados", "resume esse relatório", "/analisar-dados", ou
  jogar um arquivo em `dados/`.
---

# /analisar-dados — Análise de arquivo

## Dependências

- `_memoria/empresa.md` (pra saber o que os dados representam)
- `_memoria/estrategia.md` (pra saber qual número importa)

---

## Workflow

### Passo 1 — Contexto antes do arquivo

Antes de abrir, saber:

- De onde veio o arquivo e de que período
- Qual pergunta ele deveria responder

Se o operador não disser, perguntar. Análise sem pergunta vira lista de estatística
descritiva que não serve pra decidir nada.

### Passo 2 — Ler

Ler o arquivo inteiro quando couber. Se for grande, ler estrutura + amostra e dizer
que foi amostra.

Conferir antes de analisar:

- Quantas linhas, quantas colunas, que período cobre
- Coluna vazia, valor duplicado, data fora do intervalo
- Unidade e moeda

**Dado sujo encontrado é achado, não obstáculo.** Se 30% das linhas estão sem
origem do lead, isso é a informação mais importante do arquivo.

### Passo 3 — Analisar

Procurar, nessa ordem:

1. **A resposta à pergunta do passo 1**
2. **Tendência** — está subindo ou caindo, e desde quando
3. **Concentração** — os poucos que respondem pela maioria
4. **Anomalia** — o pico, a queda, o dia estranho. E se dá pra explicar
5. **O que falta** — o dado que faria a diferença e não está ali

Comparar com o que já se sabe do cliente. Número solto não diz nada; número contra
o mês anterior ou contra a meta diz tudo.

### Passo 4 — Entregar

```markdown
# Análise — <arquivo>
**Período:** <de> a <até> · **Linhas:** <n> · **Origem:** <de onde veio>

## O que esses dados mostram
<3-5 linhas. Começa pela resposta à pergunta.>

## O que está funcionando
<com o número do lado>

## O que merece atenção
<com o número do lado>

## 3 recomendações
1. <concreta, com quem faz>

## Números-chave
| Indicador | Valor | Comparação |
|---|---|---|

## Ressalvas
<o que o dado não permite concluir, o que estava sujo, o que foi amostra>
```

Salvar em `saidas/` ou ao lado do arquivo, e resumir no chat em até 10 linhas.

## Regras

- **Não extrapolar amostra pequena.** 12 linhas não sustentam tendência
- **Correlação não é causa.** "Publicamos mais e as vendas subiram" pode ser
  sazonalidade. Dizer o que não dá pra separar
- **A seção "Ressalvas" existe sempre.** Análise que finge certeza é pior que
  nenhuma
- Não inventar número que não está no arquivo, nem preencher lacuna com média
- Se o arquivo não responde a pergunta, dizer isso na primeira linha e falar qual
  dado responderia
