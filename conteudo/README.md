# Conteúdo

O caminho de um post: **calendário → fila → publicados**.

| Onde | O que é |
|---|---|
| `calendario.md` | a pauta do mês. Tema, formato, data, status |
| `fila/` | escrito, esperando aprovação do cliente |
| `publicados/` | foi ao ar. Com data de publicação e resultado |

**Nome do arquivo:** `AAAA-MM-DD-tema-curto.md` — a mesma data que está no
calendário. O arquivo não muda de nome quando muda de pasta, só de pasta.

Quando o cliente aprova, o arquivo sai de `fila/` e vai pra `publicados/`.
Quando o resultado chega (uma semana depois, no `/semana`), o número entra no
rodapé do próprio arquivo.

É esse rodapé que faz o `/calendario` do mês seguinte saber o que rendeu.
