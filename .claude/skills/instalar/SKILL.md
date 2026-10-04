---
name: instalar
description: >
  Instala o Farol OS pra uma empresa. Entrevista sobre o negócio, o combinado do
  contrato e o foco de marketing, e preenche `_memoria/empresa.md`,
  `_memoria/operacao.md`, `_memoria/estrategia.md`, `indice.md` e a seção final do
  `CLAUDE.md`. Use quando o usuário acabou de clonar o repositório pra um cliente
  novo, ou quando pedir "instalar", "primeiro setup", "/instalar".
---

# /instalar — Setup de um cliente

Primeiro comando depois de clonar. Roda uma vez por cliente.

É conversa de descoberta, não formulário. Uma pergunta por vez, esperando a
resposta. Se vier vago, pedir concretude uma vez — e só uma. Depois registra o
que veio e segue.

O sistema tem que sair daqui sabendo quem é a empresa, quem opera, e onde está
o atrito.

---

## Pré-checagem

**1. Nome da pasta.** Rodar `basename "$(pwd)"`. Se for `farol-os`, `Farol-OS`,
`farol-os-main` ou variação genérica, avisar:

> "A pasta ainda tem nome genérico ('<nome>'). Ela vai ser a pasta desse
> cliente — no fim eu te lembro de renomear. Bora começar?"

Guardar o nome pra Fase 5.

**2. Memória já preenchida.** Conferir se `_memoria/empresa.md`,
`_memoria/operacao.md` ou `_memoria/estrategia.md` têm conteúdo real (não
placeholder). Se tiverem:

> "Já tem contexto preenchido aqui. Sobrescrevo do zero ou complemento o que falta?"

**3. Git de origem.** Se `git log` mostrar histórico do repositório-modelo,
avisar no fim (Fase 5) que dá pra zerar.

---

## Fase 1 — A empresa

1. "Qual o nome da empresa e o que ela vende? Fala do jeito que o dono falaria."
2. "Onde ela atua? Cidade, região, ou é online?"
3. "Quem paga? Descreve um cliente real que ela atendeu esse mês — não persona."
4. "Quanto custa o que ela vende? Faixa serve."
5. "Quem trabalha lá e quem decide? Quem vai aprovar o conteúdo?"
6. "Quem disputa o mesmo cliente na região, e o que eles fazem melhor?"

## Fase 2 — Onde ela já está

7. "Onde a empresa tem presença hoje? Instagram, Google Meu Negócio, site,
   WhatsApp — e quais estão abandonados."
8. "O que já foi tentado em marketing? Agência, impulsionamento, panfleto.
   O que deu certo, o que não deu, e por quê."
9. "Tem algum número na mão hoje? Seguidor, mensagem por semana, orçamento por
   mês, faturamento. Se não tiver, tudo bem — a gente mede depois."

Se ele não souber os números, **não inventar**. Registrar "não medido" e
marcar como primeira tarefa do `/diagnostico`.

## Fase 3 — O combinado

10. "O que está dentro do contrato, e o que está fora? A parte de fora é a
    que mais importa."
11. "Quantas entregas por mês, e com que ritmo de reunião?"
12. "Quem no cliente aprova conteúdo, e em quanto tempo ele costuma responder?"

## Fase 4 — Foco

13. "Qual o objetivo dos próximos três meses? Um só, e que dê pra verificar
    no fim."
14. "Se o marketing dessa empresa está travado hoje, travado em quê?"
15. "Tem data marcada no calendário dela? Sazonalidade, campanha, fechamento,
    evento."

## Fase 5 — O nicho

Essas três alimentam o `/radar`, que é o que faz o conteúdo nascer de pesquisa em
vez de opinião. Não pular.

16. "Quando alguma coisa muda no mundo e o telefone dessa empresa toca, o que
    mudou?"
17. "Que órgão, entidade, conselho ou publicação manda no setor dela?"
18. "Onde o cliente final dela reclama e tira dúvida na internet?"

Registrar as respostas em `_memoria/empresa.md`, numa seção **"O nicho"**. O
`/radar` usa elas na primeira rodada pra montar `pesquisa/fontes.md` — e é lá que
a pesquisa de verdade acontece, não aqui.

---

## Preenchimento

| Arquivo | Vem das perguntas |
|---|---|
| `_memoria/empresa.md` | 1-9, e 16-18 na seção "O nicho" |
| `_memoria/operacao.md` | 10-12 |
| `_memoria/estrategia.md` | 13-15 |
| `indice.md` | nome da empresa, fase, data |
| `CLAUDE.md` seção "A empresa" | 1, e regras específicas que apareceram |

**Regras de escrita:**

- Escrever com as palavras do operador, não traduzir pra corporativês
- Campo sem resposta fica vazio com `*(não perguntado)*` ou `*(não medido)*` —
  nunca preenchido com suposição plausível
- Não deixar texto de placeholder nos arquivos finais
- Setor regulado (saúde, direito, contabilidade, financeiro): registrar em
  `CLAUDE.md`, seção "Regras específicas", que existe conselho com restrição de
  publicidade — mesmo sem saber a regra ainda

**Objetivo mal formulado.** Se a resposta 13 vier como "mais visibilidade" ou
"crescer o Instagram", devolver uma vez:

> "Isso não dá pra verificar em três meses. O que teria que acontecer no
> negócio pra você dizer que valeu? Mais orçamento? Mais gente ligando?"

Registrar a versão verificável. Se ele insistir no vago, registrar como veio e
anotar em `estrategia.md` que o objetivo ainda precisa de número.

---

## Fase 6 — Fechamento

Mostrar:

```
✓ Empresa          _memoria/empresa.md
✓ Operação         _memoria/operacao.md
✓ Estratégia       _memoria/estrategia.md
✓ Índice           indice.md
✓ CLAUDE.md        seção da empresa preenchida
○ Guia de marca    em branco — roda /marca
○ Diagnóstico      não feito — roda /diagnostico
○ Fontes do nicho  não montadas — a 1ª rodada do /radar monta
○ Arquitetura      em branco — roda /arquitetura-editorial depois do /marca
```

**Se a pasta tem nome genérico**, gerar slug da empresa (minúscula, sem acento,
espaço vira hífen) e instruir:

> "Renomeia a pasta pra '<slug>': fecha o VS Code, renomeia no Explorer,
> abre de novo."

**Se o git ainda tem histórico do modelo:**

> "O repo ainda carrega o histórico do Farol OS. Pra esse cliente começar
> limpo: `Remove-Item -Recurse -Force .git; git init; git add -A; git commit -m 'Farol OS instalado'` (PowerShell).
> Quer que eu rode?"

Terminar:

> "Pronto. O sistema já conhece a <empresa>.
>
> A ordem daqui:
> 1. `/diagnostico` — vira o documento da primeira reunião
> 2. `/marca` — pra nenhum texto sair genérico
> 3. `/radar` — a primeira rodada monta o mapa de fontes do nicho. É a rodada
>    mais importante do contrato, e depois dela a pesquisa fica automática
> 4. `/arquitetura-editorial` — decide o que a marca defende e as linhas do
>    mês. Antes dela, `/ideias` e `/calendario` trabalham no provisório
>
> No dia a dia: `/abrir` no começo, `/fechar` no fim."

---

## Regras

- 10 a 15 minutos. Se o operador enrolar numa pergunta, registra e segue
- Não fazer pergunta fora da lista sem motivo claro
- Não sugerir estratégia durante a entrevista. Aqui é coleta — o diagnóstico
  é a próxima skill
