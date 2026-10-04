---
name: ideias
description: >
  Gera ideias de conteúdo que não dependem de notícia — do que já existe dentro
  do negócio: pergunta real do público, objeção de venda, bastidor, prova, mito
  do setor, comparação, erro comum, glossário, calendário do setor e a tensão
  que ninguém verbaliza. Lê as linhas e as tensões da arquitetura editorial e
  entrega um banco fichado que o /calendario e o /angulos consomem. Use quando o
  usuário disser "me traz ideias", "o que postar", "acabou a pauta", "ideia de
  conteúdo", "o radar não trouxe nada", "/ideias".
---

# /ideias — Banco de conteúdo perene

O `/radar` cobre o que mudou lá fora e vira pauta hoje. Ele depende de fato novo
— e nem todo cliente tem fato novo toda semana. Essa skill cobre o resto: as
ideias que já existem dentro do negócio e não envelhecem. Na maioria dos
clientes, é daqui que sai **60 a 70% do calendário**; o radar é o tempero.

**Entrega:** `pesquisa/ideias/AAAA-MM-DD.md` — 15 a 25 ideias fichadas,
agrupadas por linha editorial e por fonte, prontas pro `/calendario` escolher.

**Essa skill não define linha editorial.** Quem define é o
`/arquitetura-editorial`. Skill de produção que improvisa a própria estratégia
gera banco sem direção — e o calendário herda o improviso.

## Dependências

- `_memoria/empresa.md`, `_memoria/estrategia.md` — o foco do momento manda na
  proporção do banco
- `marca/guia-de-marca.md` — voz, assuntos proibidos, prova disponível
- **A lente:** `conteudo/arquitetura-editorial.md` — linhas, fatias e a matriz de
  tensões. **Leitura obrigatória antes de gerar**
- `pesquisa/investigacoes/` — comentários do público, voz do dono, nicho
- `pesquisa/radar/` — últimos 30 dias, pra não repetir o que já veio
- `diagnostico/diagnostico.md` — o caminho do cliente e onde ele some
- `conteudo/publicados/` — o que já foi, com o rodapé "Resultado"

## Se a arquitetura editorial não existir

Se `conteudo/arquitetura-editorial.md` estiver em branco, **não improvisar
linhas aqui.** Avisar:

> "Esse repo ainda não tem arquitetura editorial — é ela que define as linhas e
> as fatias que esse banco respeita. Rodo o `/arquitetura-editorial` primeiro
> (tem modo enxuto)? Sem ela, o máximo que entrego é um banco provisório de 10
> ideias, marcado como provisório."

Se o operador pedir o provisório mesmo assim: gerar no máximo 10 ideias usando as
4 linhas do molde (Autoridade · Utilidade · Confiança · Oferta), marcar o arquivo
com `⚠️ provisório — sem arquitetura editorial` no topo, e registrar a pendência
em "Em aberto" no `indice.md`. Provisório não vira padrão: na segunda rodada
provisória seguida, parar e insistir na arquitetura.

---

## As treze fontes de ideia

O trabalho não é ter criatividade. É **passar por fonte que já contém a ideia**.
Percorrer as treze, na ordem, e parar quando tiver material suficiente.

### Do público

**1. As perguntas reais.** Comentário, review, grupo, e principalmente o WhatsApp
da empresa. Pergunta que chega três vezes por semana é o melhor post que essa
empresa pode fazer. Olhar `pesquisa/investigacoes/comentarios/` e o "Radar de
perguntas" dos briefings.

**2. As objeções de venda.** Por que as pessoas **não** fecharam. Preço, prazo,
medo, "vou pensar", "vou falar com meu sócio". Cada objeção é um post — e é o
conteúdo que mais aproxima de venda. Perguntar ao operador: "das últimas dez
pessoas que não fecharam, por que cada uma não fechou?"

**3. As perguntas que ninguém faz, mas deveria.** O que o cliente devia estar
perguntando e não pergunta porque nem sabe que existe. Rende bem porque entrega
informação que a pessoa não sabia que precisava.

### Do dono

**4. O que ele repete toda semana.** A explicação que ele dá de novo em toda
reunião. Se ele repete, é porque ninguém entende de primeira — e isso é uma pauta
que se sustenta sozinha. Fonte: `pesquisa/investigacoes/voz.md`.

**5. O que dá raiva nele.** O erro que o cliente comete, a prática do setor que ele
acha errada, o que ele corrige toda vez. Opinião com base técnica é o conteúdo mais
diferenciador que existe — e o mais difícil de copiar. **Sem nome de concorrente,
nem indireta que identifique.** E a opinião é dele: a ideia registra o que ele
disse, não uma opinião escrita no lugar dele.

**6. A história de origem.** Por que a empresa existe, o que aconteceu antes. Usar
com parcimônia: uma vez por trimestre, não uma vez por semana.

### Do serviço

**7. O bastidor.** Como o trabalho é feito de verdade, quem faz, o que acontece
entre o "aceito" e a entrega. O cliente compra algo que não vê — mostrar reduz o
medo mais que qualquer argumento.

**8. A prova.** Caso real, número, antes e depois, depoimento. Sempre com
autorização, e anonimizado quando o setor exigir. **Checar o acervo de foto e
material da empresa antes de pedir coisa nova.**

**9. Os erros que chegam prontos.** O que o cliente já fez errado antes de
procurar a empresa. Rende porque quem está cometendo o erro se reconhece na hora.

### Do setor

**10. Os mitos.** O que "todo mundo diz" e está errado ou incompleto. É correção,
nunca briga. Nunca com nome de concorrente.

**11. As comparações.** X ou Y, quando usar cada um, o que muda entre as opções.
Alto valor de salvamento, e responde a dúvida que trava a decisão.

**12. O glossário e o calendário do setor.** O termo técnico que o cliente não
entende, e as datas que se repetem todo ano — prazo, sazonalidade, período de
pico. Diferente do `/radar`: aqui não é notícia, é o ciclo que sempre volta, e dá
pra escrever com semanas de antecedência.

### Da lente

**13. A tensão que ninguém verbaliza.** O comportamento, o símbolo ou o medo que
o cliente vive mas não diz em voz alta. Sai da **matriz de tensões** da
arquitetura editorial, não de notícia nem de pergunta explícita. É a única fonte
que se escreve sem fato novo e sem caso — e é a que alimenta a tensão-mãe
diretamente. Inclui as **variações de formulação a testar** da seção "Testes de
atenção" da arquitetura: mesma tensão, formulações diferentes, medir qual prende.

---

## Workflow

### Passo 1 — Situar

Ler as dependências. Listar o que já foi publicado nos últimos 60 dias pra não
repetir, o que rendeu (rodapé "Resultado" das peças), e as pautas do radar dos
últimos 30 dias — ideia que o radar já cobriu não precisa entrar no banco perene.

Ler o banco anterior em `pesquisa/ideias/`: as ideias não usadas continuam
valendo. O banco novo completa o que falta, não recomeça do zero.

### Passo 2 — Perguntar o que só o operador sabe

Três perguntas, no máximo. As fontes 1, 2, 4 e 5 dependem dele:

1. "Que pergunta chega toda semana no WhatsApp da empresa?"
2. "Das últimas pessoas que não fecharam, por que não fecharam?"
3. "O que o dono explica de novo em toda reunião — e o que dá raiva nele no setor?"

Se ele não souber, **essa é a tarefa**: pedir pra ele olhar o WhatsApp e voltar.
Gerar o banco com as outras fontes, marcar no relatório o que ficou faltando, e
registrar em `_memoria/operacao.md` que essa informação precisa entrar no ritmo.

### Passo 3 — Gerar

Percorrer as treze fontes. Pra cada ideia:

```markdown
### [Título da ideia — direto, do jeito que viraria o post]

Linha: **<da arquitetura>** · Fonte: 2 (objeção) · Tensão: T2 · Funil: meio · 🌱 perene

**A ideia:** [uma frase — o que essa peça diz]
**Pra quem:** [recorte do público — se a arquitetura definir dupla que decide,
dizer com qual metade fala]
**Por que funciona:** [a dúvida, o medo ou a objeção que ela ataca]
**Prova necessária:** [o que a empresa precisa ter pra sustentar — ou "nenhuma"]
**Formato natural:** [um só: carrossel, reel, artigo, story, LinkedIn]
**Primeira linha:** "[escrita de verdade, no vocabulário do cliente final]"
```

**O rastreio é duplo, e os dois são obrigatórios:**

- **Fonte** (campo `Fonte:`) — de onde a ideia veio, uma das treze. Ideia que
  nasce de opinião solta não entra
- **Tensão** (campo `Tensão:`) — pra onde a ideia puxa, da matriz da arquitetura.
  Ideia que não puxa pra tensão nenhuma é ideia órfã: pode ser boa e mesmo assim
  não construir nada. Órfã só entra marcada como **teste**, no máximo 2 por banco

**15 a 25 ideias**, distribuídas pelas linhas na proporção da arquitetura — se uma
linha é 25% do mês, precisa ter ideia suficiente pra isso. Marcar
`⏳ com validade` a ideia presa a data e `🌱 perene` o resto. Perene é o estoque —
é o que salva a semana em que nada aconteceu.

### Passo 4 — Entregar

Salvar em `pesquisa/ideias/AAAA-MM-DD.md` e reportar em até 10 linhas:

> "Banco atualizado: <n> ideias. <distribuição por linha>. <n> puxam pra
> tensão-mãe, <n> pras tensões-porta, <n> teste.
>
> Precisa de você: <prova, foto ou autorização que falta>
>
> Abro uma em ângulos (`/angulos`) ou monto o mês (`/calendario`)?"

---

## Como conversa com as outras skills

| Skill | Relação |
|---|---|
| `/arquitetura-editorial` | define as linhas, as fatias e as tensões que esse banco respeita. Sem ela, só banco provisório |
| `/radar` | cobre o fato novo, e marca quando uma pauta reforça ideia do banco. Rodada fraca? o banco perene preenche |
| `/angulos` | pega **uma** ideia daqui e abre em ângulos. Ideia ≠ ângulo |
| `/calendario` | consome o banco e distribui no mês, respeitando a proporção |
| `/investigar` | alimenta as fontes 1, 4 e 5 com material real |
| `/revisar` | obrigatório antes de publicar — o banco não pula essa etapa |

**Ideia não é ângulo.** "As objeções que travam a contratação" é ideia; "o
mecanismo por trás do medo do preço" é ângulo. O `/angulos` entra depois, quando
a ideia já foi escolhida.

## Regras

- **Rastreio duplo em toda ideia:** fonte (de onde veio) + tensão (pra onde puxa).
  Ver Passo 3
- **Ideia que a empresa não pode sustentar não entra.** Se exige prova que ela não
  tem, ou promessa que o setor proíbe, sai da lista ou vira pedido ao cliente
- **Não gerar ideia genérica de nicho.** "5 dicas de organização financeira" serve
  pra qualquer empresa do mundo. Filtro: *só essa empresa, com o que ela viu e
  sabe, poderia publicar isso*
- **Respeitar `marca/guia-de-marca.md`** — assunto proibido não vira ideia, nem
  "com cuidado"
- **Capacidade real antes de captação.** Se o banco inteiro virar geração de
  demanda num mês em que a operação não absorve, sinalizar
- **Não esvaziar o banco de uma vez.** Ideia não usada continua valendo no mês
  seguinte. Marcar as usadas em vez de apagar
- Rodar **uma vez por mês, antes do `/calendario`**. Mais que isso repete; menos
  que isso deixa o calendário refém do radar
