---
name: publicar-tema
description: >
  Orquestra a criação completa de uma peça a partir de um tema — escolhe o ângulo,
  escreve o artigo de blog, gera o carrossel resumo e produz as legendas pra
  Instagram, Facebook e LinkedIn, tudo amarrado e passando pela revisão. Use quando
  o usuário pedir "publicar tema", "gera o conteúdo do tema X", "transforma essa
  pauta em post", "cria o conteúdo completo", "/publicar-tema".
---

# /publicar-tema — Pipeline completo de uma peça

Skill orquestradora. Tema → artigo + carrossel + 3 legendas, tudo conectado e
revisado.

## Dependências

- **Pautas:** `pesquisa/radar/` — é daqui que o tema vem por padrão
- **Temas de SEO:** `pesquisa/seo/05-estrategia-conteudo.md`
- **Skills no fluxo:** `/angulos` (passo 1), `/carrossel` (passo 4), `/revisar` (passo 6, obrigatório)
- **Voz:** `marca/guia-de-marca.md`, `pesquisa/investigacoes/voz.md` se existir
- **Saída:** `conteudo/fila/<AAAA-MM-DD>-<slug>/`

---

## Workflow

### Passo 0 — O tema

Se o operador passou tema explícito, usar.

Se não, **abrir os briefings recentes em `pesquisa/radar/`** e listar as pautas
ainda não usadas, com o destaque de cada dia. Essa é a fonte principal: pauta que
nasceu de varredura, com fato, ângulo e formato já sugeridos. Só recorrer à
estratégia de SEO se não houver briefing servindo.

Checar `conteudo/publicados/` pra não duplicar.

**Se a pauta trouxer campo "Atenção"**, esse aviso viaja com o tema até o fim e é
verificado no passo 6.

### Passo 1 — Ângulo

**Não escolher o ângulo sozinho.** Rodar `/angulos`: ele devolve 5 ângulos de
famílias diferentes e, depois da escolha, mostra como aquele ângulo vira cada
formato.

Se o operador escolher reel ou vídeo, o `/angulos` entrega o roteiro e **essa skill
não é a certa** — ver "Quando NÃO usar".

Os ângulos não escolhidos ficam salvos e viram pauta futura no `/calendario`.

### Passo 2 — Pesquisa rápida

Antes de escrever:

- Palavra-chave principal e variações (`pesquisa/seo/01-pesquisa-demanda.md`)
- Como o mercado trata o assunto (`02-analise-concorrencia.md`) — pra fugir do óbvio
- Ângulo GEO se aplicável (`08-geo.md`) — a pergunta que as IAs respondem
- Se existir `pesquisa/investigacoes/comentarios/`, procurar a dúvida real sobre
  esse tema. Artigo que responde pergunta feita de verdade rende mais que artigo
  que responde pergunta imaginada

### Passo 3 — O artigo

**Destino:** `conteudo/fila/<AAAA-MM-DD>-<slug>/artigo.md`

Se o cliente tem site e você sabe o formato dele, escrever já no formato do site
(HTML estático, markdown com frontmatter, o que for) e dizer qual é. Se não tem
site, o artigo continua valendo — é a peça-mãe de onde o carrossel e as legendas
derivam, e vira post de LinkedIn ou material de WhatsApp.

**Estrutura (800-1500 palavras):**

1. **Lead (1-2 parágrafos)** — o problema concreto do público, sem enrolação
2. **H2 explicativo** — o quê e por quê
3. **H2 prático** — como fazer, o que olhar
4. **H2 comparativo ou técnico** (opcional)
5. **H2 onde a empresa se encaixa** — conexão natural, sem virar propaganda
6. **CTA final** — WhatsApp, formulário, contato

**Escrita:** frase curta, parágrafo de 2-4 linhas, concreto (número, data, valor),
sem jargão que o público não usa. Seguir `marca/guia-de-marca.md` estritamente.

### Passo 4 — Carrossel resumo

Sem perguntar, partir pro `/carrossel` (tipo 1, texto puro), na **mesma pasta**.

- **Capa:** o título do artigo, ou variação enxuta
- **Slides 2-6:** os pontos-chave (uma ideia por slide, frase natural)
- **Slide final:** CTA pro artigo

Capa seguindo a sequência alternada do feed — checar `conteudo/publicados/`.

### Passo 5 — Legendas

Na mesma pasta:

**`legenda.md`** (Instagram + Facebook):
- Hook na primeira linha
- 2-3 parágrafos de contexto
- CTA pro carrossel + CTA pro artigo
- Bloco da empresa (o que faz, contato)
- 10-15 hashtags (público + nicho + cidade se for negócio local)

**`legenda-linkedin.md`**:
- Hook profissional
- 3-5 parágrafos analíticos — LinkedIn aceita texto longo
- Sem "arraste pro lado"
- CTA: link direto pro artigo
- Sem bloco de oferta agressivo. Máximo 3 hashtags

### Passo 6 — Revisão (obrigatório)

**Nunca entregar sem passar pelo `/revisar`.** Rodar em subagente (`Agent`,
`general-purpose`), passando a pasta da peça — quem escreveu não enxerga o próprio
vício.

Conferir junto o campo "Atenção" da pauta de origem, se houver.

- **APROVADO** / **APROVADO COM AJUSTES** → aplicar os ajustes e seguir
- **REPROVADO** → corrigir e **revisar de novo**. Não entregar peça reprovada
  dizendo "tem uns pontos a ajustar"

### Passo 7 — Entregar

```
✓ Artigo:    conteudo/fila/<pasta>/artigo.md
✓ Carrossel: carrossel.html + render.js + instagram/*.png
✓ Legendas:  legenda.md · legenda-linkedin.md
✓ Revisão:   revisao.md — veredito <X>

Preciso de você: <foto, dado, aprovação que falta>

Pra publicar: /aprovar-post
```

Atualizar o status no `conteudo/calendario.md`.

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

1. **Pauta pesquisada primeiro.** O tema vem do `/radar`. Post sem pesquisa por trás
   não passa no `/revisar` (bloqueio 9)
2. **Ângulo é escolha, não sorte.** O primeiro ângulo que vem à cabeça costuma ser o
   mais óbvio, e o óbvio já foi publicado por todo mundo
3. **O artigo é a peça-mãe.** Carrossel e legendas derivam dele, não o contrário
4. **Tudo conectado.** Carrossel aponta pro artigo, artigo tem CTA pro contato
5. **Nada publica sem revisão.** O `/revisar` é passo obrigatório, não cortesia
6. **Linguagem do público real.** Sempre
