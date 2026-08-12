---
name: radar
description: >
  Varredura de notícia, norma, decisão, mercado e conversa real do público do nicho
  do cliente, transformada em briefing de pautas prontas — cada uma com fato, fonte,
  por que importa, ângulo e formato. É a primeira etapa da esteira de conteúdo.
  Use quando o usuário disser "roda o radar", "o que rolou no nicho hoje", "me traz
  pauta", "insumo pra conteúdo", "varredura", "/radar", ou quando precisar abastecer
  o calendário com tema que nasceu de pesquisa em vez de opinião solta.
---

# /radar — Varredura do nicho → pautas de conteúdo

Primeira etapa da esteira. **Todo conteúdo nasce de pesquisa, nunca de opinião
solta** — essa skill é a máquina que produz a pesquisa.

**Entrega:** `pesquisa/radar/AAAA-MM-DD.md` — 5 a 8 pautas fichadas.

Roda na mão a qualquer momento. Dá pra agendar (ver "Rodar sozinho" no fim).

## Dependências

- **Contexto:** `_memoria/empresa.md`, `_memoria/estrategia.md`, `marca/guia-de-marca.md`
- **Fontes do nicho:** `pesquisa/fontes.md` — montado na primeira rodada
- **Modelo da saída:** `modelo-briefing.md` (nesta pasta)
- **Ferramentas:** WebSearch e WebFetch

---

## Primeira rodada — montar as fontes do nicho

Se `pesquisa/fontes.md` não existir, **essa é a rodada mais importante do
contrato**. Antes de varrer, montar o mapa de fontes daquele nicho.

Ler `_memoria/empresa.md` e definir, com o operador, **as frentes de varredura**:
os 4 a 6 assuntos que, quando se mexem, mudam alguma coisa pro cliente final da
empresa.

Frentes servem pra qualquer nicho — o conteúdo é que muda:

| Tipo de frente | Contabilidade | Clínica odontológica | Loja de material de construção |
|---|---|---|---|
| Norma e obrigação | Receita Federal, prazo de declaração, eSocial | ANVISA, conselho regional | Norma técnica, NBR, licenciamento |
| Decisão e fiscalização | Carf, autuação, jurisprudência tributária | Processo ético, fiscalização sanitária | Procon, garantia, responsabilidade |
| Dinheiro e mercado | Taxa, crédito, custo de folha | Tabela de convênio, custo de insumo | Preço de insumo, câmbio, juros de financiamento |
| Calendário do setor | Prazo fiscal, fechamento, IR | Campanha de saúde, sazonalidade | Safra de obra, chuva, 13º |
| Regional | Prefeitura, junta comercial, economia local | Concorrência e demanda da cidade | Obra pública, loteamento novo |
| A conversa do público | Dúvida de empresário no Reddit, grupo, YouTube | Medo de dentista, preço, dor | "Vale a pena", "quanto gasta", "fui enganado" |

Perguntar ao operador:

1. "Quando alguma coisa muda no mundo e o telefone do cliente toca, o que mudou?"
2. "Que órgão, entidade ou publicação manda no setor dele?"
3. "Onde o cliente final dele reclama e tira dúvida na internet?"

Com as respostas, **pesquisar de verdade** — buscar os sites oficiais, as
associações, os portais setoriais, os canais e fóruns. Não montar de cabeça.

Escrever `pesquisa/fontes.md` no formato descrito em "Estrutura de `fontes.md`",
mostrar pro operador e só então varrer.

Fonte nova boa que aparecer numa rodada futura: acrescentar no arquivo.

---

## Workflow da rodada

### Passo 0 — Situar

1. Ler `_memoria/empresa.md`, `_memoria/estrategia.md`, `marca/guia-de-marca.md`
2. Confirmar a data de hoje
3. Ler os **últimos 5 briefings** em `pesquisa/radar/`. Serve pra duas coisas: não
   repetir pauta já entregue, e reconhecer quando assunto antigo teve desdobramento
   novo — aí não é repetição, é continuação, e vale marcar como tal
4. Ler `pesquisa/fontes.md`

### Passo 1 — Varrer as frentes

Percorrer as frentes de `pesquisa/fontes.md`, na ordem de prioridade que o arquivo
define.

**As fontes fixas são o piso, não o teto.** Todo dia tem que haver pelo menos uma
busca aberta por tema, fora da lista. Seguir o fio de uma notícia até a fonte
primária, e abrir fonte nova quando o assunto pedir.

Como buscar:

1. **Busca antes de URL decorada.** Portal muda estrutura e link profundo morre.
   `WebSearch` com `site:` e só então `WebFetch` na página que a busca devolveu
2. **Sempre com recorte de tempo.** Acrescentar mês e ano à consulta — sem isso o
   buscador devolve matéria de 2019 com cara de novidade
3. **Subir até a fonte primária.** Portal noticiou uma norma? Abrir a norma. Citou
   decisão? Abrir a decisão. A ficha se escreve a partir do documento, não do
   resumo do portal
4. **Conferir a data em toda página aberta.** Notícia sem data não entra
5. **Duas fontes independentes** pra qualquer número que vá virar post

### Passo 2 — A conversa real

Separado da varredura de fato, e igualmente importante: onde o cliente final fala
com as palavras dele. Dúvida, reclamação, discussão real — comentário de YouTube,
fórum, grupo, review, seção de comentários de portal.

Vira a seção **Radar de perguntas**: 3 a 5 perguntas reais, transcritas o mais
próximo possível de como foram feitas.

É o insumo mais valioso do dia inteiro. Conteúdo bom costuma ser a resposta
literal a uma pergunta que alguém já fez em voz alta.

**Olhar primeiro em `pesquisa/investigacoes/comentarios/`** — o `/investigar` no
modo `comentarios` deixa o corpus pronto ali, e puxar de lá é melhor e mais barato
que buscar na web na hora. Se o corpus tiver mais de duas semanas, avisar no
briefing que vale rodar de novo. Se não existir, buscar na web e registrar em
"Falhas da varredura" que não havia corpus.

### Passo 3 — O filtro

Antes de virar pauta, cada achado passa por uma pergunta:

> **Isso muda alguma coisa concreta pro cliente final dessa empresa?**

Se a resposta for "não muda nada, mas é interessante", **corta**. Vai pra "Sinais
fracos" ou pro lixo.

O erro de um radar automático é encher o briefing pra parecer produtivo. Quem lê
perde a confiança na primeira vez que abre e acha enchimento.

Corta também:

- O que só rende post alarmista
- Pauta político-partidária, disputa eleitoral, briga de figura pública
- Assunto que exige opinião sem base técnica
- Nome de concorrente — sempre, em qualquer contexto
- Qualquer coisa na lista de assuntos proibidos de `marca/guia-de-marca.md`

**Se o dia for fraco, entregar dia fraco.** É legítimo fechar com 3 pautas e
escrever "hoje o setor não mexeu muito". Melhor que 8 pautas mornas. Nesses dias,
puxar do banco de temas permanentes de `pesquisa/fontes.md`.

### Passo 4 — Fichar

5 a 8 pautas, no formato de `modelo-briefing.md`. Os campos que mais importam:

- **O fato** — 1 ou 2 frases, com link e data. Sem adjetivo
- **Por que importa** — concreto, no vocabulário do cliente final. "Quem fechou
  contrato antes de março vai pagar a diferença na renovação", não "impactos
  relevantes no setor"
- **O ângulo da empresa** — o que ela fala que o resto não fala. Se não tiver
  ângulo próprio, a pauta é fraca
- **Formato e canal** — um formato escolhido, não uma lista de opções
- **Gancho de abertura** — a primeira linha, escrita de verdade
- **Temperatura** — 🔥 quente (perde validade em dias) ou 🌱 permanente
- **Ativo raiz** — a qual serviço ou tema-mãe da empresa a pauta se amarra

### Passo 5 — Salvar e reportar

1. Salvar em `pesquisa/radar/AAAA-MM-DD.md`
2. **Na última rodada da semana**, consolidar em `resumo-semanal-AAAA-Www.md`: o
   que se repetiu, o que virou tendência, as 3 pautas mais fortes e o que ficou
   pendente de desdobramento. É esse arquivo que alimenta o `/calendario` do mês
3. Reportar no chat em até 10 linhas: os títulos e o destaque do dia. Quem quiser
   detalhe abre o arquivo

---

## Estrutura de `fontes.md`

```markdown
# Fontes e táticas de busca — <empresa>

> Piso da varredura, não teto. Fonte nova boa → acrescentar aqui.

## Frente A — <nome> (prioridade máxima)

<por que essa é a mais importante pra esse cliente>

| Fonte | Onde | O que procurar |
|---|---|---|
| | | |

**Consultas-modelo:**
- `<consulta com [mês] [ano]>`

## Frente B — <nome>
...

## Onde o público conversa

| Lugar | O que se acha lá |
|---|---|

## Banco de temas permanentes

Pra dia fraco. Assunto que vale em qualquer semana:

1.
```

---

## Regras

- **Nunca inventar fato, número, data ou decisão.** Se não achou a fonte primária,
  escrever "não confirmado na fonte original" na ficha. Um briefing que vira post
  errado custa mais caro que um dia sem pauta
- Todo dado tem link e data. Notícia sem data não entra
- Número de norma, processo e artigo de lei: copiar exato, conferido
- **Valor que varia por faixa não é um valor só.** Taxa, alíquota, teto, prazo,
  tabela — quase sempre mudam por porte, enquadramento ou modalidade. Nunca
  escrever o número sem dizer pra quem ele vale. É o erro que mais aparece em
  conteúdo de nicho técnico
- Fonte oficial que devolve **403** é comum. Contornar por fonte secundária é
  aceitável **se duas fontes independentes convergirem** — e a ficha diz que a
  primária não abriu
- Nunca citar concorrente pelo nome
- Sem alarmismo, clickbait, promessa de resultado ou ataque político
- Pauta que gera demanda acima da capacidade de entrega da empresa merece aviso na
  ficha. Em operação enxuta o gargalo costuma ser entrega, não demanda

## Rodar sozinho (agendado)

Dá pra agendar `claude -p "/radar"` no Agendador de Tarefas do Windows ou no cron.
Nesse modo:

- Não perguntar nada — decidir e seguir
- Se uma fonte cair ou bloquear, anotar em "Falhas da varredura" e continuar.
  Nunca abortar o briefing inteiro por uma fonte fora do ar
- Só agendar depois que `pesquisa/fontes.md` existir e o operador tiver aprovado
  pelo menos duas rodadas na mão. Radar automático em cima de fontes erradas
  produz lixo todo dia, com pontualidade
- Escolher a frequência pelo ritmo do setor. Setor que muda toda hora (tributário,
  crédito) pede diário; setor de ciclo lento pede semanal. Diário num setor parado
  gera briefing vazio e ninguém abre mais
