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

## As skills

**Começo de contrato**

`/instalar` monta a memória da empresa numa entrevista ·
`/diagnostico` mapeia onde o marketing está furado hoje — canais, funil, quem
faz o quê, o que é medido — e vira o documento que você mostra na primeira
reunião · `/marca` extrai voz, público e território de palavras, e gera o guia
que todas as outras skills leem antes de escrever.

**Produção**

`/calendario` monta a pauta do mês a partir da estratégia e do que já rendeu ·
`/post` escreve o conteúdo na voz da marca e joga na fila de aprovação.

**Ritmo**

`/semana` fecha a semana: o que saiu, o que rendeu, o que trava ·
`/relatorio` fecha o mês num documento que o cliente entende — sem esconder o
que caiu.

**Operação**

`/abrir` carrega o contexto antes de trabalhar · `/fechar` destila a conversa
pra memória · `/salvar` faz commit e push · `/atualizar` varre o repo e corrige
a memória desatualizada.

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
