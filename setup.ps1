Write-Host "🚀 Iniciando configuração do ambiente de desenvolvimento..." -ForegroundColor Green

# 1. Criação do ambiente virtual .venv (se não existir)
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Criando ambiente virtual (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "✔ Ambiente virtual (.venv) já existe." -ForegroundColor Cyan
}

# 2. Definição do caminho do Python e Pip do ambiente virtual
$venvPython = ".\.venv\Scripts\python.exe"

# 3. Atualização do Pip
Write-Host "🔄 Atualizando o pip..." -ForegroundColor Yellow
& $venvPython -m pip install --upgrade pip --quiet

# 4. Instalação das dependências
if (Test-Path "requirements.txt") {
    Write-Host "📥 Instalando dependências a partir do requirements.txt..." -ForegroundColor Yellow
    & $venvPython -m pip install -r requirements.txt
} else {
    Write-Host "📥 Instalando dependências padrão..." -ForegroundColor Yellow
    & $venvPython -m pip install ics playwright beautifulsoup4 requests canvasapi
}

# 5. Instalação dos navegadores do Playwright
Write-Host "🌐 Instalando navegadores para o Playwright (Chromium)..." -ForegroundColor Yellow
& $venvPython -m playwright install chromium

Write-Host "✅ Ambiente pronto para uso!" -ForegroundColor Green
Write-Host "Para ativar a venv no seu terminal, rode: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan