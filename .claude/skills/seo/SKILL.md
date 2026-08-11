---
name: seo
description: >
  Fluxo completo de SEO e GEO em 7 passos: pesquisa de demanda, análise de
  concorrência, Google Meu Negócio, otimização on-page, estratégia de conteúdo,
  checklist de monitoramento e GEO (aparecer nas respostas de IAs como ChatGPT,
  Gemini e Perplexity). Use quando o usuário pedir "seo", "geo", "palavras-chave",
  "aparecer no google", "aparecer no chatgpt", "google meu negócio", "gmb",
  "analisar concorrência", "/seo".
---

# /seo — SEO + GEO

Sete passos, na ordem. Dá pra rodar tudo de uma vez ou um passo por sessão — mas
não pular a ordem: cada passo usa o anterior.

Saída: `pesquisa/seo/`, um arquivo por passo.

## Dependências

- `_memoria/empresa.md`, `_memoria/estrategia.md`, `marca/guia-de-marca.md`
- WebSearch e WebFetch

---

## Passo 1 — Demanda

**Saída:** `pesquisa/seo/01-pesquisa-demanda.md`

O que o público realmente digita. Não o que a empresa acha que ele digita.

- Levantar 30 a 50 termos, agrupados por **intenção**: informacional ("o que é",
  "como funciona"), comercial ("melhor", "vale a pena", "quanto custa") e
  transacional ("perto de mim", "contratar", "preço")
- Puxar o autocomplete do Google e a seção "As pessoas também perguntam"
- Anotar o termo **com a cidade** quando for negócio local. "Contador" e "contador
  em Jataí" são mercados diferentes
- Marcar os termos que a empresa consegue atender de verdade. Ranquear pra serviço
  que ela não presta é tráfego que dá trabalho e não vira nada

Sem ferramenta paga, o volume é estimado. **Dizer isso no arquivo** em vez de
escrever número com cara de exato.

## Passo 2 — Concorrência

**Saída:** `pesquisa/seo/02-analise-concorrencia.md`

Pros 10 termos mais importantes: quem aparece, e por quê.

- Que tipo de página ganha — blog, página de serviço, GMB, diretório, marketplace
- Que profundidade tem o conteúdo que está em primeiro
- O que **ninguém** respondeu direito. É essa a brecha
- Se quem ranqueia são só diretórios e agregadores, o termo está fácil. Se são
  empresas grandes com conteúdo denso, escolher outra briga

## Passo 3 — Google Meu Negócio

**Saída:** `pesquisa/seo/03-gmb.md`

É o passo de resultado mais rápido pra negócio local, e o mais abandonado. Fazer
antes de qualquer coisa de site.

Checklist:

- [ ] Perfil existe, é reivindicado e está verificado
- [ ] Categoria principal certa (e secundárias)
- [ ] Nome, endereço e telefone exatamente iguais aos do site e das redes
- [ ] Horário de funcionamento correto, feriado incluído
- [ ] Descrição com os termos do passo 1, escrita na voz da marca
- [ ] Serviços e produtos cadastrados um a um
- [ ] Fotos reais, recentes, e mais de dez
- [ ] Perguntas e respostas populadas pela própria empresa
- [ ] Avaliações sendo respondidas (`/responder-avaliacoes`)
- [ ] Posts do GMB publicados com alguma regularidade

Cada item não marcado vira tarefa com responsável.

## Passo 4 — On-page

**Saída:** `pesquisa/seo/04-onpage.md`

Só se o cliente tem site. Se não tem, registrar que esse passo está bloqueado e
seguir — não vender site aqui, isso é conversa de escopo.

- Title e meta description por página, com o termo e a cidade
- Um H1 por página, H2 por seção
- URL curta em kebab-case
- Velocidade e mobile: medir, não achar
- Schema.org — `LocalBusiness` no mínimo, e o específico do setor quando existir
- Link interno entre artigo e página de serviço

## Passo 5 — Estratégia de conteúdo

**Saída:** `pesquisa/seo/05-estrategia-conteudo.md`

A lista mestra de temas, cruzando o passo 1 com a brecha do passo 2.

Organizar em **grupos**: um tema-mãe (o serviço) e os artigos-satélite que
respondem as dúvidas em volta dele, todos linkando pro tema-mãe.

Pra cada tema: palavra-chave, intenção, formato, prioridade. É essa lista que
alimenta o `/calendario` e o `/publicar-tema` quando o `/radar` não tiver pauta
melhor.

## Passo 6 — Monitoramento

**Saída:** `pesquisa/seo/06-monitoramento.md`

Checklist mensal, curto o bastante pra ser feito de verdade:

- Posição dos 10 termos principais
- Buscas e ações no GMB (do painel, não estimado)
- Tráfego orgânico e as páginas que mais entram
- Quantas mensagens ou ligações vieram de busca
- O que os concorrentes publicaram

Vira insumo do `/relatorio`.

## Passo 7 — GEO

**Saída:** `pesquisa/seo/07-geo.md`

Aparecer nas respostas de ChatGPT, Gemini, Perplexity e da IA do próprio Google.
Cada vez mais gente pergunta pra IA antes de buscar.

O que muda em relação a SEO clássico:

- **Responder a pergunta na primeira frase**, e só depois desenvolver. IA cita
  quem responde direto
- Estrutura de pergunta e resposta explícita, com H2 em forma de pergunta
- Dado com fonte e data no corpo do texto — IA prefere o que consegue atribuir
- Entidade clara: nome da empresa, cidade, serviço e diferencial escritos de forma
  inequívoca em algum lugar do site
- Presença em fontes que as IAs leem: GMB, diretórios do setor, associações,
  perfis profissionais

**Testar:** perguntar pra três IAs o que um cliente perguntaria ("melhor contador
pra empresa do Simples em Jataí") e registrar o que elas respondem hoje. É o
baseline. Repetir em três meses.

---

## Execução

Perguntar por onde começar. Se o operador não souber:

> "Se o cliente é negócio local e o GMB está abandonado, o passo 3 dá resultado em
> semanas e não depende de site. Começo por ele?"

Rodar um passo por vez, salvando o arquivo antes de seguir.

## Regras

- **Volume estimado é estimado.** Sem ferramenta paga, dizer isso no arquivo
- **Não prometer posição nem prazo.** Nem no material interno — vira promessa no
  relatório depois
- Não recomendar tática de risco: comprar link, texto escondido, página duplicada,
  review falsa. Além de errado, quebra o negócio do cliente quando o Google pega
- Termo que a empresa não atende não entra na lista
- Anúncio pago está fora do escopo do Farol OS. Se aparecer oportunidade clara,
  registrar como recomendação pro cliente, não como tarefa
