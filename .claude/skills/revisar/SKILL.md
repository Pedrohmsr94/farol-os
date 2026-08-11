---
name: revisar
description: >
  Controle de qualidade de peça de conteúdo antes de publicar — carrossel, legenda,
  artigo, roteiro de vídeo, post de LinkedIn, anúncio. Julga contra critério escrito
  (voz da marca, restrições do cliente, risco do setor, fato conferido) e devolve
  veredito: aprovado, aprovado com ajustes ou reprovado, com o trecho problemático
  citado. Use quando o usuário disser "revisa esse post", "isso pode publicar?",
  "passa no controle de qualidade", "/revisar", antes de qualquer /aprovar-post, ou
  como último passo do /publicar-tema.
---

# /revisar — Controle de qualidade antes de publicar

Julga, não escreve. Lê a peça pronta e diz se pode ir ao ar.

Existe porque peça ruim não é vergonha pequena: número errado, promessa de resultado
ou clichê de IA derrubam num post o que meses de conteúdo construíram — e em setor
regulado ainda viram risco de processo no conselho.

**Critérios:** `criterios.md` (nesta pasta). É lá que se mexe quando a régua muda.

## Regra de ouro: olhos frescos

Quem escreveu não enxerga o próprio vício. Quando o `/revisar` for chamado **dentro
do `/publicar-tema`**, ou logo depois de você mesmo ter escrito a peça na mesma
conversa, rodar a revisão em um **subagente** (`Agent`, tipo `general-purpose`),
passando o caminho da peça e o de `criterios.md` — e não revisar de cabeça.

O subagente lê a peça sem saber as justificativas de quem escreveu. É o ponto inteiro.

Revisão avulsa, sobre peça de outra sessão, pode ser direto.

## Workflow

### Passo 1 — Reunir

1. Identificar a peça: pasta em `conteudo/fila/`, arquivo solto, ou texto colado.
   Se for pasta, revisar **tudo** — `texto.md`, `legenda.md`, `legenda-linkedin.md`,
   o artigo e os PNGs se existirem
2. Ler `criterios.md`
3. Ler `marca/guia-de-marca.md` — **a régua viva**. `criterios.md` deriva dele; se
   divergirem, o guia manda e o `criterios.md` está velho (avisar)
4. **Se a peça nasceu de pauta do `/radar`**, abrir o briefing de origem. O campo
   **"Atenção"** da ficha é obrigação, não sugestão: se dizia "não confirmado na
   fonte primária" e a peça publica assim mesmo, é **reprovação**

### Passo 2 — Bloqueios

Os bloqueios de `criterios.md`. Qualquer um → **REPROVADO**. Sem negociação, sem
"mas o resto está bom". Um bloqueio é um bloqueio.

Pra cada, citar o **trecho exato** e dizer por que bate.

### Passo 3 — Ajustes

Não impedem publicação sozinhos, mas acumulam: **5 ou mais = reprovado por
acúmulo**. Peça com cinco problemas médios não é peça boa com detalhes, é peça mal
escrita.

### Passo 4 — Veredito

| Veredito | Quando | O que acontece |
|---|---|---|
| **APROVADO** | zero bloqueios, até 1 ajuste | libera pro `/aprovar-post` |
| **APROVADO COM AJUSTES** | zero bloqueios, 2-4 ajustes | corrigir e publicar. Não revisa de novo |
| **REPROVADO** | qualquer bloqueio, ou 5+ ajustes | volta pro autor. Depois de corrigir, **revisar de novo** |

### Passo 5 — Entregar

Salvar `revisao.md` na pasta da peça e resumir no chat:

```markdown
# Revisão — <peça>
**Veredito: REPROVADO** · 2 bloqueios, 1 ajuste · <data>

## Bloqueios

### 1. Promessa de resultado (bloqueio 2)
> "a gente resolve o seu problema e você não paga nada a mais"

Promete resultado que depende de terceiro. Trocar por: o que a empresa faz, não
o que o cliente vai obter.

### 2. [...]

## Ajustes

### 1. Abstrato onde cabia concreto (ajuste 1)
> "os desafios do setor"
Trocar pelo desafio específico da pauta.

## O que está bom
[1-3 linhas. Não é gentileza — serve pro autor saber o que preservar na reescrita.]
```

## Regras

- **Não reescrever a peça.** Apontar o trecho e indicar a direção. Quem reescreve é
  quem escreveu — senão o revisor vira autor e some o olho externo
- **Citar sempre o trecho literal.** "O tom está ruim" não é revisão, é opinião
- **Não inventar bloqueio pra parecer rigoroso.** Peça boa é aprovada e pronto. Um
  revisor que nunca aprova é tão inútil quanto um que nunca reprova — e treina o
  autor a ignorar o veredito
- **Não julgar estratégia.** Se o tema vale a pena, se o momento é certo — não é
  aqui. Aqui é se a peça, do jeito que está, pode ir ao ar
- Dúvida entre aprovar com ajustes e reprovar: **reprovar**. Custa uma rodada; o
  contrário custa a percepção de competência do cliente
