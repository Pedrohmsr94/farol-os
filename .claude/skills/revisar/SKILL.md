---
name: revisar
description: >
  Controle de qualidade de peça de conteúdo antes de publicar — carrossel, legenda,
  artigo, roteiro de vídeo, post de LinkedIn, anúncio, e-mail que vai pra fora.
  Julga contra critério escrito (voz da marca, restrições do cliente, risco do
  setor, fato conferido, cara de IA, filtro da arquitetura editorial) e contra o
  placar real da conta (formato e abertura que entregam), e devolve veredito:
  aprovado, aprovado com ajustes ou reprovado, com o trecho problemático citado.
  Roda em subagente pra ter olhos frescos. Use quando o usuário disser "revisa
  esse post", "isso pode publicar?", "passa no controle de qualidade",
  "/revisar", antes de qualquer /aprovar-post, ou como último passo do
  /publicar-tema.
---

# /revisar — Controle de qualidade antes de publicar

Julga, não escreve. Lê a peça pronta e diz se pode ir ao ar.

Existe porque peça ruim não é vergonha pequena: número errado, promessa de resultado
ou clichê de IA derrubam num post o que meses de conteúdo construíram — e em setor
regulado ainda viram risco de processo no conselho. O critério-mor: **se dá pra
perceber que uma máquina escreveu, não presta** — e quem escreveu não enxerga isso
na própria peça.

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
   Se for pasta, revisar **tudo** — `texto.md`, `artigo.md`, `legenda.md`,
   `legenda-linkedin.md`, `roteiro-reel.md` e os PNGs se existirem
2. Ler `criterios.md`
3. Ler `marca/guia-de-marca.md` — **a régua viva**. `criterios.md` deriva dele; se
   divergirem, o guia manda e o `criterios.md` está velho (avisar)
4. Ler `conteudo/arquitetura-editorial.md` — de onde vem o filtro de aprovação
   copiado no `criterios.md`. Se a arquitetura mudou depois da cópia, avisar
5. **Se a peça nasceu de pauta do `/radar`**, abrir o briefing de origem. O campo
   **"Atenção"** da ficha é obrigação, não sugestão: se dizia "não confirmado na
   fonte primária" e a peça publica assim mesmo, é **reprovação**
6. **Se a peça é de opinião ou análise** (leitura de mercado, "o que eu acho",
   case com número), conferir de onde veio a leitura: fala do dono registrada
   (`pesquisa/investigacoes/voz.md`, transcrição em `_memoria/fontes/`, resposta
   dele na conversa) ou texto que o Claude escreveu sozinho. O segundo caso é
   bloqueio 9
7. Ler o placar da conta, `pesquisa/investigacoes/desempenho/perfil-de-desempenho.md`
   (Passo 3b). Se não existe ou tem mais de 30 dias, rodar antes:
   `python scripts/perfil-de-desempenho.py --posts 40`. Se não der (sem token da
   Meta no `.env`, sem rede, conta sem histórico), seguir e escrever **"placar não
   conferido"** no veredito, com o motivo

### Passo 2 — Bloqueios

Os bloqueios de `criterios.md`. Qualquer um → **REPROVADO**. Sem negociação, sem
"mas o resto está bom". Um bloqueio é um bloqueio.

Pra cada, citar o **trecho exato** e dizer por que bate.

### Passo 3 — Ajustes

Não impedem publicação sozinhos, mas acumulam: **5 ou mais = reprovado por
acúmulo**. Peça com cinco problemas médios não é peça boa com detalhes, é peça mal
escrita.

Passar a peça também pelo **filtro da arquitetura editorial** (seção própria do
`criterios.md`). O que o filtro pega entra como bloqueio ou ajuste, conforme está
escrito lá.

### Passo 3b — O placar

Critério e desempenho são réguas diferentes. Os passos 2 e 3 dizem se a peça
**pode** ir ao ar; este diz se ela **vai ser vista**. A fonte é o perfil de
desempenho: dado real da própria conta — alcance, salvamento e compartilhamento
por post, separados por formato, com os 25% melhores e os 25% piores lidos de
perto. Sem estimativa, sem benchmark de fora: o número de outra conta não diz nada
sobre esta.

Comparar a peça com o perfil em três pontos:

1. **Formato.** O perfil diz a mediana de alcance de cada formato nessa conta.
   Peça em formato que entrega abaixo da mediana ganha o **ajuste de placar**
   (ajuste 13), com o número junto: *"carrossel: mediana 300 contas; reel: 746.
   Essa peça é carrossel técnico."* Exceção: carrossel que precisa ser visto lado
   a lado (comparação em duas colunas, sequência de passos, história com imagem)
   — dizer qual dos três casos é
2. **Abertura.** Como abrem os 25% melhores e como abrem os 25% piores. Peça que
   abre como os piores ganha aviso — não é ajuste, é informação pro autor
3. **Salvamento e compartilhamento.** É o placar de autoridade. Se a peça é técnica
   e o perfil mostra que técnico não é guardado nessa conta, dizer isso com o número

O placar **não reprova sozinho**. Entra como ajuste e como texto no veredito, e o
operador decide. Mas nunca fica em silêncio: peça no formato errado sai com o
número na frente, não com "aprovado" seco.

### Passo 4 — Veredito

| Veredito | Quando | O que acontece |
|---|---|---|
| **APROVADO** | zero bloqueios, até 1 ajuste | libera pro `/aprovar-post` |
| **APROVADO COM AJUSTES** | zero bloqueios, 2-4 ajustes | corrigir e publicar. Não revisa de novo |
| **REPROVADO** | qualquer bloqueio, ou 5+ ajustes | volta pro autor. Depois de corrigir, **revisar de novo** |

### Passo 5 — Entregar

Salvar `revisao.md` na pasta da peça (ou ao lado do arquivo revisado) e resumir no
chat:

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

## Placar
Perfil de <data>, <N> posts. Formato da peça: carrossel (mediana da conta: 300
contas; reel: 746). Abertura técnica; os 25% melhores abrem com história.
[ou: "placar não conferido — motivo"]

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
  aqui. Aqui é se a peça, do jeito que está, pode ir ao ar. As exceções são o
  placar, que é dado, e o filtro da arquitetura, que é decisão escrita — nenhum
  dos dois é opinião do revisor
- Dúvida entre aprovar com ajustes e reprovar: **reprovar**. Custa uma rodada; o
  contrário custa a percepção de competência do cliente
