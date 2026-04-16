@echo off
REM Script para iniciar o Extrator de Imagens com OCR
REM Obtém o diretório raiz do projeto (pasta pai de scripts\)
cd /d "%~dp0.."

echo.
echo ========================================
echo    EXTRATOR DE IMAGENS COM OCR + SQL
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Por favor, instale o Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verifica se Streamlit está instalado
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo AVISO: Streamlit não encontrado!
    echo Instalando dependências...
    python -m pip install -r requirements.txt
    echo.
)

echo Diretório do projeto: %CD%
echo Iniciando interface web...
echo.
echo A interface se abrirá em: http://localhost:8502
echo.
echo Para parar, pressione Ctrl+C
echo.

python -m streamlit run src\image_extractor\image_extractor_web.py --server.port 8502
pause
