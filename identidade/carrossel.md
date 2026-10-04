# O modelo de carrossel · "editorial" (v2)

> O desenho é código: `scripts/carrossel/modelo.css` (o desenho),
> `scripts/carrossel/gerar.py` (a ficha YAML vira HTML) e
> `scripts/render-carrossel.js` (o HTML vira PNG 1080×1350). A marca entra por
> `identidade/marca-visual.yaml`. O que se edita é a ficha, nunca o HTML.
>
> Provado em produção desde setembro/2026: peças de notícia, case, comparativo,
> homenagem e eleição. Exemplo pronto em `conteudo/exemplos/carrossel-exemplo/`.

## Em uma frase

Coluna de revista em seis a dez slides: uma tese, um fato ou caso como porta, a
decisão do leitor como destino, e a empresa só no fim, com gente real.

## As decisões de desenho

| # | Decisão | Por quê |
|---|---|---|
| 1 | Capa com **foto real sangrando** e título em duas camadas (leve + **negrito**) | Rosto na capa é o formato que mais entrega na maioria das contas. O premium vem do peso da letra |
| 2 | **Selo numerado** na cor de destaque por seção | Organiza a leitura sem precisar de olho em caixa alta |
| 3 | **Cartão de prova** (fonte, data, manchete ou dado) | Todo número tem origem rastreável, no próprio slide |
| 4 | Alternância **escuro/claro** nos internos | O gerador aplica sozinho; o feed não vira bloco de uma cor só |
| 5 | **Fecho com gente da empresa** + CTA que continua a narrativa | Nunca "fale com um especialista", nunca foto de banco |
| 6 | Motivos decorativos (halftone, curva) **só se a marca tiver** | Liga e desliga em `marca-visual.yaml` |

## As regras de texto

- **Máximo 60 palavras por slide.** O gerador avisa
- **Uma frase em negrito por slide** — a que carrega a tensão
- **Seta ou pergunta no fim de cada slide interno**
- **Fonte em cartão** pra todo dado, com data. Sem fonte, o dado não entra: vira
  "(validar antes de publicar)" na ficha e na legenda
- **Sem olho em caixa alta** espalhado pela peça. Dá cara de IA
- **Foto real ou do acervo da empresa.** Rosto gerado por IA de gente da empresa, nunca

## O vocabulário de layouts

| layout | Pra quê | Campos principais |
|---|---|---|
| `capa` | foto + título + sub | `foto`, `titulo`, `sub`, `seta`, `selo`; `degrade: leve` só fecha o escuro embaixo do título; `alinha: centro`; `estilo: noticia` pro card único de notícia |
| `capa-dupla` | comparativo: duas fotos lado a lado | `a{foto,k,t}`, `b{...}`, `vs`, `titulo` |
| `capa-reacao` | reação a fala pública: quadro do vídeo, a frase em destaque, a pergunta da casa | `foto`, `selo`, `legenda`, `titulo`, `pergunta`, `seta` |
| `texto` | uma ideia, dois ou três parágrafos | `titulo`, `corpo[]` (item pode ser `{texto, destaque, seta}`) |
| `numero` | número gigante com rótulo e fonte | `numero` (aceita `<small>%</small>`), `rotulo`, `corpo[]`, `fonte` |
| `metade` | metade foto, metade número; sem `numero`, foto + título + corpo | `foto`, `numero`, `rotulo`, `corpo[]`, `fonte`, `alto`, `pos` |
| `cartoes` | lista numerada ou de checks | `titulo`, `itens[{t,d}]`, `check: true`, `corpo[]` |
| `prova` | manchete, citação ou dado com fonte | `titulo`, `antes[]`, `cartao{k,t,fonte}`, `corpo[]` |
| `secao` | selo numerado + título + corpo + foto opcional | `n`, `titulo`, `corpo[]`, `foto` |
| `comparativo` | A em cima (claro), B embaixo (escuro) | `a{k,t,foto?}`, `b{k,t,foto?}` |
| `dois-lados` | a mesma situação vista de dois jeitos, linha a linha | `titulo`, `cab{a,b,ico_a,ico_b}`, `linhas[{k,a,b}]`, `corpo[]` |
| `diagrama` | círculos conectados: a decisão no centro | `titulo`, `centro`, `satelites[{t,d}]` (4 a 6), `corpo[]`, `alto`, `raio`, `girar` |
| `ciclo` · `ano` | roda: etapas de um processo · os doze meses com os marcados | `titulo`, `nos[]` ou `marcados[{m,t}]`, `centro`, `corpo[]` |
| `notas` | duas contas ou notas lado a lado | `titulo`, `a{k, linhas[{t,v,destaque?,apagado?}], veredito}`, `b{...}`, `corpo[]` |
| `extrato` | a conta como extrato, linha a linha | `titulo`, `cab{a,b}`, `linhas[{t,v,destaque,apagado,small}]`, `veredito`, `fonte` |
| `frame` | quadro de vídeo como player, a frase e o comentário da casa | `foto`, `tempo`, `fonte`, `progresso`, `frase`, `comentario` |
| `print` | print de manchete em cartão, um ou dois | `titulo`, `itens[{foto, fonte}]`, `comentario`, `corpo[]` |
| `cena` | imagem sangrando com texto no topo e na base e marcação de caneta | `foto`, `pos`, `topo{t,corpo}`, `base{t,corpo}`, `marcas[]` |
| `mosaico` | 3 a 5 fotos em grade — a equipe | `fotos[]`, `alto`, `rotulo`, `corpo[]` |
| `proposta` | proposta com print da matéria e o "Na prática" | `n`, `titulo`, `corpo[]`, `print`, `pratica`, `bg{foto,pos,tam}` |
| `paginas` | páginas reais de um documento em leque, com a proposta grifada | `titulo`, `paginas[{foto,n,k}]`, `corpo[]` |
| `fecho` | pessoa real + CTA + método da empresa | `foto`, `titulo`, `corpo[]`, `nome`, `cargo`, `cta`, `metodo`; `largo: true` pra foto de grupo |

**Em qualquer layout:** `recorte: {foto, x, y, h, lado}` põe uma figura sem fundo
(PNG) por cima. O mesmo recorte em dois slides seguidos (`x` no primeiro,
`x − 1080` no segundo) faz a figura **atravessar a divisa** entre eles.

**Marcação leve no texto:** `**negrito**` vira o peso forte; `[palavra]` vira a
cor de destaque.

**Ficha limpa (`limpo: true`):** some série, edição e contador da cabeça (fica só
o logo) e o `@` do pé. Pra peça institucional ou homenagem, onde a mobília
editorial atrapalha.

## Os esqueletos que já provaram

- **Notícia que vira decisão:** `capa` → `texto` (o fato) → `numero` ou `prova` →
  `texto` (a virada) → `cartoes` (3 ou 4 decisões) → `texto` (o que você
  controla) → `fecho`
- **Case:** `capa` → `numero` ou `prova` (o dado que surpreende) → `diagrama` ou
  `secao 1` → `secao 2` → `secao 3` → `cartoes` (traduzindo pro leitor) → `fecho`
- **Comparativo:** `capa-dupla` → 4 a 6 × `comparativo` ou `dois-lados` → `texto`
  (a pergunta que o leitor faz a si) → `fecho`
- **Framework:** `capa` com rosto → n × `secao` com foto real → `fecho`
- **Documento público** (plano, lei, norma): `capa` → `paginas` (as páginas reais,
  grifadas) → n × `proposta` (com print e "Na prática") → `texto` (o que já tem
  data) → `fecho`

## Como rodar

```powershell
py scripts\carrossel\gerar.py conteudo\fila\<AAAA-MM-DD>-<slug>\ficha.yaml --render
```

Gera `carrossel.html` (com `modelo.css`, logo e fotos copiados pra pasta), os PNGs
em `instagram/` e a folha de contato `_previa.png`. Fotos: `fotos:` aponta a
pasta; os nomes nos slides são relativos a ela.
