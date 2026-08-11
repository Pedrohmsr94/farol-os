---
name: abrir
description: >
  Abre a sessão de trabalho carregando a memória do cliente (empresa, operação,
  estratégia, guia de marca, índice) e devolve uma síntese de quatro linhas com
  o que está pendente. Use quando o usuário disser "abrir", "começar",
  "/abrir", ou no primeiro turno de uma sessão de trabalho.
---

# /abrir — Abertura de sessão

Curto. Carrega contexto e devolve o estado do cliente em poucas linhas.

## Workflow

1. Ler, em ordem:
   - `_memoria/empresa.md`
   - `_memoria/operacao.md`
   - `_memoria/estrategia.md`
   - `marca/guia-de-marca.md`
   - `indice.md`
   - `conteudo/calendario.md` (só o mês corrente)

2. Se `_memoria/empresa.md` estiver em placeholder:

   > "A memória ainda não foi preenchida. Rodar `/instalar` agora?"

   E parar.

3. Conferir quatro coisas e mencionar só quando forem verdade:
   - `marca/guia-de-marca.md` em branco → avisar que conteúdo vai sair genérico
   - `diagnostico/diagnostico.md` não existe → avisar que não tem baseline
   - `pesquisa/fontes.md` não existe → avisar que o `/radar` ainda não foi montado
   - itens em "Em aberto" no `indice.md` parados há mais de 15 dias

4. Responder no formato:

```
<Empresa> — <o que vende, 5-8 palavras>
Objetivo: <objetivo do trimestre em uma frase>
Fila: <n> na aprovação · <n> pauta sem escrever
Estoque: <n> pautas do radar não usadas · último radar <data>
Aberto: <o item mais velho, ou "nada">

O que vamos fazer?
```

A linha "Estoque" é o que evita a pergunta "sobre o que a gente posta hoje?".
Se houver pauta guardada, ela já está ali.

5. Não listar arquivos lidos. Não confirmar leitura.

## Regras

- Máximo 6 linhas
- Só uma pergunta: "o que vamos fazer?"
- Alerta só quando for verdade. Repetir toda sessão que o guia está em branco
  vira ruído — dizer uma vez por sessão e seguir
