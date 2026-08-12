---
name: nova-skill
description: >
  Cria uma skill nova a partir de uma ideia do operador — entrevista sobre o que
  ela faz, escreve o SKILL.md com os gatilhos certos, roda uma vez num caso real
  e registra no sistema. Use quando o usuário disser "quero criar uma skill",
  "cria um comando que faça X", "dá pra automatizar isso?", "nova skill",
  "/nova-skill".
---

# /nova-skill — Transformar uma ideia em comando

O sistema vem com 24 skills. Elas cobrem o que é comum a qualquer operação de
marketing — mas cada operador tem o jeito dele, e cada cliente tem uma exigência
que ninguém previu.

Essa skill fecha esse buraco. O operador descreve o que quer, e sai um comando
funcionando.

**Não confundir com a vizinha:**

| Skill | Ponto de partida |
|---|---|
| `/mapear-rotinas` | "o que você repete toda semana?" — descoberta |
| `/nova-skill` | "quero um comando que faça X" — o operador já sabe |

Se ele não souber o que quer automatizar, o caminho é `/mapear-rotinas`.

---

## Passo 1 — Entender a ideia

Quatro perguntas. Uma por vez.

1. **"O que essa skill entrega no fim?"** Um arquivo? Um texto no chat? Uma peça
   pronta? Uma decisão? Sem saber a saída, não dá pra escrever o passo a passo
2. **"Me conta como você faria isso na mão, do começo ao fim."** É daqui que sai
   o workflow. Pedir o último caso real, não o processo idealizado
3. **"O que ela precisa saber antes de começar?"** Quais arquivos ler, o que
   perguntar, o que já existe no repositório
4. **"Como você chamaria isso? E o que você diria quando quisesse usar?"** O nome
   e as frases-gatilho

Se a resposta 2 vier vaga, pedir o exemplo concreto: *"a última vez que você fez
isso, o que você abriu primeiro?"*

## Passo 2 — Conferir se já existe

Antes de escrever, **ler as skills de `.claude/skills/`** e conferir três coisas:

- **Já existe?** Boa parte das ideias já está coberta por skill que o operador
  não sabia que existia. Dizer qual é e mostrar
- **É extensão de uma que existe?** Se a ideia é "o `/carrossel` mas em outro
  formato", o certo é **editar a skill atual**, não criar outra. Skill duplicada
  é pior que skill faltando: as duas divergem com o tempo e ninguém sabe qual vale
- **Conflita com alguma?** Duas skills com gatilho parecido fazem o Claude
  escolher errado. Se os gatilhos se cruzam, ajustar os dois

Só seguir pra escrita depois de responder essas três.

## Passo 3 — Decidir onde mora

> "Essa skill é específica desse cliente, ou você vai querer ela em todos?"

| Escopo | Onde | Quando |
|---|---|---|
| **Deste cliente** | `.claude/skills/<nome>/SKILL.md` | depende do setor, do contrato ou de uma exigência daquela empresa |
| **De todos** | `~/.claude/skills/<nome>/SKILL.md` | é jeito de trabalhar do operador, vale em qualquer cliente |

Na dúvida, começar local. Promover pra global depois de funcionar em dois
clientes é fácil; despromover é bagunça.

## Passo 4 — Escrever

Estrutura obrigatória:

```markdown
---
name: <nome-em-kebab-case>
description: >
  <O que faz, em 1-2 frases.> Use quando o usuário disser "<gatilho 1>",
  "<gatilho 2>", "<gatilho 3>", "/<nome>".
---

# /<nome> — <o que é, em 4 a 6 palavras>

<Uma ou duas frases: por que essa skill existe e o que ela protege.>

## Dependências

- <arquivo que ela lê>
- **Saída:** <caminho exato onde salva>

## Workflow

### Passo 1 — <nome do passo>
<o que fazer, concreto>

### Passo 2 — <...>

## Regras

- <o que nunca fazer>
- <o que fazer quando faltar informação>
```

**A `description` é a parte que mais importa.** É por ela que o Claude decide
quando usar a skill. Regras:

- Escrever os gatilhos **com as palavras que o operador realmente fala**, não com
  o nome técnico. Se ele diz "fecha o mês do cliente", esse é o gatilho — não
  "gerar relatório mensal consolidado"
- Três a cinco gatilhos, incluindo o `/<nome>`
- Descrição vaga = skill que nunca dispara sozinha

**O workflow é o processo dele, não um processo ideal.** Se ele faz em 4 passos,
a skill tem 4 passos. Melhorar o processo é outra conversa, e deve ser proposta
separada — não embutida sem ele perceber.

**A seção Regras não é decorativa.** É onde entram os limites: o que a skill não
pode inventar, o que ela precisa perguntar em vez de supor, o que exige aprovação
do operador antes de acontecer.

## Passo 5 — Calibrar ao cliente

Antes de fechar, ler e refletir no texto da skill:

- `_memoria/empresa.md` — o que a empresa vende e pra quem
- `marca/guia-de-marca.md` — se a skill escreve alguma coisa, ela obedece a voz
- `_memoria/operacao.md` — o que está dentro e fora do contrato

Skill que gera conteúdo **precisa** mandar ler o guia de marca e passar pelo
`/revisar`. Skill que toca número **precisa** proibir número inventado. Isso não
é opcional: são as regras que o sistema inteiro segue, e uma skill nova que as
ignora abre um buraco por onde o erro entra.

## Passo 6 — Rodar uma vez

**Skill que nunca rodou é palpite escrito em markdown.**

Rodar na frente do operador, no caso real que ele descreveu no passo 1. Ver onde
trava, onde falta contexto, onde ela pergunta o que já estava no arquivo.

Ajustar o `SKILL.md` com o que apareceu. Quase sempre aparece alguma coisa.

## Passo 7 — Registrar

1. Acrescentar a skill na tabela do `CLAUDE.md`, seção "Fluxo de trabalho"
2. Se ela produz arquivo em pasta nova, registrar em "Onde cada coisa mora"
3. Oferecer o `/salvar`

Fechar assim:

```
Criada: /<nome>  (<local | global>)
Testada em: <o caso real>
Entrega: <caminho da saída>
Registrada no CLAUDE.md

Pra usar, é só dizer "<um dos gatilhos>".
```

---

## Regras

- **Uma skill por vez.** Skill boa leva tempo. Cinco medianas valem menos que uma
  que funciona
- **Não criar skill pra tarefa que acontece uma vez.** Se não repete pelo menos
  duas vezes por mês, o custo de manter é maior que o de fazer na mão — e vale
  dizer isso ao operador em vez de aceitar calado
- **Skill não decide sozinha o que é irreversível.** Se o processo envolve
  publicar, enviar, pagar ou apagar, a skill prepara e mostra; quem dispara é o
  operador
- **Não copiar skill existente e trocar palavras.** Se duas skills têm o mesmo
  esqueleto, provavelmente eram pra ser uma com um parâmetro
- Nome em kebab-case minúsculo, sem acento. É o que vira o comando
