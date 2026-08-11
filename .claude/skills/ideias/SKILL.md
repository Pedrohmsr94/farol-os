---
name: ideias
description: >
  Gera ideias de conteúdo que não dependem de notícia — das linhas editoriais
  perenes do cliente: dúvida real do público, objeção de venda, bastidor, prova,
  mito do setor, comparação, erro comum, glossário. Mantém as linhas editoriais e
  entrega um banco de ideias fichadas que o /calendario e o /angulos consomem.
  Use quando o usuário disser "me traz ideias", "o que postar", "acabou a pauta",
  "ideia de conteúdo", "linha editorial", "o radar não trouxe nada", "/ideias".
---

# /ideias — Banco de conteúdo perene

O `/radar` cobre a **linha de autoridade**: o que mudou lá fora e vira pauta hoje.
Ele depende de fato novo — e nem todo cliente tem fato novo toda semana.

Essa skill cobre o resto: as ideias que já existem dentro do negócio e não
envelhecem. Na maioria dos clientes, é daqui que sai **60 a 70% do calendário**.

**Entrega:** `pesquisa/ideias/AAAA-MM-DD.md` — 15 a 25 ideias fichadas, agrupadas
por linha editorial e por fonte, prontas pro `/calendario` escolher.

## Dependências

- `_memoria/empresa.md`, `_memoria/estrategia.md`
- `marca/guia-de-marca.md` — assuntos proibidos, prova disponível, voz
- `conteudo/linhas-editoriais.md` — definido na primeira rodada
- `pesquisa/investigacoes/` — voz do dono, comentários do público
- `diagnostico/diagnostico.md` — o caminho do cliente e onde ele some
- `conteudo/publicados/` — o que já foi, com resultado

---

## Primeira rodada — definir as linhas editoriais

Se `conteudo/linhas-editoriais.md` não existir, montar antes de gerar ideia.

Linha editorial não é "tipo de post". É **o que cada grupo de conteúdo tem que
conquistar** na cabeça de quem lê. Sem isso, o calendário vira lista de assunto
solto e ninguém sabe por que aquele post existe.

O padrão que serve pra quase toda empresa pequena — ajustar ao cliente:

| # | Linha | O que conquista | Fatia |
|---|---|---|---|
| 1 | **Autoridade** | "essa gente entende do assunto" | 30% |
| 2 | **Utilidade** | "isso aqui me serviu" | 30% |
| 3 | **Confiança** | "dá pra confiar neles" | 25% |
| 4 | **Oferta** | "é isso que eu preciso, e é com eles" | 15% |

A 1 é a que o `/radar` alimenta. As outras três são desta skill.

**Perguntar ao operador:**

1. "O que o cliente precisa acreditar pra fechar com essa empresa?" — cada resposta
   vira candidata a linha
2. "O que faz ele desistir no meio?" — vira a linha que ataca a objeção
3. "Quanto do mês pode ser oferta direta sem cansar?"

Escrever `conteudo/linhas-editoriais.md`: nome da linha, o que ela conquista, a
fatia do mês, e 3 exemplos de post que caberiam nela. Mostrar antes de salvar.

Revisar a cada trimestre, ou quando a estratégia mudar.

---

## As doze fontes de ideia

O trabalho não é ter criatividade. É **passar por fonte que já contém a ideia**.
Percorrer as doze, na ordem, e parar quando tiver material suficiente.

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
diferenciador que existe — e o mais difícil de copiar.

**6. A história de origem.** Por que a empresa existe, o que aconteceu antes. Usar
com parcimônia: uma vez por trimestre, não uma vez por semana.

### Do serviço

**7. O bastidor.** Como o trabalho é feito de verdade, quem faz, o que acontece
entre o "aceito" e a entrega. O cliente compra algo que não vê — mostrar reduz o
medo mais que qualquer argumento.

**8. A prova.** Caso real, número, antes e depois, depoimento. Sempre com
autorização, e anonimizado quando o setor exigir. Prova é o que a linha de
Confiança consome.

**9. Os erros que chegam prontos.** O que o cliente já fez errado antes de
procurar a empresa. Rende porque quem está cometendo o erro se reconhece na hora.

### Do setor

**10. Os mitos.** O que "todo mundo diz" e está errado ou incompleto. Cuidado: é
correção, não briga. Nunca com nome de concorrente.

**11. As comparações.** X ou Y, quando usar cada um, o que muda entre as opções.
Alto valor de salvamento, e responde a dúvida que trava a decisão.

**12. O glossário e o calendário do setor.** O termo técnico que o cliente não
entende, e as datas que se repetem todo ano — prazo, sazonalidade, período de
pico. Diferente do `/radar`: aqui não é notícia, é o ciclo que sempre volta.

---

## Workflow

### Passo 1 — Situar

Ler as dependências. Listar o que já foi publicado nos últimos 60 dias pra não
repetir, e o que rendeu (rodapé "Resultado" das peças).

### Passo 2 — Perguntar o que só o operador sabe

Três perguntas, no máximo. As fontes 1, 2, 4 e 5 dependem dele:

1. "Que pergunta chega toda semana no WhatsApp da empresa?"
2. "Das últimas pessoas que não fecharam, por que não fecharam?"
3. "O que o dono explica de novo em toda reunião — e o que dá raiva nele no setor?"

Se ele não souber, **essa é a tarefa**: pedir pra ele olhar o WhatsApp e voltar. E
registrar em `_memoria/operacao.md` que essa informação precisa entrar no ritmo.

### Passo 3 — Gerar

Percorrer as doze fontes. Pra cada ideia:

```markdown
### [Título da ideia — direto, do jeito que viraria o post]

Linha: **Utilidade** · Fonte: 2 (objeção de venda) · 🌱 perene

**A ideia:** [uma frase — o que essa peça diz]
**Pra quem:** [recorte do público]
**Por que funciona:** [a dúvida, o medo ou a objeção que ela ataca]
**Prova necessária:** [o que a empresa precisa ter pra sustentar — ou "nenhuma"]
**Formato natural:** [carrossel, reel, texto, story]
**Primeira linha:** "[escrita de verdade]"
```

**15 a 25 ideias.** Distribuídas pelas linhas na proporção do arquivo — se a linha
de Confiança é 25% do mês, ela precisa ter ideia suficiente pra isso.

Marcar `⏳ com validade` a ideia presa a data (sazonalidade, prazo do setor) e
`🌱 perene` o resto. Perene é o estoque; é o que salva a semana em que nada
aconteceu.

### Passo 4 — Entregar

Salvar em `pesquisa/ideias/AAAA-MM-DD.md` e reportar em até 10 linhas: quantas
ideias por linha, as três mais fortes, e o que ficou faltando de prova.

> "Banco atualizado: <n> ideias. <n> de Utilidade, <n> de Confiança, <n> de Oferta.
>
> Precisa de você: <lista de prova, foto ou autorização que falta>
>
> Monto o calendário com isso? (`/calendario`)"

---

## Como conversa com as outras skills

| Skill | Relação |
|---|---|
| `/radar` | cobre a linha 1 (Autoridade). Se o dia foi fraco, essa skill preenche |
| `/angulos` | pega **uma** ideia daqui e abre em 5 ângulos. Ideia ≠ ângulo |
| `/calendario` | consome o banco e distribui no mês, respeitando a proporção das linhas |
| `/investigar` | alimenta as fontes 1, 4 e 5 com material real |

**Ideia não é ângulo.** "As objeções que travam a contratação de um contador" é
ideia; "o mecanismo por trás da objeção do preço" é ângulo. O `/angulos` entra
depois, quando a ideia já foi escolhida pro calendário.

## Regras

- **Ideia que a empresa não pode sustentar não entra.** Se exige prova que ela não
  tem, ou promessa que o setor proíbe, sai da lista ou vira pedido ao cliente
- **Não gerar ideia genérica de nicho.** "5 dicas de organização financeira" serve
  pra qualquer empresa do mundo. Se a ideia não passa pelo filtro de *só essa
  empresa, com o que ela sabe, poderia publicar isso*, reescrever
- **Respeitar `marca/guia-de-marca.md`** — assunto proibido não vira ideia, nem
  "com cuidado"
- **Não esvaziar o banco de uma vez.** Ideia não usada continua valendo no mês
  seguinte. Marcar as usadas em vez de apagar
- Rodar uma vez por mês, antes do `/calendario`. Mais que isso repete; menos que
  isso deixa o calendário refém do radar
