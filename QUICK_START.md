# ⚡ Guia Rápido - Scrapling Project

## 🚀 Iniciar Sistemas

### ⭐ **RECOMENDADO: Interface Unificada (NOVO!)**

**Todas as 3 ferramentas em uma única interface com abas!**

```cmd
# CMD:
scripts\start_unified.bat

# PowerShell:
.\scripts\start_unified.ps1
```

- **URL:** http://localhost:8500
- **Contém:** 🖼️ Extrator de Imagens | 🕷️ Web Scraper | 🔬 Analisador
- **Vantagem:** Tudo em um só lugar!

---

### Ou execute cada ferramenta separadamente:

**CMD (arquivos .bat):**
```cmd
scripts\start_web.bat              - Web Scraping Interface (porta 8501)
scripts\start_image_extractor.bat  - Extrator de Imagens + OCR (porta 8502)
scripts\start_analyzer.bat         - Analisador de Websites (porta 8503)
```

**PowerShell (arquivos .ps1):**
```powershell
.\scripts\start_web.ps1              - Web Scraping Interface (porta 8501)
.\scripts\start_image_extractor.ps1  - Extrator de Imagens + OCR (porta 8502)
.\scripts\start_analyzer.ps1         - Analisador de Websites (porta 8503)
```

## 📋 O Que Cada Sistema Faz

### 1. Web Scraping Interface (porta 8501)
- Extrai dados de qualquer website
- Usa seletores CSS para capturar elementos
- Exporta em JSON ou TXT
- Interface visual para facilitar o scraping

### 2. Extrator de Imagens + OCR (porta 8502)
- Extrai imagens de websites (12 formatos: JPG, PNG, GIF, WebP, etc.)
- Aplica OCR (reconhecimento de texto) nas imagens
- Organiza imagens por domínio em pastas separadas
- Salva metadados em banco de dados SQLite
- Busca por texto encontrado nas imagens

### 3. Analisador de Websites (porta 8503)
- Analisa tecnologias usadas (frameworks, bibliotecas, etc.)
- Verifica performance e SEO
- Mapeia estrutura e arquitetura do site
- Gera relatórios completos com visualizações

## 📁 Onde Encontrar Arquivos

```
src/               - Todo o código Python dos 3 sistemas
scripts/           - Scripts para iniciar os sistemas
tests/             - Testes (execute para verificar se tudo funciona)
examples/          - Exemplos de como usar
docs/              - Documentação completa de cada sistema
data/              - Dados gerados (imagens, bancos de dados)
```

## 🧪 Testar Instalação

Execute estes comandos para verificar se tudo está funcionando:

```bash
# Testar OCR (Tesseract)
python tests/test_ocr.py

# Testar Scrapling
python tests/test_scrapling.py

# Testar extrator de imagens
python tests/test_image_formats.py
```

## 📖 Documentação Completa

Consulte a pasta `docs/` para guias detalhados:
- [README.md](README.md) - Documentação técnica completa
- [docs/INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md) - Tutorial passo a passo
- [docs/SISTEMAS_ATIVOS.md](docs/SISTEMAS_ATIVOS.md) - Detalhes dos sistemas
- [docs/GUIA_INTERFAZ_WEB.md](docs/GUIA_INTERFAZ_WEB.md) - Como usar o Web Scraper
- [docs/GUIA_EXTRATOR_IMAGENS.md](docs/GUIA_EXTRATOR_IMAGENS.md) - Como usar o Extrator

## 🆘 Problemas?

**Erro: "Tesseract not found"**
- Instale o Tesseract OCR
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Execute: `scripts\install_portuguese.bat` (para OCR em Português)

**Erro: "Module not found"**
```bash
pip install -r requirements.txt
```

**Scripts PowerShell não funcionam**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Ou use os scripts `.bat` no lugar.

---

💡 **Dica:** Você pode rodar os 3 sistemas ao mesmo tempo! Cada um usa uma porta diferente.
