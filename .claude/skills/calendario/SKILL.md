---
name: calendario
description: >
  Monta a pauta do mês a partir do objetivo da estratégia, do que já rendeu nos
  posts publicados e das datas do setor, e escreve em `conteudo/calendario.md`.
  Use quando o usuário disser "montar a pauta", "calendário do mês", "o que
  vamos postar", "planejar conteúdo", "/calendario".
---

# /calendario — A pauta do mês

Roda uma vez por mês, antes de escrever qualquer post.

Pauta não é lista de assunto bonito. É a tradução do objetivo do trimestre em
coisas publicáveis — e se não der pra dizer como um tema ajuda o objetivo, ele
não entra.

Saída: uma seção nova no topo de `conteudo/calendario.md`.

---

## Passo 1 — Ler antes de propor

- `_memoria/estrategia.md` — o objetivo do trimestre e as datas com prazo
- `_memoria/empresa.md` — o que ela vende, pra quem, sazonalidade
- `marca/guia-de-marca.md` — voz, assuntos proibidos, prova disponível
- `_memoria/operacao.md` — **quantas entregas o contrato prevê**
- `conteudo/publicados/` — o rodapé "Resultado" dos últimos dois meses
- `conteudo/calendario.md` — o que ficou como `pauta` e nunca foi escrito

Se o guia de marca estiver em branco, avisar e perguntar se segue assim mesmo.

Se `_memoria/estrategia.md` não tiver objetivo do trimestre, parar e perguntar.
Pauta sem objetivo é conteúdo por conteúdo — é exatamente o que o cliente já
fazia antes de contratar.

---

## Passo 2 — Olhar o que rendeu

Dos posts publicados com resultado preenchido: quais formatos, temas e ângulos
performaram, e quais não.

Se nenhum post tem resultado preenchido, dizer:

> "Nenhum post publicado tem resultado registrado, então essa pauta é aposta,
> não leitura. Vou marcar dois temas como teste pra gente ter o que medir mês
> que vem."

Repetir o que funcionou é o trabalho — não é falta de criatividade.

---

## Passo 3 — Montar

**Quantidade:** a do contrato. Nem mais nem menos. Propor 12 posts num contrato
de 8 gera atraso e fila entupida.

**Mistura.** Toda pauta precisa das quatro:

| Tipo | Pra quê | Quanto |
|---|---|---|
| Resolve dúvida | tira a objeção que trava a venda | o grosso |
| Prova | caso, número, depoimento, bastidor | recorrente |
| Oferta | diz o que vende e como comprar | mínimo 1 |
| Teste | ângulo ou formato novo, pra medir | 1 a 2 |

Pauta só de dúvida não vende. Pauta só de oferta cansa e some do alcance.

**Datas.** Cruzar com o que tem prazo na estratégia — sazonalidade do setor,
fechamento, feriado que muda o horário, evento da cidade.

**Cada tema precisa responder:**

1. Que dúvida ou objeção ele ataca?
2. Como ele ajuda o objetivo do trimestre?
3. A empresa tem prova pra sustentar o que vai afirmar?

Se a 3 for não, o tema muda ou entra como pedido ao cliente ("preciso de uma
foto do serviço pronto pra esse aqui").

---

## Passo 4 — Escrever no calendário

Seção nova no topo de `conteudo/calendario.md`:

```markdown
## Setembro/2026

**Objetivo do mês:** <como esse mês empurra o objetivo do trimestre>

| Data | Tema | Formato | Canal | Status | Arquivo |
|---|---|---|---|---|---|
| 03/09 | Quanto custa atrasar a entrega do IR | carrossel | Instagram | pauta | — |
```

Nome do arquivo já definido aqui (`AAAA-MM-DD-tema-curto.md`), mesmo antes de
existir — é assim que o `/post` sabe onde salvar.

---

## Passo 5 — Fechar

Mostrar a tabela e:

```
<n> pautas pra <mês>. <n> resolvem dúvida · <n> prova · <n> oferta · <n> teste

Preciso de você: <lista do que depende do cliente — foto, dado, autorização>

Escrevo o primeiro agora? (/post)
```

Atualizar `indice.md` se alguma pauta virou pendência com o cliente.

---

## Regras

- **Não estourar o contrato.** Se o operador quiser mais, avisar que isso é
  trabalho fora do combinado antes de escrever a pauta
- **Não propor tema sem prova.** Conteúdo que afirma o que a empresa não pode
  sustentar é risco, principalmente em setor regulado
- **Não copiar trend.** Se sugerir formato que está bombando, dizer o que ele
  resolve pra esse cliente. Sem isso, não entra
- Pauta antiga que nunca foi escrita: perguntar se entra nesse mês ou é
  descartada. Não deixar apodrecer no arquivo
