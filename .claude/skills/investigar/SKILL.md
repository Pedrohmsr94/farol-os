---
name: investigar
description: >
  Levanta matéria-prima de linguagem e de padrão pra alimentar o conteúdo, em
  quatro modos: "voz" (minera material real do dono pra extrair como ele fala de
  verdade), "nicho" (analisa canais e perfis de referência pra mapear ganchos,
  estruturas e temas saturados, e mede a saturação de anúncios ativos na
  Biblioteca de Anúncios do Meta), "comentarios" (puxa comentário real do público
  no YouTube via yt-dlp) e "reel" (baixa um reel que estourou, transcreve com
  Whisper local e lê gancho, estrutura e ritmo por tempo). Analisar, nunca
  copiar. Use quando o usuário disser "investiga", "analisa esse canal", "como o
  pessoal do nicho fala disso", "extrai comentários", "qual o tom real do dono",
  "quantos anúncios ativos tem nesse tema", "biblioteca de anúncios", "analisa
  esse reel", "por que esse vídeo bombou", colar URL de reel, ou "/investigar".
---

# /investigar — Voz, padrão e linguagem real

Alimenta as outras skills com matéria-prima. Não produz peça, produz insumo.

**Saída:** `pesquisa/investigacoes/`

| Modo | O que faz | Alimenta |
|---|---|---|
| `voz` | Minera material real do dono | `/marca`, `/angulos`, `/post`, `/carrossel` |
| `nicho` | Analisa canais, perfis de referência e a Biblioteca de Anúncios | `/angulos`, `/calendario`, `/arquitetura-editorial` |
| `comentarios` | Puxa comentário real do público no YouTube | `/radar` (Radar de perguntas), `/ideias`, `/angulos` |
| `reel` | Transcreve um reel de referência e lê a estrutura por tempo | `/angulos` (roteiro de reel) |

Se o operador não disser o modo, perguntar. São trabalhos bem diferentes. URL de
reel colada sem mais nada é modo `reel`.

---

## Modo `voz` — como o dono fala de verdade

O ativo mais subaproveitado de todo cliente. Autenticidade é o que toda empresa diz
querer, e a voz já existe gravada em algum lugar — não precisa inventar persona,
precisa extrair a que existe.

**Onde procurar material:** `_memoria/fontes/` (transcrição de reunião, briefing),
áudio de WhatsApp, vídeo do Instagram, entrevista, live, conversa com cliente.
Áudio ou vídeo ainda sem texto passa antes pelo `/transcrever`; este modo lê o que
ele produz.

Se não houver material, pedir: **"grava três áudios de dois minutos explicando os
três serviços, do jeito que você explicaria pra um amigo."** Vale mais que qualquer
questionário.

**O que extrair:**

1. **Expressões recorrentes** — as palavras que ele usa e as que evita. Como ele
   chama o cliente, o problema, o concorrente, o dinheiro, o produto
2. **Metáforas e comparações próprias** — as imagens que ele usa pra explicar coisa
   técnica. São ouro pra carrossel e reel
3. **Como ele explica cada serviço** — nas palavras dele, não nas do site
4. **A história de origem** — como *ele* conta: o que enfatiza, o que evita, onde pausa
5. **O que ele recusa** — o que critica nos outros, o território que não entra.
   Vira critério negativo no bloqueio 10 do `criterios.md` do `/revisar`
6. **Ritmo de fala** — frase curta ou longa, se explica antes ou depois de afirmar.
   Serve pra roteiro soar como ele e não como texto lido
7. **As opiniões dele** — o que ele pensa de verdade sobre o setor, com a frase
   dele. É daqui que peça de opinião tira a raiz (bloqueio 9 do `/revisar`)

**Saída:** `pesquisa/investigacoes/voz.md`, com **citação literal** sustentando cada
observação. Observação sem citação é achismo — e a skill existe pra substituir
achismo por evidência.

Reprocessar quando entrar material novo.

---

## Modo `nicho` — o que já existe no mercado

Mapeia como o nicho comunica, pra saber o que funciona, o que está saturado e onde
tem espaço vazio. Duas perguntas guiam tudo: o que já está saturado (pra não
repetir) e o que ninguém está dizendo (a brecha).

### Como levantar

1. Levantar 5 a 10 perfis ou canais de referência do setor — não só os grandes.
   Perfil médio que cresce ensina mais que perfil grande que já chegou
2. Pra cada um: que formatos usa, que ganchos repete, que temas dominam, o que
   claramente performa melhor (o número está visível — usar)

**YouTube** — não adivinhar a URL do canal, descobrir pela busca:

```bash
python -m yt_dlp "ytsearch3:<nome do canal>" --skip-download --no-warnings \
  --print "%(channel)s | %(channel_url)s"
```

Com a URL, listar os vídeos com audiência — é o que revela qual gancho pegou:

```bash
python -m yt_dlp "<channel_url>/videos" --flat-playlist --playlist-end 30 \
  --no-warnings --print "%(view_count)s | %(title).90s"
```

**Instagram** — os coletores em `scripts/coletores/` (cada um explica o uso no
cabeçalho do arquivo):

- `instagram.js` — o número público do perfil (seguidores, posts, bio), sem custo
- `apify.py` — os posts do perfil com curtida e comentário, pelo Apify. Salva o
  bruto em `pesquisa/coleta/raw/<nome>.json`. **Cobra por execução** e precisa de
  `APIFY_TOKEN` no `.env`: um perfil por chamada, volume pequeno
- `resumir-perfil.py` — lê esse bruto e monta o resumo do perfil com os posts que
  mais engajaram
- `baixar-referencias.py` — baixa capa, slides e vídeo dos posts coletados. Os
  links do Instagram expiram em dias: rodar no mesmo dia da coleta

Sem `APIFY_TOKEN`, ler o perfil na mão e anotar o número com a data.

### O que produzir

- **Padrão de gancho** — como os títulos e capas que performaram acima da média
  daquele perfil são construídos. **Comparar com a mediana do próprio perfil, não
  com número absoluto**: 100 mil views num canal de 2 milhões é fracasso
- **Saturado** — o tema que todo mundo do nicho já publicou até cansar. Só entrar
  com ângulo novo
- **Vazio** — a dúvida óbvia do público que ninguém está respondendo bem. É aqui
  que mora a oportunidade
- **Registro e tom** — formal, técnico, de igual pra igual, professoral
- **O que NÃO fazer** — vício do nicho que contraria o posicionamento: promessa de
  resultado, tom de guru, capa alarmista. Vira entrada no bloqueio 10 do
  `criterios.md`

**Saída:** `pesquisa/investigacoes/nicho-<AAAA-MM-DD>.md`, com número medido junto
de cada afirmação. "Título em caixa alta não performa" não vale nada; "título em
caixa alta, 39 views; mesmo tema com consequência no título, 4.100" vale muito.

**Analisar, nunca copiar.** O relatório descreve padrão estrutural, nunca entrega
frase pronta pra reaproveitar. Copiar estrutura de quem já saturou o nicho é a
forma mais rápida de virar mais um.

### A Biblioteca de Anúncios — saturação medida, não sentida

Antes de ordenar a pauta ou gastar gravação, medir quantos anúncios **ativos**
existem em cada território de tema. A Biblioteca de Anúncios do Meta é pública —
facebook.com/ads/library, filtrar país, "todos os anúncios", status ativo — e
não precisa de conta, de chave nem de API.

**Como fazer:**

1. Buscar cada território com as palavras do público (`pesquisa/vocabulario.md`
   ajuda) e anotar o número de anúncios ativos por termo
2. Classificar: **saturado** (centenas), **vazio** (menos de dez), **deserto**
   (zero). Conferir quem são os poucos do vazio — às vezes nem são do nicho
3. Cruzar com a capacidade de entrega (`_memoria/empresa.md`): o território
   vazio que a operação aguenta em volume é o único em que o CTA pode abrir
   em vez de qualificar
4. Ler o padrão dos saturados, **sem citar nome**: como qualificam, que CTA
   usam, que posicionamento repetem. O que ninguém está fazendo ali é o
   registro que sobra — e costuma ser prova técnica e procedimento
5. Cruzar com `pesquisa/investigacoes/comentarios/`: a dor mais curtida que
   nenhum anúncio toca é a maior abertura do conjunto

Medido no projeto que originou esse método, no mesmo dia: o território óbvio
tinha **551** anúncios ativos; o território ao lado, que respondia por quase
metade do mercado real, tinha **9**. A ordem de gravação inverteu na hora — e
é esse tipo de decisão que essa varredura existe pra tomar.

O número muda toda semana: datar a varredura e refazer junto com o modo
`nicho`. Quando o nicho anuncia em busca, a Central de Transparência do Google
(adstransparency.google.com) serve pro mesmo movimento.

Aqui o anúncio é **sinal de saturação de tema**, não estudo de campanha paga — o
Farol OS é orgânico. O que se lê é onde o mercado já grita e onde está quieto.

**Saída:** `pesquisa/investigacoes/anuncios-<AAAA-MM-DD>.md`. O resultado
alimenta a ordem do `/calendario` e o campo "Risco" de cada peça no `/angulos`.

---

## Modo `comentarios` — a voz do público, sem filtro

A fala literal do público é o insumo mais valioso do sistema inteiro, e o mais
difícil de conseguir por busca aberta.

**Script pronto:** `scripts/coletar-comentarios.py` (requer `pip install yt-dlp`)

```bash
python scripts/coletar-comentarios.py \
  --busca "nao consigo pagar meu contador" "abri empresa e me arrependi" \
          "caí na malha fina o que fazer" \
  --videos 6 --comentarios 60
```

### A regra que decide se isso funciona

**Sempre buscar com as palavras do público, nunca com as do especialista.** Não é
detalhe de estilo. Medido no projeto que originou esse método, mesma ferramenta,
mesmo dia:

| Busca | Comentários úteis |
|---|---|
| vocabulário técnico do especialista | **6** |
| vocabulário do público, 4 variações | **655** |

Cem vezes mais material, mesma ferramenta. A diferença foi só a escolha das
palavras.

Como achar as palavras certas: pegar a dor, não o serviço. Não "planejamento
tributário" e sim "tô pagando imposto demais". Não "assessoria contábil" e sim
"meu contador some". Não "reestruturação" e sim "não consigo pagar as contas".

Termo que funcionar vai pra `pesquisa/vocabulario.md`, na tabela de buscas — e o
que não funcionar também, na lista de baixo. Repetir busca que deu certo é mais
barato que inventar termo novo toda rodada.

### Onde o público não fala

Também medido: quem tem problema grande e nome a zelar na cidade **pesquisa, não
comenta**. Se duas rodadas com vocabulário certo voltam vazias, não é termo
errado, é canal errado. Aí a escuta é busca (Google, `/seo`) e balcão (as
perguntas que já chegam no WhatsApp da empresa), não comentário. Registrar isso
no `leitura-<data>.md` e parar de insistir.

### O que o script já faz

Descarta elogio solto e saudação, e **ordena por sinal em vez de curtida**. Isso é
deliberado: ordenar por curtida parece óbvio e entrega o contrário do que serve,
porque o YouTube premia indignação e enterra a dor real embaixo de discussão
política. Relato em primeira pessoa com vocabulário concreto vem primeiro; briga
política vai pro fim.

O vocabulário concreto do nicho ele lê de `pesquisa/vocabulario.md`. Sem esse
arquivo o script roda, mas ordena pior — na primeira rodada, preencher com as
palavras que aparecem no material e rodar de novo.

### A triagem fina é sua

O script faz a grossa. Ao ler o corpus, separar em três:

1. **Dor real** — pessoa falando da própria situação. É o material nobre: vai pro
   `/marca` calibrar voz, pro `/ideias` como fonte 1 e pra matriz de tensões do
   `/arquitetura-editorial`
2. **Dúvida concreta** — pergunta que dá pra responder com conteúdo. Vai direto pro
   `/angulos`, família "A pergunta"
3. **Ruído** — política, moralismo, autopromoção. Descartar

**Saída:** o script salva sozinho em
`pesquisa/investigacoes/comentarios/<termo>-<AAAA-MM-DD>.md`.

Ao terminar, escrever ao lado um `leitura-<data>.md` com o que a triagem achou. O
corpus é grande demais pra alguém reler inteiro depois — se a leitura não for
escrita, o trabalho se perde.

### Fora do YouTube

O script só cobre YouTube. As outras fontes são na mão, e valem:

- **Reviews do Google** — do cliente e dos concorrentes. Reclamação de concorrente
  é o mapa do que o cliente pode prometer
- **Instagram** — comentários nos posts do próprio cliente e nos perfis de
  referência do nicho. Os do próprio perfil saem pela Graph API (mesma
  configuração do `/aprovar-post`); os dos outros perfis, pelo `apify.py` do modo
  `nicho` ou na mão
- **Grupos e fóruns** onde o público se junta
- **O WhatsApp da empresa** — a fonte mais rica e a mais ignorada. As dúvidas que
  chegam toda semana já estão lá, escritas, de graça

Transcrever **sem corrigir**: erro de português, gíria e repetição são exatamente o
dado. Agrupar por tema e marcar o que aparece várias vezes — pergunta repetida é
pauta pronta.

---

## Modo `reel` — por que aquele vídeo entregou

O modo `nicho` lê título e view de perfil; este lê **o vídeo por dentro**: o que é
dito nos 3 primeiros segundos, onde muda de bloco, quanto dura cada parte, qual o
ritmo de fala. É de onde sai o molde de roteiro que o `/angulos` aplica — o molde,
nunca a frase.

**Script pronto:** `scripts/reel-referencia.py`. Baixa com yt-dlp (Instagram,
TikTok, Shorts) e transcreve com faster-whisper local, offline — nada sai da
máquina. Requer `pip install yt-dlp faster-whisper`.

```bash
python scripts/reel-referencia.py "https://www.instagram.com/reel/XXXX/"
python scripts/reel-referencia.py caminho/do/video.mp4 --slug nome-curto
python scripts/reel-referencia.py "<url>" --cookies chrome   # se o Instagram bloquear anônimo
```

Sai em `pesquisa/investigacoes/reels/<slug>/`: `video.mp4`, `meta.json` (views,
curtidas, duração, conta de origem) e `transcricao.md` — transcrição por tempo com
o esqueleto da análise no fim. Um reel de 60s leva uns 4 minutos na CPU.

**O que preencher no esqueleto** (é análise, não resumo):

1. **Gancho, 0–3s** — a frase literal e o mecanismo: número, contradição, pergunta
   do público, cena, confissão. Se o gancho é "oi pessoal", anotar isso também — é
   dado sobre o que a audiência tolera
2. **Estrutura por tempo** — os blocos e a duração de cada um, contra o molde do
   `/angulos` (0–3 · 3–10 · 10–35 · 35–50 · 50–60). Fato antes da implicação ou
   depois? Quantos pontos cabem?
3. **Ritmo** — palavras por minuto (a ficha calcula), tamanho de frase, pausa,
   texto na tela
4. **Por que funcionou** — hipótese com evidência. Views contra a mediana da conta
   de origem, nunca contra número absoluto
5. **O que serve pra nós** — o padrão estrutural, dito de forma que o `/angulos`
   consiga aplicar num ângulo diferente. Exemplo bom: "abre com a consequência
   concreta e só explica o mecanismo aos 20s". Exemplo proibido: a frase do vídeo
6. **O que NÃO copiar** — promessa, alarmismo, tom de guru, ataque. Vira entrada no
   bloqueio 10 do `criterios.md`

Rodar em **3 a 5 reels** antes de escrever molde — um vídeo é anedota. Quando
houver padrão, consolidar em `pesquisa/investigacoes/reels/leitura-<AAAA-MM-DD>.md`
e apontar de lá pro `/angulos`.

---

## O placar da própria conta

Não é modo de investigação — é o dado que o `/revisar` consulta no passo 3b e que o
`/calendario` e o `/angulos` usam pra escolher formato. Mora aqui porque o script é
irmão dos outros.

```bash
python scripts/perfil-de-desempenho.py --posts 40
python scripts/perfil-de-desempenho.py --posts 40 --excluir <id>,<id>   # posts impulsionados
```

Lê o token da Meta do `.env` da raiz — a mesma configuração do `/aprovar-post`.
Puxa alcance, salvamento e compartilhamento por post pela Graph API, separa por
formato, lista os 25% melhores e os 25% piores. Sai em
`pesquisa/investigacoes/desempenho/` — o arquivo datado fica como histórico;
`perfil-de-desempenho.md` é sempre o mais recente.

Post impulsionado tem alcance pago misturado e a API não separa por post. Passar os
IDs dele em `--excluir`; sem isso, o relatório avisa. Métrica que a API não devolve
fica em branco — nunca preenchida com estimativa.

Refazer todo mês, antes do `/calendario`.

---

## Regras

- **Citação literal sempre.** Toda observação, nos quatro modos, vem com o trecho
  ou o número que a sustenta. Sem isso, é achismo com cara de pesquisa
- **Analisar, nunca copiar.** Nem texto, nem estrutura de peça, nem identidade
  visual. O produto é padrão, brecha e vocabulário — nunca frase pronta de terceiro
- **Concorrente não entra pelo nome** no que vai pra peça. No arquivo de
  investigação o perfil pode ser identificado (é material interno); no que sai pro
  conteúdo, nunca
- Comentário de terceiro e vídeo baixado são **matéria-prima interna**. Não
  publicar print, não republicar, não recortar, não citar autor. O que sai pro
  conteúdo é a *dúvida* ou o *padrão*, reescritos — não a pessoa
- **Não expor o que é privado.** Conversa de WhatsApp de cliente entra sem nome e
  sem detalhe que identifique
- Não transformar investigação em peça. Aqui é insumo — quem produz é o `/post`,
  `/carrossel` e `/publicar-tema`. O valor está em ter o material pronto quando a
  pauta pedir
- Investigação velha engana. Marcar a data em tudo, refazer o modo `nicho` e a
  Biblioteca a cada três meses, os comentários a cada duas semanas de uso ativo, o
  placar todo mês
