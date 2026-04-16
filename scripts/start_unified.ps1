# Script para iniciar a Interface Unificada - Scrapper Tools
# Obtém o diretório raiz do projeto (pasta pai de scripts/)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath

# Navega para o diretório raiz do projeto
Set-Location $projectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SCRAPPER TOOLS - SUITE COMPLETA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🖼️  Extrator de Imagens com OCR" -ForegroundColor Yellow
Write-Host "  🕷️  Web Scraper (Scrapling)" -ForegroundColor Yellow
Write-Host "  🔬 Analisador de Websites" -ForegroundColor Yellow
Write-Host ""
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
Write-Host "Iniciando interface unificada..." -ForegroundColor Yellow
Write-Host ""
Write-Host "A interface se abrirá em: http://localhost:8500" -ForegroundColor Cyan
Write-Host ""
Write-Host "📌 Todas as 3 ferramentas estarão disponíveis em ABAS!" -ForegroundColor Green
Write-Host ""
Write-Host "Para parar, pressione Ctrl+C" -ForegroundColor Yellow
Write-Host ""

python -m streamlit run src/unified_app.py --server.port 8500
