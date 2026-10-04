---
name: radar
description: >
  Varredura de notícia, norma, decisão, mercado e conversa real do público do
  nicho do cliente, transformada em briefing de pautas prontas — cada uma com
  fato, fonte, por que importa, linha editorial, tensão, funil e gancho escrito.
  É a etapa diária da esteira de conteúdo. Use quando o usuário disser "roda o
  radar", "o que rolou no nicho hoje", "me traz pauta", "insumo pra conteúdo",
  "varredura", "/radar", ou quando precisar abastecer o calendário com tema que
  nasceu de pesquisa em vez de opinião solta.
---

# /radar — Varredura do nicho → pautas de conteúdo

Primeira etapa diária da esteira. **Todo conteúdo nasce de pesquisa, nunca de
opinião solta** — essa skill é a máquina que produz a pesquisa.

**Entrega:** `pesquisa/radar/AAAA-MM-DD.md` — 5 a 8 pautas fichadas.

Roda na mão a qualquer momento. Dá pra agendar (ver "Rodar sozinho" no fim).

## Dependências

- **Contexto:** `_memoria/empresa.md`, `_memoria/estrategia.md`,
  `marca/guia-de-marca.md` (voz e lista de proibidos)
- **A lente:** `conteudo/arquitetura-editorial.md` — linhas, fatias, balanço de
  funil e a matriz de tensões. Vem do `/arquitetura-editorial`
- **O banco perene:** `pesquisa/ideias/` — pra dizer onde cada pauta encaixa
- **Fontes do nicho:** `pesquisa/fontes.md` — montado na primeira rodada
- **Modelo da saída:** `modelo-briefing.md` (nesta pasta)
- **Ferramentas:** WebSearch e WebFetch. **Só isso.** Nada de API paga em rotina
  recorrente: é o único consumidor diário do sistema, e gasta sem ninguém ver

---

## Primeira rodada — montar as fontes do nicho

Se `pesquisa/fontes.md` não existir, **essa é a rodada mais importante do
contrato**. Antes de varrer, montar o mapa de fontes daquele nicho.

Ler `_memoria/empresa.md` e definir, com o operador, **as frentes de
varredura**: os 4 a 6 assuntos que, quando se mexem, mudam alguma coisa pro
cliente final da empresa.

Frentes servem pra qualquer nicho — o conteúdo é que muda:

| Tipo de frente | Contabilidade | Clínica odontológica | Loja de material de construção |
|---|---|---|---|
| Norma e obrigação | Receita Federal, prazo de declaração, eSocial | ANVISA, conselho regional | Norma técnica, NBR, licenciamento |
| Decisão e fiscalização | Carf, autuação, jurisprudência tributária | Processo ético, fiscalização sanitária | Procon, garantia, responsabilidade |
| Dinheiro e mercado | Taxa, crédito, custo de folha | Tabela de convênio, custo de insumo | Preço de insumo, câmbio, juros de financiamento |
| Calendário do setor | Prazo fiscal, fechamento, IR | Campanha de saúde, sazonalidade | Safra de obra, chuva, 13º |
| Regional | Prefeitura, junta comercial, economia local | Concorrência e demanda da cidade | Obra pública, loteamento novo |
| A conversa do público | Dúvida de empresário em grupo, YouTube | Medo de dentista, preço, dor | "Vale a pena", "quanto gasta", "fui enganado" |

Perguntar ao operador:

1. "Quando alguma coisa muda no mundo e o telefone do cliente toca, o que mudou?"
2. "Que órgão, entidade ou publicação manda no setor dele?"
3. "Onde o cliente final dele reclama e tira dúvida na internet?"

Com as respostas, **pesquisar de verdade** — buscar os sites oficiais, as
associações, os portais setoriais, os canais e fóruns. Não montar de cabeça.

Escrever `pesquisa/fontes.md` no formato descrito em "Estrutura de `fontes.md`",
mostrar pro operador e só então varrer.

Fonte nova boa que aparecer numa rodada futura: acrescentar no arquivo.

### Duas frentes opcionais, com regra própria

Valem quando o nicho pede. Entram em `fontes.md` como qualquer frente, com a
regra junto.

**A leitura do analista** — o que 3 ou 4 analistas do setor estão dizendo
(YouTube, coluna, LinkedIn). **Roda uma vez por semana, na segunda**, não todo
dia. O valor não é a leitura em si, é o cruzamento: o analista diz "a margem
caiu pra 8%"; a pauta da empresa é "e o que isso muda na decisão que o seu
cliente toma este mês". **Sem essa segunda metade, não é pauta, é repost.**

**Falas públicas** — declaração de autoridade, entidade, banco ou órgão que dá
pra traduzir em **decisão prática** do cliente final. As outras frentes pegam a
regra; esta pega o discurso sobre a regra, que é o que circula no grupo de
WhatsApp. A ponte é mais dura, não mais frouxa:

1. **Separar a fala em afirmações** e classificar cada uma: testável (dá pra
   checar com número), tese, método, ou identidade/partidária
2. **Descartar o que só dá pra responder tomando lado.** Sempre
3. **Traduzir o que sobra em decisão:** "o que muda pra ele na segunda-feira?"
   A fala abre; quem fecha é a conta

Regras de risco: reagir à ideia, nunca à pessoa · sem adjetivo · preferir a
frase ao vídeo · nada de rosto de político ou símbolo de partido · em período
eleitoral, toda pauta desta frente sai marcada `⚠️ decisão do cliente` e não vai
ao ar sem ele · quando a fala for quente demais, oferecer na ficha a versão sem
autor. Dia sem fala que passe na ponte: a frente entrega zero, e isso se
escreve no briefing.

---

## Workflow da rodada

### Passo 0 — Situar

1. Ler as dependências. Confirmar a data de hoje e **em que ponto do ano do
   setor a gente está** (calendário do setor em `fontes.md`). Pauta fora de
   estação rende menos, por melhor que seja
2. Ler os **últimos 5 briefings** em `pesquisa/radar/`. Serve pra duas coisas:
   não repetir pauta já entregue, e reconhecer quando assunto antigo teve
   desdobramento — aí não é repetição, é continuação, e vale marcar como tal
3. **A janela da varredura vai do último briefing até hoje**, não só "desde
   ontem". Ler a data do arquivo mais recente da pasta e usar como corte.
   Depois de fim de semana, feriado ou máquina desligada, a janela é maior
4. Ler `pesquisa/fontes.md`

> **Buraco na pasta não é falha do agendamento.** Data faltando entre os
> briefings diz só quanto tempo a janela precisa cobrir. Esta skill não enxerga
> o Agendador de Tarefas: nunca escrever no briefing que "a tarefa não rodou".
> Se algo parecer errado, vai em "Falhas da varredura" como pergunta, não como
> constatação.

### Passo 1 — Varrer as frentes

Percorrer as frentes de `pesquisa/fontes.md`, na ordem de prioridade que o
arquivo define.

**As fontes fixas são o piso, não o teto.** Toda rodada tem pelo menos uma busca
aberta por tema, fora da lista. Seguir o fio de uma notícia até a fonte
primária, e abrir fonte nova quando o assunto pedir.

Como buscar:

1. **Busca antes de URL decorada.** Portal muda estrutura e link profundo morre.
   `WebSearch` (com `site:` quando servir) e só então `WebFetch` na página que a
   busca devolveu
2. **Sempre com recorte de tempo.** Acrescentar mês e ano à consulta — sem isso o
   buscador devolve matéria velha com cara de novidade
3. **Subir até a fonte primária.** Portal noticiou uma norma? Abrir a norma.
   Citou decisão? Abrir a decisão. A ficha se escreve a partir do documento, não
   do resumo do portal
4. **Conferir a data em toda página aberta.** Notícia sem data não entra
5. **Duas fontes independentes** pra qualquer número que vá virar post

### Passo 2 — A conversa real

Separado da varredura de fato, e igualmente importante: onde o cliente final
fala com as palavras dele. Dúvida, reclamação, discussão real — comentário de
YouTube, fórum, grupo, review, seção de comentários de portal.

Vira a seção **Radar de perguntas**: 3 a 5 perguntas reais, transcritas o mais
próximo possível de como foram feitas. Sem corrigir a gramática — corrige só
quando a pergunta virar título.

**Olhar primeiro em `pesquisa/investigacoes/comentarios/`** — o `/investigar` no
modo `comentarios` deixa o corpus pronto ali, e puxar de lá é melhor e mais
barato que buscar na web na hora. Se o corpus tiver mais de duas semanas, avisar
no briefing que vale rodar de novo. Se não existir, buscar na web e registrar em
"Falhas da varredura" que não havia corpus.

**O gancho nasce do vocabulário do público, não do termo técnico.** A pauta pode
nascer da norma; a primeira linha nasce de como o cliente final fala dela.
`pesquisa/vocabulario.md` tem as palavras dele.

### Passo 3 — O filtro

Cada achado passa por três perguntas, nesta ordem:

> **1. Isso muda alguma coisa concreta pro cliente final dessa empresa?**
> **2. Em qual linha e em qual tensão isso entra?** (da arquitetura editorial.
> Pauta que não entra em nenhuma é notícia, não é pauta)
> **3. Amarra em algum serviço que a empresa realmente vende?**

"Não muda nada, mas é interessante" → corta. Vai pra "Sinais fracos" ou pro lixo.

O erro de um radar automático é encher o briefing pra parecer produtivo. Quem lê
perde a confiança na primeira vez que abre e acha enchimento.

Corta também:

- O que só rende post alarmista
- Disputa partidária e briga de figura pública. A **fala** de uma autoridade
  pode entrar, pela frente de falas públicas, quando vira decisão sem tomar
  lado; a **disputa** entre elas nunca entra
- Promessa de resultado que o setor proíbe
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
- **Linha e tensão** — da arquitetura editorial, uma de cada, escolhida.
  Sem arquitetura: usar **Ativo raiz** (o serviço ou tema-mãe a que a pauta se
  amarra) e escrever no topo do briefing que a lente ainda não existe
- **Funil** — topo, meio ou fundo. Se a semana está enchendo de um só, dizer
- **Amarra em** — qual serviço da empresa a pauta prepara. Pauta que não amarra
  em nada que a empresa vende é conteúdo bonito que não paga a conta
- **Banco** — se `pesquisa/ideias/` existir: a pauta **reforça** uma ideia do
  banco (é o fato que faltava pra produzir aquela agora), **atualiza** uma ideia
  (muda um dado dela), ou é **nova**. Casar por linha, tensão e tema, nunca por
  palavra solta. Assunto que aparece "novo" três semanas seguidas é buraco no
  banco: dizer isso
- **O ângulo da empresa** — o que ela fala que o resto não fala. Se não tiver
  ângulo próprio, a pauta é fraca
- **Formato e canal** — um formato escolhido, não uma lista de opções
- **Gancho de abertura** — a primeira linha, escrita de verdade, no vocabulário
  do público
- **Temperatura** — 🔥 quente (perde validade em dias) ou 🌱 permanente

### Passo 5 — Salvar e reportar

1. Salvar em `pesquisa/radar/AAAA-MM-DD.md` — exatamente esse nome, com a data
   de hoje. É por ele que o script agendado confere se a rodada entregou
2. **Na última rodada da semana** (sexta, quando agendado), consolidar em
   `pesquisa/radar/resumo-semanal-AAAA-Www.md`: o que se repetiu, o que virou
   tendência, as 3 pautas mais fortes, o balanço de linha e funil da semana, e o
   que ficou pendente de desdobramento. É esse arquivo que alimenta o
   `/calendario` do mês
3. Reportar no chat em até 10 linhas: os títulos e o destaque do dia. Quem quiser
   detalhe abre o arquivo

---

## Estrutura de `fontes.md`

```markdown
# Fontes e táticas de busca — <empresa>

> Piso da varredura, não teto. Fonte nova boa → acrescentar aqui.

## Calendário do setor

| Mês | O que acontece | Antecipar pauta em |
|---|---|---|

## Frente A — <nome> (prioridade máxima)

<por que essa é a mais importante pra esse cliente>

| Fonte | Onde | O que procurar |
|---|---|---|
| | | |

**Consultas-modelo:**
- `<consulta com [mês] [ano]>`

## Frente B — <nome>
...

## Frente <X> — A leitura do analista (semanal, opcional)

| Analista | Canal onde é mais forte | Do que fala |
|---|---|---|

## Frente <Y> — Falas públicas (opcional)

<onde procurar · a ponte · as regras de risco>

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
- Sem alarmismo, clickbait, promessa de resultado ou ataque político. **Sem medo
  como mecanismo**: "existe uma mudança, e ela pede organização antes da próxima
  decisão" serve; "você vai perder tudo" não
- Evitar vocabulário morto: "ecossistema", "jornada", "protagonismo",
  "resiliência", "parceiro estratégico"
- Pauta que gera demanda acima da capacidade de entrega da empresa merece aviso na
  ficha. Em operação enxuta o gargalo costuma ser entrega, não demanda — e todo
  setor tem o mês em que a operação está no limite. Pauta de captação nesse mês
  cai no pior momento

## Rodar sozinho (agendado)

`scripts/radar-diario.ps1` roda `claude -p "/radar"` sem ninguém na frente,
agendado pelo `scripts/agendar-radar.ps1` (segunda a sexta, no horário que o
operador escolher). Nesse modo:

- **Não perguntar nada — decidir e seguir.** Pergunta numa rodada agendada mata a
  rodada: ninguém responde, e o processo termina sem briefing
- **Só as ferramentas de busca, leitura e escrita existem.** O script libera
  WebSearch, WebFetch, Read, Write, Edit, Glob, Grep e TodoWrite, e sobe sem
  nenhum servidor MCP. Nada de terminal, script Python ou subagente nesta skill —
  se o corpus de comentários estiver velho, avisar no briefing, não tentar coletar
- **O log de hoje já existe quando você começa, e é da sua própria rodada.** O
  script grava `pesquisa/radar/_log/AAAA-MM-DD.log` ("=== Radar de ..." e
  "Iniciando varredura") **antes** de chamar a skill. Isso não indica outra
  varredura em paralelo: seguir normalmente
- Se uma fonte cair ou bloquear, anotar em "Falhas da varredura" e continuar.
  Nunca abortar o briefing inteiro por uma fonte fora do ar
- **Sempre salvar o arquivo do dia**, mesmo em dia fraco. O script julga a rodada
  pelo arquivo `pesquisa/radar/AAAA-MM-DD.md`, não pelo código de saída
- A frente semanal (leitura do analista), se existir, roda na segunda. O resumo
  semanal sai na sexta
- Só agendar depois que `pesquisa/fontes.md` existir e o operador tiver aprovado
  pelo menos duas rodadas na mão. Radar automático em cima de fontes erradas
  produz lixo todo dia, com pontualidade
- Escolher a frequência pelo ritmo do setor. Setor que muda toda hora (tributário,
  crédito) pede diário; setor de ciclo lento pede semanal. Diário num setor parado
  gera briefing vazio e ninguém abre mais
