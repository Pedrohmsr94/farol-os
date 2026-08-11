---
name: relatorio
description: >
  Fecha o mês num relatório que o cliente lê — o que aconteceu, os números com
  origem, o que funcionou, o que não funcionou e o que muda no mês seguinte.
  Lê os exports de `dados/` e os resultados dos posts publicados. Use quando o
  usuário disser "fechar o mês", "relatório mensal", "relatório pro cliente",
  "/relatorio".
---

# /relatorio — Fechamento do mês

Esse documento vai pra mão do cliente. É ele que faz o contrato ser renovado ou
não — e não por ser bonito, mas por mostrar que alguém está prestando atenção.

Saída: `relatorios/AAAA-MM-relatorio.md`, a partir de
`templates/relatorio-mensal.md`.

---

## Passo 1 — Juntar o material

- `dados/` — os exports do mês. **Se não tiver export, parar e pedir.**
- `conteudo/publicados/` — os posts do mês e os rodapés de resultado
- `relatorios/AAAA-Snn-semana.md` — os semanais do mês
- `relatorios/` do mês anterior — a base de comparação
- `_memoria/estrategia.md` — o objetivo e os indicadores
- `diagnostico/diagnostico.md` — o baseline do dia zero

**Sem export, sem relatório:**

> "Não tem export de <plataforma> em `dados/`. Sem isso eu escrevo o relatório
> com o campo de número vazio e uma nota dizendo por quê — ou você exporta e a
> gente fecha certo. O que prefere?"

Nunca preencher número de cabeça. Um número errado num relatório mensal é o
tipo de erro que o cliente descobre e não esquece.

---

## Passo 2 — Comparar

Três comparações, nessa ordem de importância:

1. **Contra a meta** — bateu o que estava em `_memoria/estrategia.md`?
2. **Contra o mês anterior** — subiu ou caiu?
3. **Contra o dia zero** — onde estava quando o contrato começou?

A terceira é a que mais convence em mês ruim. Um mês fraco em cima de uma base
que triplicou desde março continua sendo progresso — e dizer isso com o número
do diagnóstico do lado não é maquiar, é dar escala.

**Separar movimento de resultado.** Alcance subiu e mensagem não subiu não é
vitória — é sinal de que o conteúdo atrai quem não compra. Dizer isso.

---

## Passo 3 — Escrever

Preencher `templates/relatorio-mensal.md`.

**Como escrever cada parte:**

**O que aconteceu** — uma frase, começando pelo resultado. Se caiu, a primeira
linha diz que caiu. Cliente que descobre a queda no meio da tabela para de
confiar no documento inteiro.

**Os números** — tabela, com a origem. Campo sem dado fica vazio com a nota do
motivo.

**O que foi feito** — fato com data, não esforço. "8 posts, 2 campanhas de
aniversário, ficha do Google Meu Negócio corrigida" — não "trabalhamos
intensamente no conteúdo".

**O que funcionou** — com o número do lado. Sem número não é "funcionou", é
"achei que".

**O que não funcionou** — existe sempre. Relatório sem essa seção é apresentação
de vendas, e o cliente sente. Escrever sem drama e já emendar no que muda.

**O que muda no mês que vem** — consequência direta das duas seções acima.

**O que preciso de você** — o que trava do lado dele: foto, aprovação, acesso,
resposta. Com quanto tempo está parado, tirado dos semanais. Essa seção resolve
90% da conversa difícil de renovação.

**Linguagem:** a do dono, não a de agência. Nada de CTR, engajamento, alcance
orgânico sem explicação. Se um termo técnico for necessário, explicar do lado
na primeira vez.

---

## Passo 4 — Mês ruim

Quando o mês foi ruim, o relatório fica **mais** direto, não menos:

1. Diz que foi ruim, na primeira linha
2. Diz por quê, com o que se sabe — e diz o que não se sabe
3. Diz o que muda, concreto
4. Não compensa com métrica de vaidade que subiu

Se a causa foi do lado do cliente (não mandou material, não aprovou, mudou de
ideia no meio), registrar como fato com data — sem acusação e sem omissão.
Os semanais têm as datas.

---

## Passo 5 — Fechar

Mostrar o relatório inteiro pro operador antes de qualquer coisa:

> "Lê antes de mandar. Tem alguma coisa aqui que você prefere falar na reunião
> em vez de deixar escrito?"

Depois de aprovado:

- Atualizar `_memoria/estrategia.md` — o baseline dos indicadores vira o número
  desse mês
- Se o objetivo do trimestre fechou, oferecer definir o próximo
- Atualizar `indice.md`
- Oferecer o `/salvar`

---

## Regras

- **Nenhum número sem origem.** Nem estimativa, nem benchmark de setor, nem
  "cerca de"
- **Não esconder queda.** Nem em adjetivo, nem em gráfico recortado, nem
  escolhendo o mês de comparação que favorece
- **Não prometer o mês que vem.** Dizer o que vai ser feito, não o que vai
  acontecer
- Comparação com o diagnóstico é honesta e vale usar. Trocar a base de
  comparação de mês pra mês procurando a que fica melhor, não
- Se o contrato não foi cumprido do lado do operador (entregou menos que o
  combinado), isso entra no relatório. Ele vai perceber de qualquer jeito
