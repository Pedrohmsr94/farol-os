---
name: investigar
description: >
  Levanta matéria-prima de linguagem e de padrão pra alimentar o conteúdo, em três
  modos: "voz" (minera material real do dono pra extrair como ele fala de verdade),
  "nicho" (analisa canais e perfis de referência pra mapear ganchos, estruturas e
  temas saturados) e "comentarios" (puxa comentário real do público). Analisar,
  nunca copiar. Use quando o usuário disser "investiga", "analisa esse canal",
  "como o pessoal do nicho fala disso", "extrai comentários", "qual o tom real do
  dono", "/investigar".
---

# /investigar — Voz, padrão e linguagem real

Alimenta as outras skills com matéria-prima. Não produz peça, produz insumo.

**Saída:** `pesquisa/investigacoes/`

| Modo | O que faz | Alimenta |
|---|---|---|
| `voz` | Minera material real do dono | `/marca`, `/angulos`, `/post`, `/carrossel` |
| `nicho` | Analisa canais e perfis de referência | `/angulos`, `/calendario` |
| `comentarios` | Puxa comentário real do público | `/radar` (Radar de perguntas), `/angulos` |

Se o operador não disser o modo, perguntar. São trabalhos bem diferentes.

---

## Modo `voz` — como o dono fala de verdade

O ativo mais subaproveitado de todo cliente. Autenticidade é o que toda empresa diz
querer, e a voz já existe gravada em algum lugar — não precisa inventar persona,
precisa extrair a que existe.

**Onde procurar material:** `_memoria/fontes/` (transcrição de reunião, briefing),
áudio de WhatsApp, vídeo do Instagram, entrevista, live, conversa com cliente.

Se não houver material, pedir: **"grava três áudios de dois minutos explicando os
três serviços, do jeito que você explicaria pra um amigo."** Vale mais que qualquer
questionário.

**O que extrair:**

1. **Expressões recorrentes** — as palavras que ele usa e as que evita. Como ele
   chama o cliente, o problema, o concorrente, o produto
2. **Metáforas e comparações próprias** — as imagens que ele usa pra explicar coisa
   técnica. São ouro pra carrossel e reel
3. **Como ele explica cada serviço** — nas palavras dele, não nas do site
4. **A história de origem** — como *ele* conta: o que enfatiza, o que evita, onde pausa
5. **O que ele recusa** — o que ele critica nos outros. Vira critério negativo
6. **Ritmo de fala** — frase curta ou longa, se explica antes ou depois de afirmar.
   Serve pra roteiro soar como ele e não como texto lido

**Saída:** `pesquisa/investigacoes/voz.md`, com **citação literal** sustentando cada
observação. Observação sem citação é achismo — e a skill existe pra substituir
achismo por evidência.

Reprocessar quando entrar material novo.

---

## Modo `nicho` — o que já existe no mercado

Mapeia como o nicho comunica, pra saber o que funciona, o que está saturado e onde
tem espaço vazio.

**O que fazer:**

1. Levantar 5 a 10 perfis ou canais de referência do setor — não só os grandes.
   Perfil médio que cresce ensina mais que perfil grande que já chegou
2. Pra cada um: que formatos usa, que ganchos repete, que temas dominam, o que
   claramente performa melhor (o número está visível — usar)
3. Mapear o **saturado** — o tema que todo mundo do nicho já publicou até cansar
4. Mapear o **vazio** — a dúvida óbvia do público que ninguém está respondendo. É
   aqui que mora a oportunidade

**Saída:** `pesquisa/investigacoes/nicho-<AAAA-MM-DD>.md`, com número medido junto
de cada afirmação. "Título em caixa alta não performa" não vale nada; "título em
caixa alta, 39 views; mesmo tema com consequência no título, 4.100" vale muito.

**Analisar, nunca copiar.** O objetivo é entender a lógica, não clonar a peça.
Copiar estrutura de quem já saturou o nicho é a forma mais rápida de virar mais um.

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
   `/marca` calibrar voz e pro `/ideias` como fonte 1
2. **Dúvida concreta** — pergunta que dá pra responder com conteúdo. Vai direto pro
   `/angulos`, família "A pergunta"
3. **Ruído** — política, moralismo, autopromoção de concorrente. Descartar

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
  referência do nicho. Não tem coleta automática: os comentários do próprio perfil
  saem pela Graph API (mesma configuração do `/aprovar-post`), e os dos outros
  perfis se leem na mão
- **Grupos e fóruns** onde o público se junta
- **O WhatsApp da empresa** — a fonte mais rica e a mais ignorada. As dúvidas que
  chegam toda semana já estão lá, escritas, de graça

Transcrever **sem corrigir**: erro de português, gíria e repetição são exatamente o
dado. Agrupar por tema e marcar o que aparece várias vezes — pergunta repetida é
pauta pronta.

---

## Regras

- **Citação literal sempre.** Toda observação, nos três modos, vem com o trecho que
  a sustenta. Sem citação, é achismo com cara de pesquisa
- **Analisar, nunca copiar.** Nem texto, nem estrutura de peça, nem identidade visual
- **Não anonimizar o que é público, não expor o que é privado.** Comentário público
  pode ser citado; conversa de WhatsApp de cliente entra sem nome e sem detalhe que
  identifique
- Não transformar investigação em peça. Aqui é insumo — quem produz é o `/post`,
  `/carrossel` e `/publicar-tema`
- Investigação velha engana. Marcar a data em tudo e refazer o modo `nicho` a cada
  três meses
