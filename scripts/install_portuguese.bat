@echo off
REM Script para instalar idioma Português no Tesseract
REM Execute como Administrador (clique direito -> Executar como administrador)

echo ========================================
echo  INSTALACAO DO IDIOMA PORTUGUES
echo  Tesseract OCR
echo ========================================
echo.

REM Verifica se está rodando como administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Executando como Administrador
) else (
    echo ❌ ERRO: Este script precisa ser executado como Administrador
    echo.
    echo    Clique direito no arquivo e selecione "Executar como administrador"
    pause
    exit /b 1
)

echo.
echo Copiando arquivo por.traineddata...
echo.

REM Copia o arquivo do temp para o Tesseract
copy /Y "%TEMP%\por.traineddata" "C:\Program Files\Tesseract-OCR\tessdata\por.traineddata"

if %errorLevel% == 0 (
    echo.
    echo ✅ Idioma Português instalado com sucesso!
    echo.
    echo    Local: C:\Program Files\Tesseract-OCR\tessdata\por.traineddata
    echo.
) else (
    echo.
    echo ❌ Erro ao copiar arquivo
    echo.
    echo    Tente copiar manualmente:
    echo    De: %TEMP%\por.traineddata
    echo    Para: C:\Program Files\Tesseract-OCR\tessdata\
    echo.
)

echo.
echo Testando instalação...
python test_ocr.py

echo.
pause
