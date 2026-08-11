# agendar-radar.ps1 - cria a tarefa do Agendador de Tarefas do Windows
#
# Rodar uma vez, dentro da pasta do cliente:
#     powershell -ExecutionPolicy Bypass -File scripts\agendar-radar.ps1
#
# Cria uma tarefa que roda o /radar de segunda a sexta, no horario escolhido.
# Se a maquina estiver desligada na hora, a tarefa roda assim que ela ligar
# (StartWhenAvailable). Nao precisa de administrador.
#
# Pra desfazer:
#     Unregister-ScheduledTask -TaskName "Farol OS - Radar <cliente>" -Confirm:$false
#
# IMPORTANTE: manter este arquivo em ASCII puro. Ver o comentario em radar-diario.ps1.

$ErrorActionPreference = 'Stop'

$projeto = Split-Path -Parent $PSScriptRoot
$cliente = Split-Path -Leaf $projeto
$script  = Join-Path $PSScriptRoot 'radar-diario.ps1'
$tarefa  = "Farol OS - Radar $cliente"

if (-not (Test-Path $script)) {
    Write-Output "ERRO: nao achei $script"
    exit 1
}

$hora = Read-Host "Que horas o radar deve rodar? (formato 24h, ex: 08:00)"
if ([string]::IsNullOrWhiteSpace($hora)) { $hora = '08:00' }

Write-Output ""
Write-Output "Tarefa:   $tarefa"
Write-Output "Projeto:  $projeto"
Write-Output "Horario:  $hora, de segunda a sexta"
Write-Output ""

$acao = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`"" `
    -WorkingDirectory $projeto

$gatilho = New-ScheduledTaskTrigger -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At $hora

# StartWhenAvailable: se a maquina estava desligada na hora marcada, roda ao ligar.
# StartIfOnBatteries: notebook no fim de semana longe da tomada ainda roda.
$config = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

try {
    Register-ScheduledTask -TaskName $tarefa `
        -Action $acao -Trigger $gatilho -Settings $config `
        -Description "Varredura diaria do nicho - skill /radar do Farol OS" `
        -Force | Out-Null
}
catch {
    Write-Output "ERRO ao criar a tarefa: $($_.Exception.Message)"
    Write-Output ""
    Write-Output "Se disser acesso negado, abrir o PowerShell como administrador e rodar de novo."
    exit 1
}

Write-Output "Tarefa criada."
Write-Output ""
Write-Output "Testar agora, sem esperar o horario:"
Write-Output "    Start-ScheduledTask -TaskName `"$tarefa`""
Write-Output ""
Write-Output "Ver o resultado em: pesquisa\radar\"
Write-Output "Ver o log em:       pesquisa\radar\_log\"
