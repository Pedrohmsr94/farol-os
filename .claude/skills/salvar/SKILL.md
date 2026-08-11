---
name: salvar
description: >
  Salva o trabalho do repositório no GitHub (commit + push). Na primeira vez,
  configura o repositório remoto do cliente. Use quando o usuário disser
  "salvar", "salva no github", "commit", "push", "/salvar", ou pedir backup.
---

# /salvar — Commit e push

## Workflow

### 1. Conferir o estado

Rodar `git status` e `git remote -v`.

### 2. Primeira vez (sem remote, ou remote apontando pro Farol OS modelo)

Se o remote não existe, ou ainda aponta pro repositório-modelo do Farol OS:

> "Esse repo ainda não tem destino próprio *(ou: ainda aponta pro modelo do
> Farol OS)*. Cada cliente precisa do repositório dele — senão o trabalho de
> um cliente sobe no repo de outro.
>
> Cria um repositório **privado** no GitHub com o nome do cliente e me manda a
> URL. Se preferir, eu crio pelo `gh` se você tiver ele instalado."

Configurar com `git remote set-url origin <url>` (ou `add`).

**Privado é o padrão.** Se o operador pedir público, confirmar uma vez —
o repo tem dado de cliente dentro.

### 3. Checagem antes de subir

Antes do commit, rodar `git status --porcelain` e conferir se algo em
`notas/privado/` ou `dados/` entrou. Se entrou, parar e avisar — o `.gitignore`
está furado.

Se aparecer arquivo com cara de credencial (`.env`, `senha`, `credenciais`,
`token`), parar e perguntar antes de qualquer coisa.

### 4. Commit

Mensagem em português, dizendo o que mudou de verdade — não "atualiza
arquivos". Uma linha, no imperativo:

- `Adiciona diagnóstico de marketing`
- `Escreve os 4 posts da pauta de setembro`
- `Fecha o relatório de agosto`

Se a sessão mexeu em coisas sem relação, fazer commits separados.

### 5. Push

`git push`. Se falhar por autenticação, explicar em uma linha o que fazer
(`gh auth login` ou token) e parar — não tentar contornar.

Se falhar por divergência, mostrar o que tem no remoto antes de sugerir
qualquer `pull` ou `merge`. Nunca `push --force` sem o operador pedir.

### 6. Confirmar

```
Subiu. <n> arquivos · <mensagem do commit>
<url do repo>
```

## Regras

- Nunca commitar sem olhar o que está sendo commitado
- Nunca `git add -A` sem ter rodado `git status` antes na mesma sessão
- Não criar branch nem PR — esse repo é linear, um operador só
