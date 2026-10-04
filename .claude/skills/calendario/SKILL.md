---
name: calendario
description: >
  Monta a pauta do mês a partir do objetivo da estratégia, das fatias e do
  balanço de funil da arquitetura editorial, do que já rendeu nos posts
  publicados, do estoque de pesquisa (banco de ideias, radar, ângulos guardados)
  e das datas do setor, e escreve em `conteudo/calendario.md`. Use quando o
  usuário disser "montar a pauta", "calendário do mês", "o que vamos postar",
  "planejar conteúdo", "/calendario".
---

# /calendario — A pauta do mês

Roda uma vez por mês, antes de escrever qualquer post.

Pauta não é lista de assunto bonito. É a tradução do objetivo do trimestre em
coisas publicáveis — e se não der pra dizer como um tema ajuda o objetivo, ele
não entra.

**Saída:** uma seção nova no topo de `conteudo/calendario.md`.

---

## Passo 1 — Ler antes de propor

- `_memoria/estrategia.md` — o objetivo do trimestre e as datas com prazo
- `_memoria/empresa.md` — o que ela vende, pra quem, sazonalidade
- `_memoria/operacao.md` — **quantas entregas o contrato prevê**
- `marca/guia-de-marca.md` — voz, assuntos proibidos, prova disponível
- **A lente:** `conteudo/arquitetura-editorial.md` — as linhas, **a fatia de cada
  uma e o balanço de funil** (ex.: 60% topo · 25% meio · 15% fundo), e os testes
  de atenção. É ela que define a mistura. Se estiver em branco, rodar
  `/arquitetura-editorial` antes — ou marcar o mês como provisório
- `conteudo/publicados/` — o rodapé "Resultado" dos últimos dois meses
- `conteudo/calendario.md` — o que ficou como `pauta` e nunca foi escrito

**E o estoque de pesquisa, que é de onde a pauta deve sair:**

- `pesquisa/ideias/` — o banco perene, por linha. Na maioria dos clientes é daqui
  que sai o grosso do mês
- `pesquisa/radar/resumo-semanal-*.md` — as pautas mais fortes de cada semana
- `pesquisa/radar/` — os briefings do mês, incluindo os "Sinais fracos" que
  cresceram e as perguntas capturadas do público
- `pesquisa/angulos/` — **os ângulos que foram gerados e não viraram peça**. Cada
  um é uma pauta pronta, com tese e primeira linha escritas. Olhar aqui antes de
  inventar tema novo
- `pesquisa/seo/05-estrategia-conteudo.md` — a lista mestra de temas com demanda,
  se o `/seo` rodou
- O calendário do setor em `pesquisa/fontes.md` — **antecipar pico de busca em 6
  a 8 semanas**

Se o estoque estiver vazio, avisar:

> "Não tem pesquisa no estoque, então essa pauta vai sair de contexto e não de
> varredura. Rodo o `/radar` e o `/ideias` antes? Muda a qualidade do mês
> inteiro."

Se o guia de marca estiver em branco, avisar e perguntar se segue assim mesmo.

Se `_memoria/estrategia.md` não tiver objetivo do trimestre, parar e perguntar.
Pauta sem objetivo é conteúdo por conteúdo — é exatamente o que o cliente já
fazia antes de contratar.

---

## Passo 2 — Olhar o que rendeu

Dos posts publicados com resultado preenchido: quais formatos, temas, linhas e
aberturas performaram, e quais não. Cruzar com o placar da conta,
`pesquisa/investigacoes/desempenho/perfil-de-desempenho.md`, se existir — ele diz
a mediana de cada formato nessa conta e como abrem os posts que mais entregam.

Se nenhum post tem resultado preenchido, dizer:

> "Nenhum post publicado tem resultado registrado, então essa pauta é aposta,
> não leitura. Vou marcar dois temas como teste pra gente ter o que medir mês
> que vem."

Repetir o que funcionou é o trabalho — não é falta de criatividade.

---

## Passo 3 — Montar

**Quantidade:** a do contrato. Nem mais nem menos. Propor 12 posts num contrato
de 8 gera atraso e fila entupida.

**Mistura.** A proporção vem da arquitetura editorial — linhas e funil. Quem
manda é o arquivo do cliente, não um padrão.

Mês todo em autoridade constrói reputação e não vende. Mês todo em oferta cansa e
some do alcance.

Fora da proporção, reservar **1 a 2 testes**: ângulo, formato novo ou uma
formulação de tensão da seção "Testes de atenção" da arquitetura, pra ter o que
medir no mês seguinte.

Se uma linha não tiver ideia suficiente no banco pra preencher a fatia dela,
dizer isso em vez de forçar tema fraco — e apontar qual fonte do `/ideias` está
seca.

**Datas.** Cruzar com o que tem prazo — sazonalidade do setor, fechamento,
feriado que muda o horário, evento da cidade, o calendário do setor.

**Cada tema precisa responder:**

1. Que dúvida, objeção ou tensão ele ataca?
2. Como ele ajuda o objetivo do trimestre?
3. A empresa tem prova pra sustentar o que vai afirmar?
4. **De qual pesquisa ele nasceu?** Banco de ideias, briefing do `/radar`,
   documento de ângulos, tema de SEO ou pergunta real capturada do público — com
   o caminho do arquivo

Se a 3 for não, o tema muda ou entra como pedido ao cliente ("preciso de uma
foto do serviço pronto pra esse aqui").

Se a 4 for "de nenhuma", o tema não entra. Ele seria reprovado no `/revisar`
depois de escrito, e aí o trabalho já foi feito.

---

## Passo 4 — Escrever no calendário

Seção nova no topo de `conteudo/calendario.md`:

```markdown
## Setembro/2026

**Objetivo do mês:** <como esse mês empurra o objetivo do trimestre>

| Data | Tema | Linha | Funil | Tensão | Formato | Canal | Status | Origem | Arquivo |
|---|---|---|---|---|---|---|---|---|---|
| 03/09 | Quanto custa atrasar a entrega do IR | Utilidade | meio | T2 | carrossel | Instagram | pauta | ideias 30/08 | 2026-09-03-atraso-ir |
| 10/09 | [formulação B da T0] | Confiança | topo | T0 | reel | Instagram | pauta · teste | arquitetura, testes de atenção | 2026-09-10-... |
```

Nome do arquivo já definido aqui (`AAAA-MM-DD-tema-curto`), mesmo antes de
existir — é assim que o `/post`, o `/carrossel` e o `/publicar-tema` sabem onde
salvar em `conteudo/fila/`.

A coluna **Origem** aponta a pesquisa de onde o tema saiu. Ela é o que permite,
no fim do mês, responder se o conteúdo veio de pesquisa ou de improviso.

---

## Passo 5 — Fechar

Mostrar a tabela e:

```
<n> pautas pra <mês>.
Linhas: <distribuição> · Funil: <topo/meio/fundo> · testes: <n>
Origem: <n> do banco de ideias · <n> do radar · <n> de ângulos guardados · <n> de SEO

Preciso de você: <lista do que depende do cliente — foto, dado, autorização>

Escrevo o primeiro agora? (/angulos → /post, /carrossel ou /publicar-tema)
```

Atualizar `indice.md` se alguma pauta virou pendência com o cliente.

---

## Regras

- **Não estourar o contrato.** Se o operador quiser mais, avisar que isso é
  trabalho fora do combinado antes de escrever a pauta
- **Não propor tema sem prova.** Conteúdo que afirma o que a empresa não pode
  sustentar é risco, principalmente em setor regulado
- **Não copiar trend.** Se sugerir formato que está bombando, dizer o que ele
  resolve pra esse cliente. Sem isso, não entra
- **Respeitar o balanço de funil.** Se uma semana está cheia de fundo, dizer — o
  desequilíbrio tem consequência conhecida: só topo atrai e não aquece; só meio
  aquece e não cresce; só fundo vende pra ninguém
- Pauta antiga que nunca foi escrita: perguntar se entra nesse mês ou é
  descartada. Não deixar apodrecer no arquivo
