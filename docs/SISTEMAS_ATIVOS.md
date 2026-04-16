# 🎉 SISTEMAS ATIVOS - Guia Rápido

**Data de Ativação:** 27 de Fevereiro de 2026  
**Última Atualização:** 27 de Fevereiro de 2026

---

## 🚀 SISTEMAS EM EXECUÇÃO

### 1️⃣ Interface Web Scraping
**URL:** http://localhost:8501

**Funcionalidades:**
- ✅ Extrair dados de qualquer site
- ✅ Selectores CSS interativos
- ✅ Download JSON/TXT
- ✅ Vista previa de páginas
- ✅ Exemplos integrados

**Como usar:**
1. Abra http://localhost:8501 no navegador
2. Digite a URL do site
3. Digite o seletor CSS (ex: `.product`)
4. Click "Extrair Dados"

**Iniciar:**
```bash
.\start_web.bat
# ou
python web_interface.py
```

---

### 2️⃣ Interface Extrator de Imagens + OCR
**URL:** http://localhost:8502

**Funcionalidades:**
- ✅ Extrai 12 formatos de imagem (JPG, PNG, GIF, WebP, BMP, TIFF, ICO, SVG, HEIC, HEIF)
- ✅ OCR em Português, Inglês e Espanhol
- ✅ Organização automática por website em pastas separadas
- ✅ Banco de dados SQLite automático
- ✅ Busca por texto OCR
- ✅ Análises e estatísticas por domínio
- ✅ Export JSON/CSV

**Como usar:**
1. Abra http://localhost:8502 no navegador
2. Aba "🔍 Extrair Imagens"
3. Digite a URL
4. Marque "Fazer OCR"
5. Escolha idioma: "por" (português), "eng" (inglês) ou "spa" (espanhol)
6. Click "Extrair Imagens"
7. Veja as imagens organizadas em `extracted_images/<dominio>/`

**Iniciar:**
```bash
.\start_image_extractor.bat
# ou
python image_extractor_web.py
```

---

### 3️⃣ Analisador Científico de Websites ✨ **NOVO**
**URL:** http://localhost:8503

**Funcionalidades:**
- ✅ Detecção automática de tecnologias (frameworks, CMS, bibliotecas)
- ✅ Análise completa de HTML (semântica, acessibilidade)
- ✅ Análise de CSS e JavaScript
- ✅ Métricas de Performance (tamanho, recursos, otimizações)
- ✅ Análise de SEO (meta tags, Open Graph, Schema.org)
- ✅ Análise de Segurança (HTTPS, headers)
- ✅ Análise de Layout e Design (responsividade, grid systems)
- ✅ Scores científicos (0-100) para cada categoria
- ✅ Comparação entre websites
- ✅ Histórico de análises
- ✅ Export JSON completo

**O que é analisado:**
- 🔍 **Tecnologias:** React, Vue, Angular, WordPress, Shopify, etc.
- 📄 **HTML:** Estrutura semântica, acessibilidade, elementos
- 🎨 **CSS:** Frameworks (Bootstrap, Tailwind), preprocessadores
- ⚡ **JavaScript:** Bibliotecas, módulos, async/defer
- 📊 **Performance:** Tamanho da página, número de recursos, otimizações
- 🔍 **SEO:** Title, description, headings, structured data
- 🔒 **Segurança:** HTTPS, headers de segurança
- 🎨 **Layout:** Responsividade, viewport, grid systems

**Como usar:**
1. Abra http://localhost:8503 no navegador
2. Aba "🔬 Nova Análise"
3. Digite a URL do website
4. Click "Analisar Website"
5. Aguarde 10-30 segundos para análise completa
6. Veja scores, tecnologias detectadas, e recomendações
7. Exporte a análise em JSON

**Iniciar:**
```bash
.\start_analyzer.bat
# ou
python website_analyzer_web.py
```

---

## 📊 CONFIGURAÇÃO DO SISTEMA

### ✅ Instalações Concluídas:

| Componente | Status | Versão |
|------------|--------|--------|
| Python | ✅ Instalado | 3.10 |
| Scrapling | ✅ Instalado | v0.4 |
| Streamlit | ✅ Instalado | v1.31.0 |
| Tesseract OCR | ✅ Instalado | v5.5.0 |
| PyTesseract | ✅ Instalado | v0.3.13 |
| Pillow | ✅ Instalado | v10.4.0 |
| Pandas | ✅ Instalado | v2.2.0 |

### 🌐 Idiomas OCR Disponíveis:
- ✅ **Português** (por)
- ✅ **Inglês** (eng)
- ✅ **OSD** (Orientation and script detection)

---

## 📁 ESTRUTURA DE ARQUIVOS

```
D:\iCloudDrive\AvilaOps\Scrapper\
│
├── 🌐 WEB SCRAPING
│   ├── web_interface.py          → Interface web principal
│   ├── start_web.bat             → Iniciar (porta 8501)
│   └── GUIA_INTERFAZ_WEB.md      → Guia de uso
│
├── 🖼️ EXTRATOR DE IMAGENS + OCR
│   ├── image_extractor.py        → Script CLI
│   ├── image_extractor_web.py    → Interface web
│   ├── start_image_extractor.bat → Iniciar (porta 8502)
│   ├── test_ocr.py               → Teste do Tesseract
│   ├── INSTALACAO_OCR.md         → Guia de instalação
│   └── GUIA_EXTRATOR_IMAGENS.md  → Guia de uso
│
├── 📦 DADOS GERADOS
│   ├── extracted_images/         → Imagens baixadas
│   ├── images_database.db        → Banco SQLite
│   └── quotes.md                 → Exemplo extraído
│
├── 🔧 CONFIGURAÇÃO
│   ├── tesseract_config.py       → Config do Tesseract
│   ├── requirements.txt          → Dependências
│   └── tessdata/                 → Idiomas adicionais
│
└── 📚 DOCUMENTAÇÃO
    ├── README.md                 → Guia principal
    ├── INICIO_RAPIDO.md          → Início rápido
    └── INSTALAR_PORTUGUES.md     → Instalar idiomas
```

---

## 🎯 EXEMPLOS DE USO

### Exemplo 1: Extrair Notícias

**Interface Web Scraping (8501):**
```
URL: https://news.ycombinator.com
Seletor: .titleline > a::text
```

### Exemplo 2: Extrair Produtos com Imagens

**Interface Imagens (8502):**
```
URL: https://example-shop.com/products
OCR: Não (produtos geralmente não têm texto)
```

### Exemplo 3: Extrair Documentos com OCR

**Interface Imagens (8502):**
```
URL: https://site-com-documentos.com
OCR: Sim
Idioma: por (português)
```

---

## 🛑 PARAR OS SISTEMAS

Para parar as interfaces, feche as janelas do PowerShell que foram abertas ou pressione `Ctrl+C` em cada uma.

**Reiniciar:**
```bash
.\start_web.bat              # Web Scraping
.\start_image_extractor.bat  # Extrator de Imagens
```

---

## 📊 ACESSAR DADOS EXTRAÍDOS

### Imagens:
- **Pasta:** `D:\iCloudDrive\AvilaOps\Scrapper\extracted_images\`
- **Banco:** `images_database.db` (use DB Browser ou a interface web)

### Web Scraping:
- Downloads vão para a pasta padrão do navegador
- Ou use a interface para ver resultados

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### Interface não abre?
1. Verifique se as portas 8501 e 8502 estão livres
2. Abra manualmente no navegador
3. Verifique se o PowerShell não fechou

### OCR não funciona?
```bash
python test_ocr.py
```
Deve mostrar: ✅ Português e Inglês instalados

### Erro ao extrair imagens?
- Verifique se a URL é válida
- Alguns sites bloqueiam scraping automático
- Use modo Stealth se necessário

---

## 🎓 RECURSOS ADICIONAIS

- [Documentação Scrapling](https://scrapling.readthedocs.io/)
- [Tutorial Tesseract](https://tesseract-ocr.github.io/)
- [Seletores CSS](https://www.w3schools.com/cssref/css_selectors.php)

---

## 📞 STATUS ATUAL

✅ **TUDO INSTALADO E FUNCIONANDO!**

**Interfaces Ativas:**
- 🌐 Web Scraping: http://localhost:8501
- 🖼️ Extrator Imagens: http://localhost:8502

**Tesseract OCR:**
- ✅ Português (por)
- ✅ Inglês (eng)

**Banco de Dados:**
- ✅ SQLite configurado
- ✅ Pasta de imagens criada

---

🎊 **PRONTO PARA USO!** Abra os links acima no navegador e comece a extrair dados!
