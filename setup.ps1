Write-Host "Iniciando configuracao do ambiente de desenvolvimento..." -ForegroundColor Green

$venvPath = Join-Path -Path $PSScriptRoot -ChildPath ".venv"
$venvPython = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"

# 1. Cria o ambiente virtual usando o caminho absoluto
if (-not (Test-Path $venvPath)) {
    Write-Host "Criando ambiente virtual (.venv)..." -ForegroundColor Yellow
    python -m venv $venvPath
} else {
    Write-Host "Ambiente virtual (.venv) ja existe." -ForegroundColor Cyan
}

# 2. Verifica se funcionou (tenta com 'py' se 'python' falhar)
if (-not (Test-Path $venvPython)) {
    Write-Host "ERRO: O comando 'python' falhou. Tentando com 'py'..." -ForegroundColor Red
    py -m venv $venvPath
    
    if (-not (Test-Path $venvPython)) {
        Write-Host "FALHA: Python nao esta instalado ou nao esta no PATH do Windows." -ForegroundColor Red
        exit
    }
}

# 3. Atualiza o Pip
Write-Host "Atualizando o pip..." -ForegroundColor Yellow
& $venvPython -m pip install --upgrade pip --quiet

# 4. Instala dependencias
$requirementsPath = Join-Path -Path $PSScriptRoot -ChildPath "requirements.txt"
if (Test-Path $requirementsPath) {
    Write-Host "Instalando dependencias do requirements.txt..." -ForegroundColor Yellow
    & $venvPython -m pip install -r $requirementsPath
} else {
    Write-Host "Instalando dependencias padrao..." -ForegroundColor Yellow
    & $venvPython -m pip install ics playwright beautifulsoup4 requests canvasapi
}

# 5. Instala o Playwright
Write-Host "Instalando navegadores do Playwright (Chromium)..." -ForegroundColor Yellow
& $venvPython -m playwright install chromium

Write-Host "Ambiente pronto para uso!" -ForegroundColor Green
Write-Host "Para ativar a venv no terminal, digite: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan