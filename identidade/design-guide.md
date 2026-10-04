# Design guide

> **Como preencher.** Este arquivo é o porquê do visual. Os valores que o
> gerador usa ficam em `identidade/marca-visual.yaml`; aqui fica o que cada cor
> significa, o que é proibido e de onde veio. Fonte preferida: o brandbook da
> empresa (PDF em `_memoria/fontes/`). Sem brandbook, o `/marca` levanta o mínimo
> com o dono — e isso fica marcado como provisório até um designer validar.
>
> Toda skill que gera visual lê este arquivo antes. Campo vazio = o Claude
> pergunta, não inventa.

**Status:** [provisório · validado por ___ em ___]
**Origem:** [brandbook de AAAA · levantado no /marca em DD/MM/AAAA]

## Cores

| Papel | Nome | Hex | Uso |
|---|---|---|---|
| Campo escuro | | | capa, fecho, slides escuros |
| Campo claro | | | slides claros |
| Destaque | | | filete, selo, número grande, botão. **Uma só** |
| Texto | | | corpo sobre o claro |

### Regra de contraste

Testar cada combinação de texto e fundo (mínimo 4,5:1 pra texto corrido, 3:1 pra
título grande). Anotar aqui o que **não** pode virar texto — normalmente a cor de
destaque sobre o campo claro. O gerador escurece o destaque sozinho quando ele
vira letra sobre o claro e avisa quando uma combinação fica abaixo do mínimo.

| Combinação | Razão | Pode ser texto? |
|---|---|---|
| | | |

## Tipografia

- **Título:** [família · pesos]
- **Corpo:** [família · pesos]
- Só fonte do Google Fonts ou instalada na máquina. Fonte que não carrega faz o
  render sair com a fonte do sistema — o `render-carrossel.js` confere

## Logo

- Versão positiva: `identidade/logo.png` (PNG, fundo transparente, recortado rente)
- Versão negativa: `identidade/logo-negativo.png` (se existir)
- Área de respiro e tamanho mínimo: [do brandbook]

## Fotos

- De onde vêm as fotos reais: [acervo, sessão de fotos, celular da equipe]
- Quem aparece e quem não quer aparecer
- Imagem gerada por IA: só fundo, objeto ou cena **sem pessoa da empresa**. Retrato
  de figura pública só a partir de foto oficial, com registro na legenda interna

## Proibido

- [cor, filtro, fonte, estilo de foto, elemento que a marca não usa]
- Gradiente colorido sem estar no brandbook
- Emoji como elemento de layout

## Motivos

[Os elementos gráficos próprios da marca — linha, padrão, forma — e se o
gerador liga `halftone` e `curva` em `marca-visual.yaml`]
