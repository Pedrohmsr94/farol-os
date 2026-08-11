---
name: mapear-rotinas
description: >
  Mapeia o que o operador repete toda semana e transforma em skill própria. Faz uma
  entrevista curta, propõe skills concretas e cria as aprovadas em `.claude/skills/`.
  Use quando o usuário pedir "/mapear-rotinas", "criar skill personalizada",
  "automatizar isso que eu faço sempre", "o que dá pra automatizar".
---

# /mapear-rotinas — Repetição vira skill

Skill de descoberta e criação. Transforma o que o operador repete em automação.

## Workflow

### Passo 1 — Entrevista

Três perguntas, uma por vez:

1. "Quais 3 coisas você repete toda semana e queria não ter que pensar mais?"
2. "Dessas, qual é a que mais consome tempo — e quanto tempo?"
3. "Como você faz hoje, passo a passo? Me conta como se eu fosse fazer no teu lugar."

A pergunta 3 é a que importa. É dela que sai a skill — o resto é triagem.

Se a resposta vier vaga ("organizar as coisas"), pedir o último exemplo real:
"me conta a última vez que você fez isso, do começo ao fim".

### Passo 2 — Conferir o que já existe

Antes de propor, olhar `.claude/skills/`. Boa parte do que parece rotina nova já
está coberta por skill existente que o operador não sabia que existia — ou está
quase coberta, e o certo é editar a skill atual em vez de criar outra.

Dizer isso quando for o caso. Skill duplicada é pior que skill faltando: as duas
divergem com o tempo e ninguém sabe qual vale.

### Passo 3 — Propor

Pra cada rotina que vale virar skill:

```
### /<nome>
**O que faz:** <uma frase>
**Dispara quando:** <as frases que o operador falaria>
**Lê:** <arquivos de contexto>
**Entrega:** <o arquivo ou resultado, com o caminho>
**Economiza:** <tempo estimado por semana>
```

**Não propor skill pra tudo.** Rotina que acontece uma vez por trimestre não
compensa — o custo de manter a skill atualizada é maior que o de fazer na mão.
Dizer isso quando for o caso.

O corte prático: repete pelo menos duas vezes por mês, e tem passo a passo estável.

### Passo 4 — Criar

Pras aprovadas:

1. Perguntar se é específica desse cliente ou útil em qualquer:
   - Específica → `.claude/skills/<nome>/SKILL.md`
   - Universal → `~/.claude/skills/<nome>/SKILL.md` (vale em todos os clientes)
2. Escrever o `SKILL.md` com frontmatter (`name`, `description` com os gatilhos),
   workflow em passos e seção de regras
3. Ler `_memoria/empresa.md` e `marca/guia-de-marca.md` pra calibrar
4. Arquivo de apoio (template, checklist, critério) vai dentro da pasta da skill
5. **Rodar a skill uma vez, na frente do operador**, no caso real que ele acabou de
   descrever. Skill que nunca rodou é palpite escrito em markdown

### Passo 5 — Resumo

```
Criadas:
✓ /<nome> — <o que faz> (<local ou global>)

Testada: /<nome> rodou em <caso real>
Registrado em CLAUDE.md e indice.md
```

Atualizar o `CLAUDE.md` com a skill nova e oferecer o `/salvar`.

## Regras

- **A skill descreve o processo do operador, não um processo ideal.** Se ele faz em
  4 passos, a skill tem 4 passos. Melhorar o processo é outra conversa
- Não criar skill sem os gatilhos na `description` — skill que o Claude não sabe
  quando usar não é usada
- Não criar mais de 3 skills numa sessão. Skill boa leva tempo, e cinco medianas
  valem menos que uma que funciona
- Rotina que envolve senha, pagamento ou envio pra fora: a skill prepara e mostra,
  quem dispara é o operador
