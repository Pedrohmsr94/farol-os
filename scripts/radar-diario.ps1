# radar-diario.ps1 - roda a skill /radar sem ninguem na frente
#
# Chamado pelo Agendador de Tarefas do Windows. Pra criar a tarefa, rodar uma vez:
#     powershell -ExecutionPolicy Bypass -File scripts\agendar-radar.ps1
#
# Tambem da pra rodar na mao:
#     powershell -ExecutionPolicy Bypass -File scripts\radar-diario.ps1
#
# Saida: pesquisa/radar/AAAA-MM-DD.md
# Log:   pesquisa/radar/_log/AAAA-MM-DD.log
#
# --strict-mcp-config sem --mcp-config = nenhum servidor MCP sobe. E de proposito:
# servidor MCP que esteja fora do ar, sem saldo ou pedindo login derruba a rodada
# inteira, e nao tem ninguem na frente pra resolver.
#
# IMPORTANTE: manter este arquivo em ASCII puro (sem acento, sem travessao).
# O PowerShell 5.1 le .ps1 sem BOM como ANSI e o travessao vira aspas curvas,
# que o parser trata como fim de string. Quebra o script inteiro.

$ErrorActionPreference = 'Stop'

$projeto = Split-Path -Parent $PSScriptRoot
$hoje    = Get-Date -Format 'yyyy-MM-dd'

# Achar o claude.exe: primeiro o caminho padrao, depois o PATH
$claude = Join-Path $env:USERPROFILE '.local\bin\claude.exe'
if (-not (Test-Path $claude)) {
    $doPath = Get-Command claude -ErrorAction SilentlyContinue
    if ($doPath) { $claude = $doPath.Source }
}

$pastaLog = Join-Path $projeto 'pesquisa\radar\_log'
if (-not (Test-Path $pastaLog)) { New-Item -ItemType Directory -Path $pastaLog -Force | Out-Null }
$log = Join-Path $pastaLog "$hoje.log"

function Registrar($msg) {
    $linha = "[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $msg
    Add-Content -Path $log -Value $linha -Encoding utf8
    Write-Output $linha
}

Registrar "=== Radar de $hoje ==="

if (-not (Test-Path $claude)) {
    Registrar "ERRO: claude.exe nao encontrado. Instalar o Claude Code ou ajustar o caminho neste script."
    exit 1
}

# Sem fontes montadas o radar nao tem onde buscar. Melhor nao rodar do que
# produzir briefing vazio todo dia.
$fontes = Join-Path $projeto 'pesquisa\fontes.md'
if (-not (Test-Path $fontes)) {
    Registrar "ERRO: pesquisa/fontes.md nao existe. Rodar /radar na mao uma vez - a primeira rodada monta o mapa de fontes do nicho."
    exit 1
}

Set-Location $projeto

$ferramentas = 'WebSearch WebFetch Read Write Edit Glob Grep TodoWrite'

Registrar "Iniciando varredura (pode levar varios minutos)..."
$inicio = Get-Date

$saida = & $claude -p '/radar' `
    --output-format text `
    --permission-mode acceptEdits `
    --allowedTools $ferramentas `
    --strict-mcp-config `
    --effort high

$codigo = $LASTEXITCODE
$duracao = [int]((Get-Date) - $inicio).TotalMinutes

Add-Content -Path $log -Value $saida -Encoding utf8

$briefing = Join-Path $projeto "pesquisa\radar\$hoje.md"

# A entrega manda, nao o codigo de saida. Ja aconteceu de a rodada produzir o
# briefing inteiro e so entao bater no limite de uso da conta: saiu com codigo 1
# e o arquivo estava pronto na pasta. Entao: olhar o arquivo primeiro.

if (Test-Path $briefing) {
    $linhas = (Get-Content $briefing | Measure-Object -Line).Lines
    if ($codigo -ne 0) {
        Registrar "OK COM RESSALVA: briefing gerado em $duracao min ($linhas linhas), mas o claude saiu com codigo $codigo. Conferir o log - pode estar truncado."
        exit 0
    }
    Registrar "OK: briefing gerado em $duracao min ($linhas linhas) em $briefing"
    exit 0
}

if ($codigo -ne 0) {
    Registrar "FALHOU: codigo de saida $codigo apos $duracao min, sem briefing na pasta"
    exit $codigo
}

Registrar "ATENCAO: a rodada terminou em $duracao min sem erro, mas o briefing do dia nao foi criado. Ver o log acima."
exit 2
