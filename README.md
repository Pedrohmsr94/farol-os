# Farol OS

> O marketing de uma empresa, organizado dentro do Claude Code.

Marketing de pequena empresa não quebra por falta de ideia. Quebra porque
ninguém sabe o que foi feito mês passado, ninguém definiu como a marca fala, e
o relatório é um print de alcance mandado no WhatsApp.

O Farol OS resolve isso: um repositório por cliente, com a memória da empresa,
a voz da marca, o calendário, a fila de conteúdo e o relatório — tudo em texto,
versionado, e lido pelo Claude antes de cada resposta.

Um repo, uma empresa. Você clona de novo pro próximo cliente.

---

## Instalando

### Pelo Claude (mais rápido)

Abre o Claude Code em qualquer pasta e cola:

```
Clona o https://github.com/SEU-USUARIO/farol-os.git na pasta atual,
entra nela e roda o /instalar.
```

### Pelo terminal

```
git clone https://github.com/SEU-USUARIO/farol-os.git nome-do-cliente
cd nome-do-cliente
code .
```

No VS Code: terminal integrado → `claude` → `/instalar`.

O `/instalar` roda uma vez por cliente. Ele te entrevista sobre a empresa,
monta a memória e configura o sistema. Leva uns 10 minutos.

Depois de instalar, apague o histórico do repositório de origem pra esse
cliente começar com git limpo:

```
rm -rf .git && git init && git add -A && git commit -m "Farol OS instalado"
```

---

## A esteira

Nenhuma peça pula uma etapa. **Todo conteúdo nasce de pesquisa, nunca de opinião
solta** — e o controle de qualidade reprova peça que não tem raiz pesquisada.

```
/radar  →  /angulos  →  /calendario  →  produção  →  /revisar  →  /aprovar-post
                                                                       ↓
                        o resultado volta pro arquivo da peça  ←  /semana
                        e realimenta o calendário do mês seguinte
```

## As skills

**Começo de contrato**

`/instalar` monta a memória da empresa numa entrevista · `/diagnostico` mapeia
onde o marketing está furado hoje — canais, funil, quem faz o quê, o que é
medido — e vira o documento da primeira reunião · `/marca` extrai voz, público e
território de palavras, e gera o guia que todas as outras skills leem antes de
escrever.

**Pesquisa**

`/radar` varre notícia, norma, decisão, mercado e a conversa real do público do
nicho, e entrega 5 a 8 pautas fichadas com fato, fonte, ângulo e formato. Na
primeira rodada ele monta o mapa de fontes daquele setor — o resto é automático,
e dá pra agendar · `/investigar` levanta a voz real do dono, analisa os perfis de
referência do nicho e coleta comentário do público · `/seo` roda os 7 passos de
SEO e GEO, do levantamento de demanda a aparecer nas respostas do ChatGPT.

**Planejamento e produção**

`/angulos` pega um tema e devolve 5 ângulos narrativos diferentes, depois mostra
como o escolhido vira carrossel, reel, LinkedIn ou artigo — é o que faz uma
pesquisa render quatro semanas de conteúdo em vez de um post · `/calendario`
monta a pauta do mês a partir dos ângulos, da estratégia e do que já rendeu ·
`/post` escreve a peça de texto · `/carrossel` gera os slides 1080×1350 na
identidade da marca, com legenda · `/publicar-tema` faz o pacote completo:
artigo, carrossel e as três legendas, amarrados.

**Qualidade e publicação**

`/revisar` julga a peça contra critério escrito e devolve veredito — aprovado,
aprovado com ajustes ou reprovado, com o trecho problemático citado. Roda em
subagente pra ter olhos frescos · `/aprovar-post` publica e registra.

**Ritmo**

`/semana` fecha a semana e preenche o resultado das peças publicadas — é o que
faz o sistema aprender · `/relatorio` fecha o mês num documento que o cliente
entende, sem esconder o que caiu.

**Operação e apoio**

`/abrir` carrega o contexto · `/fechar` destila a conversa pra memória ·
`/salvar` faz commit e push · `/atualizar` varre o repo e corrige o que
desencontrou · `/mapear-rotinas` transforma o que você repete em skill nova ·
`/analisar-dados`, `/email-profissional` e `/responder-avaliacoes` para o dia a
dia.

---

## Como o sistema pensa

`_memoria/` é o cérebro. Quem é a empresa, quem opera, o que está em foco.
O Claude lê antes de cada resposta. Quanto melhor a memória, melhor o sistema.

`marca/` é a voz. Sem ela, todo texto sai com cara de qualquer empresa do
mesmo setor — o defeito mais caro do marketing terceirizado.

`conteudo/` e `relatorios/` são o resultado, com data e histórico. No fim do
contrato o cliente tem um registro do que foi feito, não uma pasta de PNG solto.

Três regras que o sistema não quebra: não inventa número, não escreve sem voz
definida, e não maquia queda em adjetivo.

---

## Requisitos

- [Claude Code](https://claude.com/claude-code)
- Git
- VS Code (opcional, mas é onde fica confortável)
- [Obsidian](https://obsidian.md) (opcional — abre a pasta como cofre e vira grafo)
