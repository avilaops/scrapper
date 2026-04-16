# Web Scraping Project with Scrapling

Este workspace contiene el repositorio completo de Scrapling y ejemplos de uso.

## Estructura del Proyecto

```
Scrapper/
├── Scrapling/                   # Repositório completo de Scrapling
│   ├── scrapling/               # Código fuente de la librería
│   ├── tests/                   # Tests del proyecto
│   └── docs/                    # Documentación
│
├── 🖼️ EXTRATOR DE IMAGENS COM OCR
├── image_extractor.py           # Script principal (CLI)
├── image_extractor_web.py       # Interface web do extrator
├── start_image_extractor.bat    # 🚀 Iniciar extrator (CMD)
├── start_image_extractor.ps1    # 🚀 Iniciar extrator (PowerShell)
├── test_ocr.py                  # Testar instalação do Tesseract
├── INSTALACAO_OCR.md            # 📖 Guia de instalação do OCR
├── extracted_images/            # 📁 Imagens extraídas (criado automaticamente)
├── images_database.db           # 💾 Banco de dados SQLite (criado automaticamente)
│
├── 🌐 WEB SCRAPING INTERFACE
├── web_interface.py             # Interface web (Streamlit)
├── start_web.bat                # 🚀 Iniciar interface (CMD)
├── start_web.ps1                # 🚀 Iniciar interface (PowerShell)
├── GUIA_INTERFAZ_WEB.md         # 📖 Guia completo de uso
│
├── 📝 EXEMPLOS E TESTES
├── example_scraper.py           # Exemplos de uso de Scrapling
├── test_scrapling.py            # Script de prueba rápida
├── INICIO_RAPIDO.md             # Guia de início rápido
│
├── 🔧 CONFIGURAÇÃO
├── requirements.txt             # Dependências do projeto
├── scrapling.bat                # Script helper (CMD)
├── scrapling.ps1                # Script helper (PowerShell)
└── README.md                    # Esta guia
```

## Instalación

### 1. Instalar Scrapling con todas las características

```bash
# Si tienes problemas de permisos, usa --user
pip install --user -r requirements.txt
```

> **⚠️ Nota importante**: Si instalas con `--user`, los ejecutables se instalan en:
> `C:\Users\Administrador\AppData\Roaming\Python\Python310\Scripts`
> 
> Agrega esta ruta a tu PATH para usar los comandos directamente.

### 2. Instalar dependencias de navegadores (requerido para StealthyFetcher y DynamicFetcher)

```bash
# Opción 1: Usando la ruta completa
C:\Users\Administrador\AppData\Roaming\Python\Python310\Scripts\scrapling.exe install

# Opción 2: Agregar al PATH (recomendado)
# Agrega esta ruta a tus variables de entorno PATH:
# C:\Users\Administrador\AppData\Roaming\Python\Python310\Scripts
# Luego podrás usar simplemente:
scrapling install
```

## Uso Rápido

### 🖼️ **NOVO: Extrator de Imagens com OCR + SQL**

Extrai imagens PNG/JPG de sites, aplica OCR (Tesseract) e organiza em banco de dados SQLite!

```bash
# 1. Instalar Tesseract OCR (OBRIGATÓRIO)
# Ver guia completo: INSTALACAO_OCR.md
# Windows: Download de https://github.com/UB-Mannheim/tesseract/wiki

# 2. Testar instalação
python test_ocr.py

# 3. Iniciar interface web
.\start_image_extractor.bat
```

**Abre em:** http://localhost:8502

**Funcionalidades:**
- ✅ Extrai automaticamente imagens PNG/JPG
- ✅ OCR em português/inglês/espanhol
- ✅ Banco de dados SQLite
- ✅ Busca por texto OCR
- ✅ Exporta JSON/CSV
- ✅ Estatísticas e análises

📖 **Guia completo:** [INSTALACAO_OCR.md](INSTALACAO_OCR.md)

---

### 🌐 Interfaz Web de Scraping (Recomendado para principiantes)

**Forma más fácil:**
```bash
.\start_web.bat
# O en PowerShell:
.\start_web.ps1
```

**O directamente:**
```bash
python -m streamlit run web_interface.py
```

Esto abre una **interfaz visual** en tu navegador (`http://localhost:8501`) donde puedes:
- ✅ Ingresar URLs para scrapear
- ✅ Usar selectores CSS interactivamente  
- ✅ Ver resultados en tiempo real
- ✅ Descargar datos en JSON o TXT
- ✅ Vista previa de páginas
- ✅ Ejemplos integrados

**🎯 La interfaz está ACTIVA ahora en:** http://localhost:8501

### ⚡ Verificar que todo funciona

```bash
python test_scrapling.py
```

### 📝 Ejecutar el script de ejemplo

```bash
python example_scraper.py
```

### 💻 Usar scrapling desde línea de comandos

```bash
# Opción 1: Usando el script wrapper (más fácil)
.\scrapling.bat --help
.\scrapling.ps1 --help

# Opción 2: Usando la ruta completa
C:\Users\Administrador\AppData\Roaming\Python\Python310\Scripts\scrapling.exe --help
```

### Usar el shell interactivo de Scrapling

```bash
scrapling shell
```

### Extraer contenido directamente desde la terminal

```bash
# Extraer contenido a archivo Markdown
scrapling extract get 'https://example.com' content.md

# Con navegador headless
scrapling extract fetch 'https://example.com' content.html --css-selector '.main-content'

# Modo stealth con bypass de Cloudflare
scrapling extract stealthy-fetch 'https://nopecha.com/demo/cloudflare' captchas.html --solve-cloudflare
```

## Características Principales de Scrapling

- **🕷️ Framework de Spiders**: API similar a Scrapy con crawling concurrente
- **⚡ Múltiples Fetchers**: HTTP, navegador automatizado, bypass anti-bot
- **🔄 Scraping Adaptativo**: Relocaliza elementos cuando los sitios web cambian
- **💾 Pausar & Reanudar**: Crawls con checkpoint para reanudar después
- **🛡️ Bypass Anti-Bot**: Supera Cloudflare Turnstile automáticamente
- **🤖 Integración con IA**: Servidor MCP para scraping asistido por IA

## Ejemplos de Código

### Scraping HTTP Básico

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
```

### Modo Stealth

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare', solve_cloudflare=True)
data = page.css('#content').get()
```

### Spider Completo

```python
from scrapling.spiders import Spider, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    
    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
            }

result = QuotesSpider().start()
result.items.to_json("quotes.json")
```

## Recursos

- 📚 [Documentación oficial](https://scrapling.readthedocs.io)
- 🔗 [Repositorio GitHub](https://github.com/D4Vinci/Scrapling)
- 💬 [Discord](https://discord.gg/EMgGbDceNQ)
- 🐦 [Twitter](https://x.com/Scrapling_dev)

## Desarrollo

Para contribuir al proyecto Scrapling, consulta el directorio `Scrapling/` con el código fuente completo.

```bash
cd Scrapling
pip install -e ".[dev]"
pytest  # Ejecutar tests
```

## Resolución de Problemas

### El comando 'scrapling' no se reconoce

**Solución 1**: Usa los scripts wrapper incluidos:
```bash
.\scrapling.bat --help
.\scrapling.ps1 --help
```

**Solución 2**: Agrega al PATH la ruta:
```
C:\Users\Administrador\AppData\Roaming\Python\Python310\Scripts
```

### Error de permisos al instalar

Si obtienes errores de permisos, instala con:
```bash
pip install --user -r requirements.txt
```

### Los navegadores no funcionan

Asegúrate de haber ejecutado:
```bash
.\scrapling.bat install
```

## Licencia

Scrapling está bajo la licencia BSD-3-Clause. Ver [LICENSE](Scrapling/LICENSE) para más detalles.

---

Created: February 26, 2026
