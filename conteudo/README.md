# Conteúdo

O caminho de um post: **calendário → fila → publicados**.

| Onde | O que é |
|---|---|
| `arquitetura-editorial.md` | o que a marca defende: Big Idea, tensões, linhas com fatia, balanço de funil, filtro de aprovação. Feito pelo `/arquitetura-editorial`, lido antes de qualquer pauta |
| `calendario.md` | a pauta do mês. Tema, linha, funil, tensão, formato, data, status, origem |
| `fila/` | escrito, esperando aprovação do cliente |
| `publicados/` | foi ao ar. Com data de publicação e resultado |

**Nome:** `AAAA-MM-DD-tema-curto` — a mesma data que está no calendário. O nome
não muda quando a peça muda de pasta, só a pasta muda.

Peça de texto simples é **um arquivo** (`.md`). Peça com visual é **uma pasta**
com o mesmo nome, contendo o texto, o que o `/carrossel` gerar, os PNGs em
`instagram/`, as legendas e a `revisao.md`.

Quando o cliente aprova, o arquivo sai de `fila/` e vai pra `publicados/`.
Quando o resultado chega (uma semana depois, no `/semana`), o número entra no
rodapé do próprio arquivo.

É esse rodapé que faz o `/calendario` do mês seguinte saber o que rendeu.
