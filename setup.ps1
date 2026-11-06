Write-Host "Iniciando configuracao do ambiente de desenvolvimento..." -ForegroundColor Green

$venvPath = Join-Path -Path $PSScriptRoot -ChildPath ".venv"
$venvPython = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"

# Interrompe o setup com uma mensagem de erro clara
function Stop-Setup($mensagem) {
    Write-Host "FALHA: $mensagem" -ForegroundColor Red
    Write-Host "O ambiente NAO foi configurado por completo. Corrija o erro acima e rode o setup novamente." -ForegroundColor Red
    exit 1
}

# 1. Cria o ambiente virtual usando o caminho absoluto
if (-not (Test-Path $venvPath)) {
    Write-Host "Criando ambiente virtual (.venv)..." -ForegroundColor Yellow
    python -m venv $venvPath
} else {
    Write-Host "Ambiente virtual (.venv) ja existe." -ForegroundColor Cyan
}

# 2. Verifica se funcionou (tenta com 'py' se 'python' falhar)
if (-not (Test-Path $venvPython)) {
    Write-Host "O comando 'python' falhou. Tentando com 'py'..." -ForegroundColor Yellow
    py -m venv $venvPath

    if (-not (Test-Path $venvPython)) {
        Stop-Setup "Python nao esta instalado ou nao esta no PATH do Windows."
    }
}

# 3. Atualiza o Pip
Write-Host "Atualizando o pip..." -ForegroundColor Yellow
& $venvPython -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) { Stop-Setup "Nao foi possivel atualizar o pip." }

# 4. Instala dependencias
$requirementsPath = Join-Path -Path $PSScriptRoot -ChildPath "requirements.txt"
if (-not (Test-Path $requirementsPath)) { Stop-Setup "Arquivo requirements.txt nao encontrado em $PSScriptRoot." }

Write-Host "Instalando dependencias do requirements.txt..." -ForegroundColor Yellow
& $venvPython -m pip install -r $requirementsPath
if ($LASTEXITCODE -ne 0) { Stop-Setup "Erro ao instalar as dependencias do requirements.txt." }

# 5. Instala o Chromium do Playwright (tenta ate 3 vezes, a rede as vezes falha)
Write-Host "Instalando navegadores do Playwright (Chromium)..." -ForegroundColor Yellow
$env:PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT = "120000"
$instalado = $false
for ($tentativa = 1; $tentativa -le 3; $tentativa++) {
    & $venvPython -m playwright install chromium
    if ($LASTEXITCODE -eq 0) { $instalado = $true; break }
    Write-Host "Tentativa $tentativa de 3 falhou." -ForegroundColor Yellow
}
if (-not $instalado) {
    Stop-Setup "Nao foi possivel baixar o Chromium do Playwright. Verifique sua internet e rode o setup novamente."
}

Write-Host "Ambiente pronto para uso!" -ForegroundColor Green
Write-Host "Para ativar a venv no terminal, digite: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
