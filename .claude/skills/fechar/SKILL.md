---
name: fechar
description: >
  Fecha a sessão destilando a conversa pra memória do repo — o que foi decidido,
  o que mudou no cliente, o que se aprendeu, o que ficou pendente. Propõe onde
  salvar cada item, mostra antes de escrever e atualiza o índice. Use quando o
  usuário disser "fechar", "encerrar", "salva o que conversamos", "/fechar", ou
  ao terminar uma conversa que gerou decisão, aprendizado ou fato novo.
---

# /fechar — Fechamento de sessão

O que não é escrito, evapora. Daqui a três meses o operador não vai lembrar por
que o cliente vetou aquele tema.

**Não confundir com as vizinhas:**

| Skill | O que faz |
|---|---|
| `/fechar` | destila a **conversa** |
| `/atualizar` | varre o **repositório** |
| `/salvar` | git commit + push |

## Workflow

### 1. Reler a sessão

Separar o que apareceu em cinco baldes:

- **Decisão** — bateu o martelo em alguma coisa
- **Fato novo do cliente** — produto, preço, pessoa, canal, concorrente, prazo
- **Aprendizado** — o que provou ou desmentiu uma hipótese de marketing
- **Pendência** — ficou em aberto, precisa voltar
- **Correção** — o operador corrigiu tom, formato ou jeito de trabalhar

Ignorar execução pura sem consequência (gerou um texto, respondeu uma dúvida).
Se a sessão não produziu nada dos cinco, dizer "nada dessa sessão precisa virar
memória" e parar.

### 2. Escolher o destino

Antes de propor nota nova, **buscar no repo** por nome e por tema. Se já existe
nota do assunto, editar ela.

| Balde | Destino padrão |
|---|---|
| Decisão | nota em `notas/` com `#tipo/decisao` |
| Fato do cliente | `_memoria/empresa.md` |
| Fato do contrato | `_memoria/operacao.md` |
| Aprendizado | nota com `#tipo/aprendizado`; se for de um post, o rodapé do próprio post |
| Pendência | `indice.md`, tabela "Em aberto", com data |
| Correção de voz | `marca/guia-de-marca.md` |
| Correção de foco | `_memoria/estrategia.md` |
| Regra do sistema | `CLAUDE.md` |

Opinião crua sobre o cliente, valor de contrato, conflito interno →
`notas/privado/`. Nunca no versionado.

### 3. Mostrar antes de escrever

```
Da sessão de hoje, 4 coisas pra salvar:

1. [decisão] Cliente vetou falar de preço no Instagram
   → marca/guia-de-marca.md, "Assuntos que a empresa não toca"

2. [fato] Contratou uma recepcionista nova que responde o WhatsApp
   → _memoria/empresa.md, "Quem faz o quê"

3. [aprendizado] Post de bastidor teve 3x o salvamento do post institucional
   → notas/o-que-rende-no-instagram.md (existe, vou editar)

4. [pendência] Falta o acesso ao Google Meu Negócio
   → indice.md, "Em aberto", espera o cliente

Salvo tudo, algumas ou nenhuma?
```

Uma linha por item. Balde entre colchetes, o fato, seta com o destino.
Nada é escrito antes da resposta.

### 4. Aplicar

- Cirurgia: só a linha relevante. Nunca reformatar o arquivo inteiro
- Seguir as regras de vault do `CLAUDE.md` — link no corpo, nome exato, tag
- Nota nova nasce de `templates/notas/nota.md`
- Atualizar `indice.md`
- Mostrar o diff

### 5. Fechar

> "Salvo. Rodo o `/salvar` pra subir?"

## Regras

- **Não inventar.** Só entra o que aconteceu na conversa. Se a lembrança estiver
  vaga, perguntar
- **Não duplicar.** Buscar antes; nota existente se edita
- **Contradição se mostra, não se resolve.** Se o que a sessão diz contradiz o
  repo, mostrar os dois e perguntar qual vale
- Escrever direto, com nome, data e número. Não fazer ata
- Se o operador responder "nenhuma", não insistir
