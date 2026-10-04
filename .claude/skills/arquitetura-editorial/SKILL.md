---
name: arquitetura-editorial
description: >
  Constrói o sistema editorial da empresa — Big Idea, crença e inimigo comum,
  matriz de tensões de quem compra, linhas editoriais com fatia e fronteira,
  balanço de funil, princípios "nunca" e o filtro de aprovação de peça. É a
  decisão que transforma diagnóstico, voz e pesquisa em lente de produção:
  depois dela, /radar, /ideias, /calendario, /angulos e /revisar param de
  improvisar critério. Escreve `conteudo/arquitetura-editorial.md`. Use quando o
  usuário disser "arquitetura editorial", "linha editorial", "linhas
  editoriais", "big idea", "o que essa marca defende", "estratégia de
  conteúdo", "sobre o que a gente fala", "/arquitetura-editorial".
---

# /arquitetura-editorial — A lente que decide o que a marca defende

Entre o diagnóstico e a produção existe uma decisão que ninguém costuma estar
encarregado de tomar: **o que essa empresa defende em público, pra quem, e por
quê agora.** Sem ela, o `/ideias` inventa linha editorial em três perguntas, o
`/angulos` escolhe ângulo pelo tema, e o `/revisar` julga o tom sem julgar se a
peça tem razão de existir. Essa skill toma a decisão uma vez, e o resto passa a
olhar por ela.

**Saída:** `conteudo/arquitetura-editorial.md` — um arquivo só, lido por todas
as skills de conteúdo. Substitui o antigo `linhas-editoriais.md`: as linhas
continuam existindo, agora dentro de uma decisão maior.

## Posição na esteira

Roda **depois** do `/diagnostico` e do `/marca`, e **antes** do primeiro
`/ideias` e do primeiro `/calendario`.

- **Não roda antes do `/marca`.** Voz, público e palavras proibidas são insumo.
  A arquitetura decide o que a marca *defende*; quem ela *é* está no guia
- **Consome a pesquisa:** `/investigar` (comentários, nicho, voz), `/seo`
  (demanda e concorrência), as primeiras rodadas do `/radar`. Sem pesquisa, as
  tensões são palpite, não evidência. Dá pra rodar assim, mas tudo sai marcado
  *(validar)*
- **Alimenta a produção:** `/radar`, `/ideias`, `/calendario`, `/angulos`,
  `/publicar-tema` e `/revisar` leem o que sai daqui

**Dois modos, pelo porte da operação:**

| Operação | Modo | O que sai |
|---|---|---|
| Uma pessoa produzindo, até ~12 peças/mês | **enxuto** | Big Idea, tensão-mãe + 3 tensões-porta, as 4 linhas do molde com fatia e fronteira, balanço de funil, princípios "nunca", filtro |
| Equipe, ou volume de emissora | **completo** | Tudo do enxuto + timing (por que agora), produtos e objeções por decisor, ativo atenção e plano de validação, rostos por linha, linhas agrupadas em eixos |

Os dois cabem no mesmo arquivo. O modo completo preenche mais seções.

## Dependências

- **Voz:** `marca/guia-de-marca.md` — obrigatório. Sem guia, avisar e oferecer
  `/marca` antes
- **Contexto:** `_memoria/empresa.md` (o que vende, pra quem, capacidade de
  entrega), `_memoria/estrategia.md` (objetivo do trimestre),
  `_memoria/operacao.md` (quantas peças o contrato prevê, quem produz)
- **Diagnóstico:** `diagnostico/diagnostico.md` — o caminho do cliente e onde
  ele some
- **Escuta:** `pesquisa/investigacoes/` — `comentarios/` (as leituras),
  `voz.md`, `nicho-*.md`, `anuncios-*.md`
- **Demanda:** `pesquisa/seo/01-pesquisa-demanda.md` e
  `02-analise-concorrencia.md`, se o `/seo` rodou
- **Sinais:** `pesquisa/radar/resumo-semanal-*.md` e os "Sinais fracos" dos
  briefings
- **O que já existe:** `conteudo/arquitetura-editorial.md` (se é revisão),
  `conteudo/publicados/` com resultado, e qualquer material editorial antigo da
  empresa ou de agência anterior em `_memoria/fontes/`

---

## Workflow

### Passo 0 — Portas e acervo

1. Conferir o guia de marca. Em branco → parar e oferecer `/marca`
2. Conferir o que há de pesquisa. Pouca pesquisa → avisar que a arquitetura
   vai sair com base de hipótese, e marcar tudo *(validar)*
3. **Inventariar o acervo editorial que já existe.** Se a empresa (ou uma
   agência anterior) já tem pilares, linhas, slogan ou tom definidos:
   reconciliar versões conflitantes (a mais recente e mais desenvolvida ganha,
   salvo decisão do cliente), registrar as divergências em aberto, e **adotar o
   vocabulário existente**. Nunca renomear o que a equipe já chama por um nome
4. Definir o modo (enxuto ou completo) pelo `_memoria/operacao.md`

### Passo 1 — A Big Idea

A tese central da comunicação: a frase que explica "o que está realmente
acontecendo aqui", e o filtro que decide o que entra e o que sai.

**As três perguntas que a constroem:**

1. Quem é a pessoa exata que mais precisa dessa empresa?
2. Qual é o problema mais incômodo que essa pessoa vive hoje?
3. Qual é a leitura própria da empresa sobre esse problema?

**O teste dos quatro elementos.** A Big Idea só fecha se passar nos quatro:

1. Nasce de um problema real (evidência da pesquisa, não achismo)
2. Reorganiza a percepção de quem compra (muda a categoria mental, não descreve
   a que já existe)
3. É simples o bastante pra ser repetida (uma frase, sem vírgula de apoio)
4. É proprietária: nenhum concorrente mapeado poderia assinar

Escrever também a **crença** (a visão de mundo por trás da Big Idea) e o
**inimigo comum**, que nunca é um concorrente: é uma prática ou crença do
mercado que a marca combate.

### Passo 2 — Quem decide, e a matriz de tensões

1. **Quem decide de verdade?** Muitas vezes não é uma pessoa: é uma dupla
   (dono e sócio, pai e filho, casal, quem usa e quem paga). Se for, o conteúdo
   fala com a mesa onde a decisão acontece, não com um perfil demográfico
2. **Montar a matriz de tensões:**

| # | Tensão | Nível | Formulação | Validação | Linha | Quando aparece |
|---|---|---|---|---|---|---|
| T0 | tensão-mãe | emocional, raramente dita | a frase afiada, em primeira pessoa | evidência / pesquisa / hipótese | | o momento da vida em que pesa |
| T1+ | tensões-porta | operacional, dizível | | | | |

Regras da matriz:

- **T0 é uma só.** As outras são variações dela em momentos diferentes. Se
  aparecem duas tensões-mãe, uma delas é porta
- **Toda tensão carrega grau de validação:** evidência interna da empresa
  (WhatsApp, objeção registrada) > dado público > comentário coletado >
  hipótese. Hipótese entra, marcada
- **Tensão-porta é gancho; tensão-mãe é destino.** O conteúdo entra pela porta
  (o problema que a pessoa admite) e puxa pra mãe (o que ela sente e não diz),
  sem nomear a mãe de cara

3. **O ativo atenção** *(modo completo)*: o que dispara a busca, de onde vem a
   confiança, quem ocupa hoje o papel de conselheiro — e o que o conteúdo pode
   **testar** enquanto ninguém validou nada formalmente. É a **validação por
   atenção**: mesma tensão, formulações diferentes, medir qual prende
   salvamento e comentário. Os testes entram no `/calendario` como peça-teste

### Passo 3 — Por que agora *(modo completo)*

Quais sinais de mercado e de comportamento estão convergindo pra abrir janela
pra essa marca: regulatório, geracional, tecnológico, econômico. Cada um com
fonte e data, tirado do `/radar`, do `/seo` e do `/investigar`.

**Regra dura: menos de 4 sinais convergentes, não há janela.** A seção sai
dizendo isso com todas as letras. Marca sem janela constrói autoridade de longo
prazo; não finge que surfa um momento.

Separar dado de leitura com a marca textual **"a leitura editorial é nossa"**
toda vez que a interpretação for da casa.

### Passo 4 — Linhas, fatias e fronteiras

A estrutura acompanha o porte. **Não impor grade grande em operação pequena.**

- **Modo enxuto:** as 4 linhas do molde, com fatia de partida (ajustar ao caso):

| Linha | O que conquista | Fatia de partida | Funil |
|---|---|---|---|
| **Autoridade** | "essa gente entende do assunto" | 30% | topo |
| **Utilidade** | "isso aqui me serviu" | 30% | topo/meio |
| **Confiança** | "dá pra confiar neles" | 25% | meio |
| **Oferta** | "é isso que eu preciso, e é com eles" | 15% | fundo |

- **Modo completo:** as linhas se agrupam em **eixos** pela origem da pauta
  (ex.: Notícia, Técnica, Mercado, Cultura, Marca), cada eixo com suas linhas
  nomeadas, formato principal e fatia

Em qualquer modo, cada linha precisa de:

- **O que ela conquista** na cabeça de quem lê (uma frase)
- **Fatia do mês** (%)
- **Etapa do funil** que serve
- **Fronteira** — o que **não** entra nela, escrito. É a fronteira que impede o
  técnico de virar propaganda e o institucional de virar álbum de foto
- **Quem alimenta:** `/radar`, quais fontes do `/ideias`, `/seo`
- **3 exemplos de pauta** que caberiam nela, escritos de verdade

**O balanço de funil** fecha o passo: quanto do mês é topo, meio e fundo, com o
alerta de desequilíbrio — só topo atrai e não aquece; só meio aquece e não
cresce; só fundo vende pra ninguém. Percentual é calibragem de partida:
revisar em 60 a 90 dias, com o resultado que o `/semana` registrou.

### Passo 5 — Produtos e objeções *(modo completo)*

Por produto ou serviço que o conteúdo deve preparar: o que é, pra quem, a
objeção principal, quem decide a compra. **Preço e margem não entram aqui** —
dado financeiro da empresa fica em `notas/privado/`. Basta dizer se o produto é
de entrada, principal ou de maior valor.

### Passo 6 — Princípios, voz e rostos

1. **Princípios em forma de "nunca"** — 5 a 8, específicos dessa empresa, cada
   um bloqueando um erro que esse mercado comete (ex.: "nunca medo como
   mecanismo", "nunca promessa de economia", "nunca notícia sem consequência").
   Princípio que serve pra qualquer marca não é princípio
2. **Voz** — 3 linhas apontando pro `marca/guia-de-marca.md`. Não duplicar o
   guia aqui
3. **Rostos** *(modo completo)* — quem aparece em qual linha e o que
   representa. Operação de uma pessoa só: dizer isso, e priorizar o formato que
   ela sustenta

### Passo 7 — O filtro de aprovação

As perguntas que toda peça responde antes de ir pro `/revisar`. Adaptar à
empresa:

1. Qual Big Idea esta peça sustenta?
2. De qual linha ela vem?
3. Em qual etapa do funil opera?
4. Pra quem fala (qual metade da dupla, se houver)?
5. **Qual tensão real ela organiza?** (pauta nasce de tensão, não de tema)
6. Qual decisão de quem lê ela melhora?
7. Qual é a fonte?
8. A peça reduz ou aumenta a ansiedade de quem lê?
9. Existe leitura própria, ou é só repetir a notícia?
10. O CTA continua a narrativa?

Copiar o filtro adaptado pra seção **"Filtro da arquitetura editorial"** de
`.claude/skills/revisar/criterios.md`. É o elo que faz o revisor julgar
pertinência, e não só tom. Os princípios "nunca" que forem específicos do setor
entram também no **bloqueio 10** do mesmo arquivo.

### Passo 8 — Mostrar, marcar hipóteses, salvar

1. Mostrar o documento ao operador antes de salvar. **As leituras saem como
   proposta pra validar, não como fato** — e a Big Idea e os princípios
   "nunca" precisam do aceite do cliente, porque é a empresa que vai defender
   isso em público
2. Tudo que não tem evidência sai marcado ***(validar)***, e o documento abre
   dizendo o que ainda é hipótese e com quem validar
3. Salvar em `conteudo/arquitetura-editorial.md`, com `**Status:**` e data no
   topo. Registrar em `indice.md` (em "Em aberto", se ficou validação pendente)

---

## Estrutura do arquivo

```markdown
# Arquitetura editorial — <empresa>

**Status:** preenchido em AAAA-MM-DD · modo enxuto | completo
**Ainda é hipótese:** [o que está marcado (validar), e com quem validar]

## 1. Posicionamento
**Crença:** · **Big Idea:** · **Inimigo comum:** · **A posição que ninguém ocupa:**

## 2. Quem decide e as tensões
[unidade decisória] + [matriz T0, T1...] + [ativo atenção, no completo]

## 3. Por que agora            (completo)
[sinais com fonte e data — ou "menos de 4 sinais: sem janela"]

## 4. Linhas editoriais
[tabela resumo] + [uma subseção por linha: conquista, fatia, funil, fronteira,
quem alimenta, 3 exemplos]

## 5. Balanço de funil
[topo/meio/fundo em %, e o alerta]

## 6. Produtos e objeções      (completo)

## 7. Princípios "nunca"

## 8. Voz e rostos

## 9. Filtro de aprovação

## 10. Testes de atenção
[as formulações de tensão a testar no próximo calendário]

## Revisões
| Data | O que mudou | Por quê |
```

---

## Como conversa com as outras skills

| Skill | Relação |
|---|---|
| `/marca` | insumo. Voz, público e palavras proibidas entram no posicionamento |
| `/diagnostico`, `/investigar`, `/seo` | insumo. Escuta e demanda viram tensões e timing |
| `/ideias` | consome linhas, fatias e a fonte 13 (tensão). Sem arquitetura, só gera banco provisório |
| `/radar` | classifica cada pauta por linha, tensão e funil |
| `/calendario` | respeita as fatias e o balanço de funil, e reserva os testes de atenção |
| `/angulos` | escolhe família de ângulo pela linha e pela tensão da peça |
| `/revisar` | ganha o filtro de aprovação no `criterios.md` |

## Regras

- **Decisão, não diagnóstico.** Descoberta de realidade é do `/diagnostico` e
  do `/investigar`. Aqui entra o que foi *decidido* a partir deles
- **Vocabulário existente vence.** Se a empresa já chama as coisas por um nome,
  o documento adota. Renomear o que funciona é vaidade de consultor
- **Todo quadro tem critério de parada.** Fatia sem alerta de desequilíbrio,
  timing sem a regra dos 4 sinais, tensão sem grau de validação: não sai
- **"A leitura editorial é nossa"** separa dado (com fonte e data) de
  interpretação (assumida). Usar sempre que a casa interpretar
- **Hipótese marcada não é fraqueza, é honestidade.** *(validar)* em tudo que o
  cliente ainda não confirmou
- **Revalidação:** fatias em 60 a 90 dias, com resultado registrado; timing a
  cada trimestre (janela expira); tensões quando a escuta mudar; o documento
  inteiro quando a estratégia mudar. **Nunca por causa de um post que foi mal**
  — isso é `/revisar` e placar, não arquitetura
- **A complexidade fica do lado de quem opera.** O cliente recebe clareza.
  Documento que o dono não entende numa leitura está errado
