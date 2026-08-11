---
name: angulos
description: >
  Pega um tema (pauta do /radar, tema de SEO ou ideia solta) e devolve ângulos
  narrativos diferentes pra abordá-lo, e depois mostra como o ângulo escolhido vira
  cada formato — carrossel, roteiro de reel, vídeo longo, post de LinkedIn e artigo.
  Serve pra não gastar o tema num ângulo óbvio e pra extrair várias peças distintas
  de uma pesquisa só. Use quando o usuário disser "que ângulos dá pra esse tema",
  "como abordar isso", "transforma essa pauta em reel", "de quantos jeitos dá pra
  contar isso", "/angulos", ou como primeiro passo do /publicar-tema.
---

# /angulos — Ângulos narrativos e tratamento por formato

Um tema pesquisado é caro. Gastar ele num único ângulo óbvio é desperdício —
principalmente aqui, onde cada pauta nasce de varredura de fonte primária.

Duas fases, com o operador decidindo entre elas.

## Dependências

- **Pauta de origem:** `pesquisa/radar/`
- **Voz:** `marca/guia-de-marca.md` — obrigatório
- **Voz real do dono:** `pesquisa/investigacoes/voz.md`, se existir (do `/investigar`)
- **Contexto:** `_memoria/empresa.md`
- **Saída:** `pesquisa/angulos/<slug-do-tema>-<AAAA-MM-DD>.md`

---

## Fase 1 — Os ângulos

Escolher **5 famílias** das 7 abaixo, as que melhor servem ao tema. Nunca as mesmas
5 sempre — o tema é que manda.

| Família | O que é | Quando usar |
|---|---|---|
| **O mecanismo** | Como a coisa funciona por dentro: a regra por trás da regra, o que a outra parte pode e não pode, por que uma norma vence a outra | Prova técnica pura. É o ângulo que mais constrói autoridade |
| **O erro caro** | O que quase todo mundo faz errado, e quanto custa | Alto engajamento, e evita soar professoral porque fala de consequência |
| **A conta** | Números concretos: quanto custa, quanto sobra, quanto se perde | Rende carrossel de número grande |
| **A janela** | Algo com data e prazo real | Urgência legítima. Cuidado com o bloqueio de alarmismo |
| **A história** | Caso real anonimizado, ou a origem do dono | Humaniza sem abrir mão da lição técnica. Usar com parcimônia |
| **O contraponto** | O que se diz por aí e por que está incompleto | Diferencia sem citar ninguém. **Nunca** nomear concorrente |
| **A pergunta** | Responder literalmente uma dúvida real do público | Melhor fonte: "Radar de perguntas" dos briefings e `pesquisa/investigacoes/comentarios/` |

Para cada um dos 5:

```markdown
### Ângulo N — [nome curto] (família: [qual])

**A tese em uma frase:** [o que essa peça afirma]
**Fala com:** [qual recorte do público]
**Por que serve ao posicionamento:** [1 linha — prova técnica? autoridade? qualificação de lead?]
**Primeira linha:** "[escrita de verdade, pronta pra usar]"
**Formato natural:** [qual formato da fase 2 carrega melhor esse ângulo]
**Risco:** [só quando houver — alarmismo, promessa, demanda acima da capacidade]
```

**Parar aqui e perguntar qual ângulo seguir.** Não escolher sozinho. Se o operador
pedir mais de um, seguir com todos — ângulos diferentes do mesmo tema viram peças
diferentes, e é exatamente pra isso que essa skill existe.

---

## Fase 2 — O mesmo ângulo em cada formato

Com o ângulo escolhido, mostrar **como ele vira cada formato**. Não é o mesmo texto
recortado: cada formato tem lógica narrativa própria, e um ângulo que brilha em
carrossel pode morrer em reel.

### Carrossel (1080x1350)

7 a 10 slides. Entregar a **estrutura**, não o texto final:

- **Capa** — a tensão, não o resumo. Uma ideia, letra grande
- **Slides 2-3** — contexto: o fato e por que importa
- **Slides 4-6** — o desenvolvimento: a conta, o mecanismo, os passos
- **Penúltimo** — a implicação prática
- **Último** — CTA, qualificando (nunca convite aberto)

Dizer também qual a **sequência de capa** (claro → foto/escuro → cor da marca) —
checar a peça mais recente em `conteudo/`.

### Roteiro de reel (30 a 60 segundos, à câmera)

Roteiro **com marcação de tempo e fala escrita**, não descrição do que dizer:

```
0-3s   [gancho — a frase que segura. Sem "oi pessoal", sem apresentação]
3-10s  [o fato, concreto e datado]
10-35s [o desenvolvimento: 2 pontos, não 5. Reel não comporta lista]
35-50s [a implicação — o que a pessoa faz com isso]
50-60s [fechamento + CTA falado, curto]
```

Marcar onde entra **corte, texto na tela e B-roll**. Escrever como a pessoa fala,
não como se escreve — frase curta, sem oração subordinada longa, sem número que
exige ler duas vezes. Se `pesquisa/investigacoes/voz.md` existir, calibrar por ele.

### Vídeo longo / série documental

Só quando o ângulo pedir presença física — visita, bastidor, cliente. Estrutura de
documentário. **Quem apresenta pergunta e escuta, não ensina** — entregar as
*perguntas*, não o roteiro do que ele fala.

### LinkedIn

Texto longo analítico. Público diferente: parceiro, fornecedor, outro profissional
do setor. Aqui cabe o raciocínio técnico completo que não cabe no Instagram. Sem
"arraste pro lado", máximo 3 hashtags, abertura que não parece post de coach.

### Artigo (blog)

Outline com H2s, palavra-chave principal e a pergunta que o artigo responde pra IA
(GEO). É a peça-mãe: o carrossel e o reel apontam pra cá.

### Story

Quando servir: enquete, bastidor da pesquisa, "vocês pediram, saiu o artigo".
Formato de manutenção, não de aquisição.

---

## Fase 3 — Encaminhar

- Carrossel → `/carrossel`
- Artigo + carrossel + legendas → `/publicar-tema`
- Reel → entregar o roteiro em `conteudo/fila/<data>-<slug>/roteiro-reel.md`
- Peça de texto avulsa → `/post`
- Sempre, antes de publicar → `/revisar`

**Salvar o documento de ângulos mesmo que só um vire peça.** Os outros quatro ficam
disponíveis pro `/calendario` do mês seguinte — é assim que uma pesquisa vira quatro
semanas de conteúdo em vez de um post.

## Regras

- **Cinco ângulos de verdade diferentes.** Se dois se resumem à mesma frase, não são
  dois ângulos. Trocar um deles de família
- **Primeira linha sempre escrita.** "Um gancho sobre o prazo" não serve; "Faltam
  três meses e o que vão te pedir não é o seu problema — é o seu papel" serve
- Todo ângulo respeita `criterios.md` do `/revisar`. Ângulo que só funciona com
  promessa ou alarmismo não é ângulo, é armadilha — descartar na hora de propor
- Nunca citar concorrente, nem no ângulo do contraponto
- Se o tema veio de pauta com campo **"Atenção"**, esse aviso viaja junto pra todos
  os ângulos
