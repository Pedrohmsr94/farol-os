---
name: publicar-tema
description: >
  Orquestra a criação completa de uma peça a partir de um tema — escolhe o ângulo
  com o /angulos, escreve o artigo de blog, gera o carrossel resumo com o
  /carrossel e produz as legendas pra Instagram, Facebook e LinkedIn, tudo
  amarrado e passando pelo /revisar. Use quando o usuário pedir "publicar tema",
  "gera o conteúdo do tema X", "transforma essa pauta em post", "cria o conteúdo
  completo", "/publicar-tema".
---

# /publicar-tema — Pipeline completo de uma peça

Skill orquestradora. Tema → artigo + carrossel + 3 legendas, tudo conectado e
revisado.

## Dependências

- **Pauta:** `conteudo/calendario.md` primeiro; depois `pesquisa/radar/`,
  `pesquisa/ideias/` e os ângulos guardados em `pesquisa/angulos/`
- **A lente:** `conteudo/arquitetura-editorial.md` — linha, tensão e funil da peça
- **Temas e demanda de SEO:** `pesquisa/seo/05-estrategia-conteudo.md` e os outros
  passos do `/seo`, se rodou
- **Skills no fluxo:** `/angulos` (passo 1), `/carrossel` (passo 4), `/revisar`
  (passo 6, obrigatório)
- **Voz:** `marca/guia-de-marca.md`, `pesquisa/investigacoes/voz.md` se existir
- **Placar:** `pesquisa/investigacoes/desempenho/perfil-de-desempenho.md`, se
  existir
- **Saída:** `conteudo/fila/<AAAA-MM-DD>-<slug>/`

---

## Workflow

### Passo 0 — O tema

Se o operador passou tema explícito, usar.

Se não, **abrir `conteudo/calendario.md`** e listar as pautas do mês ainda em
`pauta`. Cada uma já tem linha, tensão, origem e o nome do arquivo definido — usar
esse nome pra pasta. Calendário vazio: listar as pautas ainda não usadas dos
briefings recentes em `pesquisa/radar/` e as ideias do banco em `pesquisa/ideias/`.
Só recorrer à estratégia de SEO se nada disso servir.

Checar `conteudo/publicados/` pra não duplicar.

**Se a pauta trouxer campo "Atenção"**, esse aviso viaja com o tema até o fim e é
verificado no passo 6.

Se o tema não tiver raiz de pesquisa nenhuma, dizer antes de escrever: a peça vai
ser reprovada no `/revisar` (bloqueio 9). Rodar `/radar` ou `/ideias` resolve.

### Passo 1 — Ângulo

**Não escolher o ângulo sozinho.** Rodar `/angulos`: ele devolve 5 ângulos de
famílias diferentes e, depois da escolha, mostra como aquele ângulo vira cada
formato.

Se o operador escolher reel ou vídeo, o `/angulos` entrega o roteiro e **essa skill
não é a certa** — ver "Quando NÃO usar". Se o placar da conta mostra que carrossel
entrega bem abaixo de reel, dizer isso aqui, com o número, antes de seguir.

Se o ângulo escolhido for de opinião, a tese precisa da resposta do dono antes do
passo 3. Sem ela, parar e pedir.

Os ângulos não escolhidos ficam salvos e viram pauta futura no `/calendario`.

### Passo 2 — Pesquisa rápida

Antes de escrever:

- Palavra-chave principal e variações (`pesquisa/seo/01-pesquisa-demanda.md`)
- Como o mercado trata o assunto (`pesquisa/seo/02-analise-concorrencia.md`) — pra
  fugir do óbvio
- Ângulo GEO se aplicável (`pesquisa/seo/07-geo.md`) — a pergunta que as IAs
  respondem
- Se existir `pesquisa/investigacoes/comentarios/`, procurar a dúvida real sobre
  esse tema. Artigo que responde pergunta feita de verdade rende mais que artigo
  que responde pergunta imaginada

### Passo 3 — O artigo

**Destino:** `conteudo/fila/<AAAA-MM-DD>-<slug>/artigo.md`

Se o cliente tem site e você sabe o formato dele, escrever já no formato do site
(HTML estático, markdown com frontmatter, o que for) e dizer qual é. Com
frontmatter, sempre começar como rascunho (`draft: true` ou o equivalente) — quem
publica é o `/aprovar-post`. Se não tem site, o artigo continua valendo — é a
peça-mãe de onde o carrossel e as legendas derivam, e vira post de LinkedIn ou
material de WhatsApp.

**Slug:** kebab-case curto, sem palavra vazia. "Como conservar carne salgada no
restaurante" → `conservar-carne-salgada`.

**Estrutura (800-1500 palavras):**

1. **Lead (1-2 parágrafos)** — o problema concreto do público, sem enrolação
2. **H2 explicativo** — o quê e por quê
3. **H2 prático** — como fazer, o que olhar
4. **H2 comparativo ou técnico** (opcional)
5. **H2 onde a empresa se encaixa** — conexão natural, sem virar propaganda
6. **CTA final** — WhatsApp, formulário, contato

**Escrita:** frase curta, parágrafo de 2-4 linhas, concreto (número com fonte e
data, valor com enquadramento), sem jargão que o público não usa, sem travessão.
Seguir `marca/guia-de-marca.md` estritamente.

### Passo 4 — Carrossel resumo

Sem perguntar, partir pro `/carrossel` (tipo 1, texto puro), na **mesma pasta**.

- **Capa:** o título do artigo, ou variação enxuta
- **Slides 2-6:** os pontos-chave (uma ideia por slide, frase natural, não bullet seco)
- **Slide final:** CTA pro artigo

Capa seguindo a sequência alternada do feed — checar `conteudo/publicados/`.

### Passo 5 — Legendas

Na mesma pasta:

**`legenda.md`** (Instagram + Facebook — mesmo texto):

- Gancho na primeira linha
- 2-3 parágrafos de contexto, frase natural
- CTA pro carrossel + CTA pro artigo (link na bio ou URL direta)
- Bloco da empresa (o que faz, contato)
- 10-15 hashtags (público + nicho + cidade se for negócio local)

**`legenda-linkedin.md`** — texto próprio, não é a legenda do Instagram encurtada.

O LinkedIn corta o post em "…ver mais" por volta de 210 caracteres. Tudo que
convence a abrir tem que caber antes do corte. E o post é lido no celular: linha
longa vira parede de texto. Regras de formato (mecânica, não voz — voz continua
sendo o guia de marca):

- **Gancho: 2 linhas, até 40 caracteres cada.** A primeira afirma algo concreto
  (número, nome, fato); a segunda contradiz, vira ou puxa. Sem pergunta na
  abertura. Escrever 3 opções em ângulos diferentes (número · contrário ·
  antes/depois) e escolher uma — não entregar as três
- **Uma frase por linha, linha em branco entre cada.** Até 55 caracteres por
  linha. No máximo 4 linhas podem ser mini-parágrafo de 2-3 frases (até 110
  caracteres)
- **200 a 250 palavras, no máximo 20 linhas.** Se o artigo tem mais pra dizer, o
  post pega um ponto só e manda o resto pro artigo
- Zero corporativês, nada de "ver mais" forçado com reticência
- Sem "arraste pro lado" — no LinkedIn o carrossel é PDF, não tem swipe
- **CTA: 1 linha, link do artigo.** O link vai no primeiro comentário, e o post diz
  isso — link no corpo derruba o alcance
- Fechar com 1 linha de quem é a empresa. Sem bloco de oferta
- Até 3 hashtags no final, do nicho profissional. Sem emoji, exceto marcador
  numérico em lista

**Teste antes de salvar:** ler só as duas primeiras linhas. Se elas não fazem abrir
o post, refazer o gancho. E o teste de sempre: se cabe no LinkedIn de qualquer
outra empresa do setor, não serve.

### Passo 6 — Revisão (obrigatório)

**Nunca entregar sem passar pelo `/revisar`.** Rodar em subagente (`Agent`,
`general-purpose`), passando a pasta da peça e o caminho do `criterios.md` — quem
escreveu não enxerga o próprio vício.

Conferir junto o campo "Atenção" da pauta de origem, se houver.

- **APROVADO** / **APROVADO COM AJUSTES** → aplicar os ajustes e seguir
- **REPROVADO** → corrigir e **revisar de novo**. Não entregar peça reprovada
  dizendo "tem uns pontos a ajustar"

### Passo 7 — Entregar

```
✓ Artigo:    conteudo/fila/<pasta>/artigo.md (rascunho)
✓ Carrossel: o que o /carrossel gerou + instagram/*.png
✓ Legendas:  legenda.md · legenda-linkedin.md
✓ Revisão:   revisao.md — veredito <X> · placar <conferido | não conferido>

Preciso de você: <foto, dado, resposta do dono, aprovação que falta>

Pra publicar: /aprovar-post
```

Atualizar o status no `conteudo/calendario.md` (`pauta` → `escrito`) e preencher a
coluna Arquivo.

---

## Quando NÃO usar

| Pedido | Skill certa |
|---|---|
| Carrossel avulso, sem artigo | `/carrossel` |
| Reel ou vídeo | `/angulos` (entrega o roteiro com marcação de tempo) |
| Só explorar como abordar um tema | `/angulos` sozinho |
| Peça de texto curta e avulsa | `/post` |
| Atualizar artigo existente | editar direto |

## Princípios

1. **Pauta pesquisada primeiro.** O tema vem do calendário, do `/radar` ou do
   `/ideias`. Post sem pesquisa por trás não passa no `/revisar` (bloqueio 9)
2. **Ângulo é escolha, não sorte.** O primeiro ângulo que vem à cabeça costuma ser o
   mais óbvio, e o óbvio já foi publicado por todo mundo
3. **O artigo é a peça-mãe.** Carrossel e legendas derivam dele, não o contrário
4. **Tudo conectado.** Carrossel aponta pro artigo, artigo tem CTA pro contato
5. **Rascunho sempre.** Nada vai ao ar daqui — quem publica é o `/aprovar-post`
6. **Nada publica sem revisão.** O `/revisar` é passo obrigatório, não cortesia
7. **Linguagem do público real.** Sempre
