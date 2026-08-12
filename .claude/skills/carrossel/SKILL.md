---
name: carrossel
description: >
  Cria carrosséis e posts visuais pra Instagram, LinkedIn e TikTok com a identidade
  da marca do cliente. Gera um HTML estilizado e renderiza em PNG 1080x1350 via
  Playwright, com legenda pronta no final. Suporta carrossel de texto, carrossel com
  foto e post único. Use quando o usuário pedir "carrossel", "post pro instagram",
  "criar imagem", "post educativo", "/carrossel".
---

# /carrossel — Carrossel e posts visuais

Pega um tema → entrega HTML estilizado + PNGs prontos pra postar + legenda.

## Dependências

- **Marca:** `marca/guia-de-marca.md` — **ler antes de criar qualquer visual**
- **Contexto e voz:** `_memoria/empresa.md`, `marca/guia-de-marca.md`
- **Playwright:** pra renderizar HTML em PNG
- **Saída:** `conteudo/fila/<AAAA-MM-DD>-<slug>/`

---

## Tipos

| Tipo | Quando | Estilo |
|---|---|---|
| **Carrossel de texto** | educativo, lista, explicação | tipografia limpa, fundos alternados, sem foto |
| **Carrossel com foto** | apresentação, capa com pessoa, bastidor | foto na capa com overlay + slides internos no padrão |
| **Post único** | frase de impacto, número, depoimento | varia conforme o conteúdo |

Se não estiver claro, perguntar qual dos três.

Foto: a real da empresa vem sempre na frente de foto gerada. Cliente de serviço
local com foto de banco de imagem é o cheiro mais rápido de "isso aí é terceirizado".

---

## Estilo visual base

Quando `marca/guia-de-marca.md` tiver cores e fonte, **ele manda**. Quando estiver
vago ou em branco, usar o padrão abaixo — editorial, calmo, sóbrio. Sem clip-art,
sem emoji decorativo, sem gradiente arco-íris, sem template genérico de IA.

Não parar pra pedir `/marca`: o carrossel funciona com defaults bons. Só avisar.

### Tipografia

- **Fonte:** Inter (Google Fonts), pesos 400/500/600/700/800/900
- **Título de capa:** 90-100px, weight 900, line-height 0.98, letter-spacing **-0.04em**
- **H2 (slides internos):** 60-72px, weight 800, line-height 1.04, letter-spacing **-0.035em**
- **Corpo:** 20-24px, weight 500, line-height 1.5
- **Eyebrow/kicker:** 13-16px, weight 700-800, **CAIXA ALTA**, letter-spacing **0.22-0.32em**
- **Contador de página:** 14-16px, weight 500-600, letter-spacing 0.18em, cor suave

**A regra do tipo:** título grande com kerning **apertado** (-0.035em), eyebrow
pequeno com kerning **aberto** (0.22em+). Esse contraste é o coração do estilo.

### Cores

Fundo + off-white + **UMA** cor de destaque. Nunca quatro cores brigando.

- Fundo escuro: `#0E1116` ou `#1A1A1A`
- Fundo claro: `#F5ECD7` (cream) ou `#FAFAF7`
- Texto sobre escuro: `#FAFAF7`
- Texto sobre claro: `#1A1A1A` (título) e `#444` (corpo)
- Destaque: a cor da marca, uma só

### Elementos recorrentes

- **Régua fina** (3-4px de altura, 60-80px de largura, cor de destaque) entre kicker e título
- **Logo no topo à esquerda + contador no topo à direita** em todos os slides
- **Borda de 1px** `rgba(255,255,255,0.12)` separando rodapé do conteúdo, em slide escuro
- **Selo circular** (200x200, borda 3px translúcida, rotate -10deg) pra data ou dado
- **Pills** em caixa alta, padding generoso, kerning 0.2em, pra rotular a categoria
- Padding base: 70-100px nas laterais

### Layouts nomeados

Cada slide tem um nome. Variar entre eles pra criar ritmo:

- **CAPA** — eyebrow + título grande + subtítulo + @. Fundo: foto com overlay
  (`rgba(12,10,9,0.55)` → `rgba(12,10,9,0.85)`) ou sólido
- **SOLO** — split: foto à esquerda 50% + texto à direita 50%
- **DUO** — texto em cima + 2 fotos lado a lado embaixo
- **NÚMERO** — numeral gigante (200-320px, weight 800, cor de destaque) + título + apoio
- **CITAÇÃO** — aspas grandes em marca d'água + frase + atribuição
- **CTA FINAL** — fundo na cor de destaque, logo centralizado, headline curta, contato

**Ritmo:** alternar fundo escuro ↔ claro ↔ destaque. Nunca dois slides seguidos com
o mesmo fundo.

### Sequência de capa no feed

Antes de definir a capa, olhar a **última publicada** em `conteudo/publicados/`:

claro → foto/escuro → cor da marca → claro

Nunca duas capas iguais em sequência. Se não souber qual foi a última, perguntar.

---

## Workflow

### Passo 1 — Planejar

1. Ler `marca/guia-de-marca.md` e `_memoria/empresa.md`
2. Identificar o tipo
3. Definir tema e ângulo. Se o tema veio do `/radar` e ainda não passou pelo
   `/angulos`, oferecer rodar — o primeiro ângulo que vem à cabeça é o mais óbvio

### Passo 2 — Texto

**Carrossel (5-10 slides):**
- Capa: máximo 8 palavras. **Oferecer 3 opções de título**
- Slides internos: uma ideia por slide, frase natural, sem bullet seco
- Slide final: CTA + logo

**Post único:** frase principal + contexto curto + CTA sutil.

**CHECKPOINT: mostrar o texto completo e esperar aprovação antes do visual.**
Renderizar PNG de texto não aprovado é retrabalho garantido.

### Passo 3 — Fotos (se for o tipo 2)

**Foto real da empresa primeiro.** Sempre. Pedir pro cliente mandar antes de
cogitar gerar.

Se não houver e o operador quiser gerar por IA:

```bash
node scripts/gerar-imagem.js "PROMPT EM INGLES" conteudo/fila/<pasta>/foto-capa.png
```

Precisa de `OPENAI_API_KEY` no `.env` da raiz (copiar de `.env.exemplo`). Custa
por imagem — avisar o operador antes de gerar em série.

Prompt em inglês, no padrão:

```
Professional [tipo] photography of [assunto], [detalhes], [ambiente],
[luz] lighting, shallow depth of field, shot from [ângulo],
editorial quality
```

Mostrar a imagem antes de usar. E **nunca gerar rosto identificável de pessoa** —
imagem de IA fingindo equipe, cliente ou resultado é o tipo de coisa que destrói
confiança quando alguém percebe. Serve pra fundo, textura e cena genérica.

### Passo 4 — HTML + PNG

1. Criar **um único `carrossel.html`** com todos os slides como `<div class="slide">`.
   CSS inline, Google Fonts como única dependência externa. Aplicar cores e
   tipografia da marca, no mínimo 2 layouts diferentes, logo + contador em todos os
   slides.

   Foto no slide:
   ```html
   <div class="slide" style="
     background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.7)), url('foto.png');
     background-size: cover; background-position: center;">
     <div class="content"><h2>Texto sobre a foto</h2></div>
   </div>
   ```

2. Renderizar com o script do projeto. **Não criar `render.js` dentro da pasta
   da peça** — o script é um só, e quando o layout mudar vale pras próximas:

   ```bash
   npm run carrossel -- conteudo/fila/<AAAA-MM-DD>-<slug>
   ```

   Formato vertical de story: `-- --formato 9:16`

   Se der erro de módulo não encontrado, o setup ainda não foi feito. Rodar uma
   vez no projeto:

   ```bash
   npm run setup
   ```

3. Mostrar slide 1, 2 e o CTA final renderizados. Aprovados, mostrar o resto.

### Passo 5 — Salvar

```
conteudo/fila/<AAAA-MM-DD>-<slug>/
  texto.md              ← texto aprovado
  carrossel.html
  instagram/            ← slide-01.png ... slide-NN.png
  legenda.md
  legenda-linkedin.md   ← se pedido
  foto-*.png            ← se houver
  revisao.md            ← do /revisar
```

Atualizar o status da linha em `conteudo/calendario.md` pra `escrito`.

### Passo 6 — Legenda (automática)

Ao terminar de renderizar, **gerar a legenda sem esperar pedido** e salvar em
`legenda.md`:

1. Hook na primeira linha
2. Contexto (1-2 frases)
3. CTA pro carrossel ("Arraste pro lado")
4. Bloco da empresa (o que ela faz, contato)
5. Hashtags (10-15 — público + nicho + cidade quando for negócio local)

Respeitar o guia de marca. Se ele diz "sem emoji", a legenda sai sem emoji, mesmo
que o formato "peça".

### Passo 7 — Revisar

Antes de entregar, rodar `/revisar`. Peça visual entra no mesmo controle de
qualidade que texto.

Depois: `/aprovar-post` publica.

---

## Regras

- Ler `marca/guia-de-marca.md` antes de qualquer visual. Sempre
- Carrossel: 1080x1350 (4:5). Reels/TikTok: 1080x1920 (9:16), só quando pedido
- Sempre checar a sequência de capa do feed antes de definir capa nova
- Sempre gerar `legenda.md` automaticamente no fim
- Um único `carrossel.html` com todos os slides, CSS inline. A renderização é
  pelo `npm run carrossel` — não duplicar script dentro da pasta da peça
- Não repetir layout entre slides
- Não renderizar PNG antes do texto aprovado
- **Não escrever número no slide sem a fonte no `texto.md`.** O slide não cabe a
  fonte, mas quem revisa precisa conferir
