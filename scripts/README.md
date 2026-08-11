# Scripts

## Radar automático

Faz o `/radar` rodar sozinho, sem ninguém na frente. Todo dia útil o briefing de
pautas aparece em `pesquisa/radar/`, pronto pra abrir.

**Antes de agendar, duas condições:**

1. `pesquisa/fontes.md` precisa existir — a primeira rodada do `/radar` na mão é
   que monta o mapa de fontes do nicho. O script se recusa a rodar sem isso
2. Pelo menos **duas rodadas na mão aprovadas** pelo operador. Radar automático em
   cima de fontes erradas produz lixo todo dia, com pontualidade

**Agendar:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\agendar-radar.ps1
```

Pergunta o horário e cria a tarefa no Agendador do Windows: de segunda a sexta,
no horário escolhido. Se a máquina estiver desligada na hora, roda assim que
ligar. Não precisa de administrador.

**Testar sem esperar:**

```powershell
Start-ScheduledTask -TaskName "Farol OS - Radar <nome-da-pasta>"
```

**Rodar na mão:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\radar-diario.ps1
```

**Desagendar:**

```powershell
Unregister-ScheduledTask -TaskName "Farol OS - Radar <nome-da-pasta>" -Confirm:$false
```

## Frequência

Escolher pelo ritmo do setor, não pelo hábito:

| Setor | Frequência |
|---|---|
| Muda toda hora — tributário, crédito, jurídico, câmbio | diário |
| Ciclo mensal — varejo, serviço local, saúde | 2 a 3 vezes por semana |
| Ciclo lento — indústria, B2B de contrato longo | semanal |

Diário num setor parado gera briefing vazio, e briefing vazio treina o operador a
não abrir mais o arquivo. Aí a automação inteira vira ruído.

## Log

Cada rodada escreve em `pesquisa/radar/_log/AAAA-MM-DD.log`.

O script julga pela **entrega, não pelo código de saída**: se o briefing foi
gerado, a rodada é OK mesmo que o Claude tenha saído com erro no fim (acontece ao
bater limite de uso com o arquivo já salvo). Sem briefing na pasta é que é falha.

## Um detalhe que quebra tudo

Os `.ps1` são **ASCII puro**, sem acento e sem travessão, de propósito. O
PowerShell 5.1 lê arquivo sem BOM como ANSI, o travessão vira aspas curvas, e o
parser trata como fim de string. Ao editar, manter assim.
