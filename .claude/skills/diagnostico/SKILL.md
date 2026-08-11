---
name: diagnostico
description: >
  Faz o diagnóstico de marketing da empresa — mapeia canais, caminho do cliente,
  quem faz o quê, o que é medido — e escreve o documento que vai pra primeira
  reunião, com os furos ordenados por custo e três ações pra começar. Use quando
  o usuário disser "diagnóstico", "mapear o marketing", "auditoria", "por onde
  começar com esse cliente", "/diagnostico".
---

# /diagnostico — O retrato do dia zero

Roda uma vez, no começo do contrato, depois do `/instalar`.

Duas funções: dar ao operador o mapa do que arrumar, e dar ao cliente a foto
contra a qual o resultado do terceiro mês vai ser comparado. Sem essa foto,
daqui a seis meses ninguém consegue provar que alguma coisa melhorou.

Saída: `diagnostico/diagnostico.md`, a partir de `templates/diagnostico.md`.

---

## Antes de começar

Ler `_memoria/empresa.md`, `_memoria/operacao.md`, `_memoria/estrategia.md`.
Muita coisa já foi respondida no `/instalar` — **não perguntar de novo**.
Abrir dizendo o que já se sabe e perguntando só o que falta.

Conferir `dados/`. Se tiver export, ler antes de perguntar qualquer número.

---

## Passo 1 — Levantamento

O que precisa estar mapeado. Perguntar só o que a memória não responde.

**Canais.** Cada um: existe? está ativo? qual foi a última atividade? em que
estado está?

Instagram · Google Meu Negócio · site · WhatsApp Business · Facebook ·
e-mail · qualquer outro que o setor use.

Pra cada canal ativo, pedir o número de hoje. Se o operador tiver acesso, pedir
o export pra `dados/` em vez de aceitar número de cabeça.

**O caminho do cliente.** Como uma pessoa sai de "não conhece" até "paga":

1. Como ela descobre a empresa hoje?
2. O que ela faz depois de descobrir? *(clica onde, chama onde)*
3. Quem responde, em quanto tempo?
4. O que acontece entre a primeira mensagem e o fechamento?
5. Depois que compra, alguém volta a falar com ela?

Perguntar em qual desses passos as pessoas somem. Se ninguém souber, esse já é
o primeiro achado: **a empresa não sabe de onde vem o cliente dela.**

**Quem faz o quê.** Quem posta, quem responde, quem decide, quem aprova.
Quanto tempo por semana. "O dono faz tudo nos intervalos entre atendimentos"
é achado, não detalhe de contexto.

**O que é medido.** O que a empresa olha pra saber se está funcionando. Se a
resposta for "alcance" ou "nada", registrar exatamente assim.

---

## Passo 2 — Os furos

Listar o que está furado, **ordenado por quanto custa, não por quanto é fácil
de arrumar**.

Cada furo precisa de três coisas:

1. O que é, em uma frase direta
2. A evidência — o número, o print, a frase que o dono falou
3. O que custa — em cliente perdido, em tempo, em dinheiro

Furo sem evidência não entra. Se for palpite, escrever como palpite e dizer o
que confirmaria.

**Os furos mais comuns em pequena empresa** — usar como checagem, não como
lista pra encher:

- Ninguém sabe de onde vem o cliente
- Mensagem no WhatsApp demora horas ou some
- Google Meu Negócio abandonado, ou sem endereço/horário certo
- Conteúdo publicado sem nenhum objetivo ligado a venda
- A empresa fala de si mesma o tempo todo e nunca do problema do cliente
- Nenhum registro de cliente antigo — não dá pra vender pra quem já comprou
- Dono é o gargalo de tudo que é decisão

---

## Passo 3 — O que fazer primeiro

**No máximo três ações.** Lista de dez itens não é plano, é jeito de não
começar nenhum.

Cada uma com: o que é, por que ela primeiro, quem faz, até quando.

Priorizar o que destrava as outras. Arrumar o Google Meu Negócio antes de
produzir conteúdo, porque conteúdo mandando gente pra um perfil errado é
dinheiro na lixeira.

Marcar claramente o que **não** é do escopo contratado — se a ação depende de
coisa que o operador não faz, isso vira pedido ao cliente, não tarefa dele.

---

## Passo 4 — Escrever

Preencher `templates/diagnostico.md` e salvar em `diagnostico/diagnostico.md`.

**Como escrever:**

- O resumo tem que se sustentar sozinho — é a única parte que o dono lê inteira
- Linguagem do dono, não de agência. "Ninguém responde o WhatsApp no fim de
  semana", não "há oportunidade de otimização no funil de atendimento"
- Número sempre com a origem do lado
- A seção "O que ficou sem resposta" existe e é preenchida. Diagnóstico que
  finge ter visto tudo perde credibilidade na primeira pergunta da reunião

---

## Passo 5 — Depois

Mostrar o resumo na tela e:

> "Está em `diagnostico/diagnostico.md`.
>
> Duas coisas que saem daqui: o baseline vai pra `_memoria/estrategia.md`,
> e as três ações viram as prioridades. Atualizo os dois agora?
>
> Depois disso, `/marca` — pra nenhum texto sair genérico."

Atualizar `indice.md`.

---

## Regras

- **Nenhum número inventado.** Nem estimativa "de mercado", nem benchmark de
  setor. Se não veio de export ou da boca do cliente, não entra
- **Não editar o diagnóstico depois.** É a foto do dia zero. Renovação de
  contrato gera `diagnostico-AAAA-MM.md` novo
- Não vender no diagnóstico. Se aparecer coisa fora do escopo, listar como
  achado e marcar como fora — sem virar proposta comercial no meio do documento
- Se o operador não tiver acesso a nenhuma plataforma, dizer com todas as letras
  que o diagnóstico está baseado em relato, e que isso limita o que dá pra afirmar
