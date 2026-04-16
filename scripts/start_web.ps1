# Script para iniciar a Interface Web do Scrapling
# Obtém o diretório raiz do projeto (pasta pai de scripts/)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath

# Navega para o diretório raiz do projeto
Set-Location $projectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SCRAPLING - WEB SCRAPING" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Python está instalado
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Python: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Verifica se Streamlit está instalado
$streamlitInstalled = python -m pip show streamlit 2>$null
if (-not $streamlitInstalled) {
    Write-Host "AVISO: Streamlit não encontrado!" -ForegroundColor Yellow
    Write-Host "Instalando dependências..." -ForegroundColor Cyan
    python -m pip install -r requirements.txt
    Write-Host ""
}

Write-Host "Diretório do projeto: $projectRoot" -ForegroundColor Gray
Write-Host "Iniciando interface web do Scrapling..." -ForegroundColor Yellow
Write-Host ""
Write-Host "A interface se abrirá em: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para parar, pressione Ctrl+C" -ForegroundColor Yellow
Write-Host ""

python -m streamlit run src/web_scraper/web_interface.py
