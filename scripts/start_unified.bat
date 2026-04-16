@echo off
REM Script para iniciar a Interface Unificada - Scrapper Tools
REM Obtém o diretório raiz do projeto (pasta pai de scripts\)
cd /d "%~dp0.."

echo.
echo ========================================
echo    SCRAPPER TOOLS - SUITE COMPLETA
echo ========================================
echo.
echo   [imagen]  Extrator de Imagens com OCR
echo   [spider]  Web Scraper (Scrapling)
echo   [micro]  Analisador de Websites
echo.
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verifica se Streamlit está instalado
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo AVISO: Streamlit nao encontrado!
    echo Instalando dependencias...
    python -m pip install -r requirements.txt
    echo.
)

echo Diretorio do projeto: %CD%
echo Iniciando interface unificada...
echo.
echo A interface se abrira em: http://localhost:8500
echo.
echo [OK] Todas as 3 ferramentas estarao disponiveis em ABAS!
echo.
echo Para parar, pressione Ctrl+C
echo.

python -m streamlit run src\unified_app.py --server.port 8500
pause
