---
name: carrossel
description: >
  Cria carrosséis e posts únicos de Instagram, LinkedIn e Facebook na identidade da
  empresa com o modelo "editorial" (v2): uma ficha YAML vira HTML e PNG 1080x1350 via
  scripts/carrossel/gerar.py, com mais de vinte layouts nomeados (capa, número, prova,
  cartões, comparativo, proposta, páginas, fecho…). Lê a pauta, escreve o texto na voz
  da marca, mostra pra aprovação, monta a ficha, renderiza e gera a legenda com a lista
  "Antes de publicar". Use quando o usuário pedir "carrossel", "post pro instagram",
  "vira carrossel", "monta a peça", "conteúdo visual", "criar imagem", "/carrossel".
---

# /carrossel — Carrossel no modelo editorial (v2)

Pega uma pauta → entrega a ficha YAML, o HTML, os PNGs 1080×1350, a folha de
contato e a legenda, tudo na pasta da peça. O desenho é código; o que se edita é a
ficha.

## Dependências (ler antes)

- **Voz:** `marca/guia-de-marca.md`. Em branco = avisar e oferecer `/marca` antes
- **Visual:** `identidade/marca-visual.yaml` (os valores que o gerador usa),
  `identidade/design-guide.md` (o porquê, as proibições) e **`identidade/carrossel.md`**
  (os layouts, os esqueletos, as regras de texto)
- **Estratégia:** `conteudo/arquitetura-editorial.md` (linha, tensão, funil, o que a
  marca nunca faz) e, se a pauta veio de lá, a ficha em `pesquisa/radar/`,
  `pesquisa/ideias/` ou `pesquisa/angulos/`
- **Placar:** `pesquisa/investigacoes/desempenho/perfil-de-desempenho.md` (o que
  entrega na própria conta) e `pesquisa/referencias/padroes.md` (o que entrega no
  nicho), quando existirem
- **Ferramentas:** `scripts/carrossel/gerar.py` + `modelo.css`,
  `scripts/render-carrossel.js`, `node_modules` na raiz (`npm run setup`), Python com
  `pyyaml` (`npm run setup:python`)
- **Saída:** `conteudo/fila/<AAAA-MM-DD>-<slug>/`

Se `identidade/marca-visual.yaml` ainda estiver com os valores neutros (`nome: "Sua
Empresa"`), avisar: a peça sai no visual de teste do Farol OS e não serve pra
publicar. Oferecer preencher a identidade primeiro, a partir do brandbook.

## Regras que não se negociam

1. **Máximo 60 palavras por slide** (o gerador avisa), uma frase em negrito por slide,
   seta ou pergunta no fim dos internos
2. **Fonte em cartão** pra todo dado, com data. Dado sem fonte não entra: vira
   "(validar antes de publicar)" na ficha e na legenda
3. **Fecho com gente da empresa** e CTA que continua a narrativa. Nunca "fale com um
   especialista", nunca foto de banco de imagem
4. **Foto real** da empresa ou do acervo. Imagem gerada por IA só pra fundo, objeto,
   cena sem pessoa, ou retrato tratado de figura pública a partir da foto oficial.
   **Nunca rosto inventado de gente da empresa**
5. **Nada das palavras proibidas** do guia de marca. Nada de medo, urgência falsa,
   contagem regressiva
6. **Preço, caso de cliente e depoimento** só com autorização escrita
7. Sequência de capas no feed: alternar foto → texto/comparativo → foto. Se não souber
   qual foi a última, perguntar

## Workflow

### 1. A pauta

- Pauta com ficha (radar, ideias, ângulos): usar tese, gancho, prova e "evitar" como
  briefing. Se a ficha marca pesquisa pendente, dizer antes de escrever
- Pauta solta: passar pelo filtro da arquitetura editorial — qual tensão organiza?
  que decisão do leitor melhora? o CTA continua a narrativa?
- Escolher a **família** e o esqueleto em `identidade/carrossel.md` (notícia que vira
  decisão · case · comparativo · framework · documento público)
- Conferir no placar se carrossel é o formato certo pra essa pauta. Se reel entrega o
  dobro na conta e a pauta não precisa ser vista lado a lado, dizer

### 2. O texto (checkpoint)

Escrever slide a slide, já no formato da ficha (layout + campos). Mostrar ao usuário
**antes de renderizar**: duas opções de título de capa, o corpo de cada slide, o
fecho. Esperar o ok. Nenhuma imagem é gerada antes desse ok.

### 3. As imagens

- **Fotos reais:** pedir ao usuário as que faltam e dizer quais (capa, fecho, seção).
  Salvar em `fotos/` dentro da pasta da peça
- **Documento público** (plano, lei, norma): recortar as páginas do PDF com a
  proposta grifada, sem cabeçalho e rodapé de campanha ou de partido
- **Print de matéria:** um por dado, com veículo e data
- **IA (conector Higgsfield, quando conectado no claude.ai):** mostrar o custo em
  créditos antes de gerar e esperar o ok. Retrato de figura pública pode ser barrado
  pelo filtro; a versão monocromática costuma passar
- **Figura sem fundo** atravessando dois slides: `recorte` em dois slides seguidos

### 4. A ficha e o render

```powershell
py scripts\carrossel\gerar.py conteudo\fila\<AAAA-MM-DD>-<slug>\ficha.yaml --render
```

Conferir os avisos (palavras por slide, foto não encontrada, logo ausente,
contraste). Mostrar a `_previa.png`. Ajustar a **ficha**, nunca o HTML, e renderizar
de novo.

### 5. A legenda

Em `legenda.md` na mesma pasta, no padrão do `marca/guia-de-marca.md`. Estrutura que
funciona quando o guia não define outra: frase forte de abertura → parágrafos curtos,
um passo por parágrafo → a virada quando há fato → o que importa pro leitor agora →
a frase da tese → pergunta ao leitor. O mesmo texto serve Instagram e Facebook;
LinkedIn ganha versão própria pelo `/angulos`.

Abaixo de uma linha `---`, a lista **"Antes de publicar"** (não vai pro ar):

- [ ] Fonte de cada slide, com veículo, data e a frase exata do documento
- [ ] Quais imagens são geradas por IA e de que foto partiram
- [ ] **Tema de eleição:** perfil de empresa não impulsiona (Lei 9.504, art. 57-C).
      Descrever a proposta, sem adjetivo, sem pedido de voto, mesmo tratamento pra
      todos os candidatos
- [ ] Resposta padrão pros comentários, quando o tema for sensível
- [ ] `/revisar`

### 6. Antes de publicar

`/revisar` obrigatório. Peça que inaugura uma série nova: registrar o nome da série
e o esqueleto usado em `identidade/carrossel.md`.

## Estrutura de saída

```
conteudo/fila/<AAAA-MM-DD>-<slug>/
  ficha.yaml        ← a peça (é isto que se edita)
  fotos/            ← fotos reais, prints, recortes
  carrossel.html    ← gerado
  modelo.css, logo, fotos   ← copiados pelo gerador
  instagram/slide-01.png … slide-NN.png
  _previa.png       ← folha de contato
  legenda.md
```

## Post único

Ficha com um slide só (`capa` com `estilo: noticia`, `numero` ou `prova`). O gerador
tira o contador sozinho.

## Exemplo

`conteudo/exemplos/carrossel-exemplo/ficha.yaml` — empresa fictícia, seis slides,
família "notícia que vira decisão". Serve pra testar a instalação: se esse render sai,
o sistema está pronto.
