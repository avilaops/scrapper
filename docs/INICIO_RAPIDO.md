# 🚀 Inicio Rápido - Scrapling

## ¿Qué es esto?

Este proyecto contiene **Scrapling**, una librería moderna de web scraping con:
- ✅ **Interfaz Web Visual** (¡la forma más fácil de empezar!)
- ✅ Shell interactivo
- ✅ Scripts Python
- ✅ CLI (línea de comandos)

---

## 🎯 Opción 1: Interfaz Web (MÁS FÁCIL) ⭐

### Iniciar la interfaz:
```bash
.\start_web.bat
```

**Se abrirá en tu navegador:** http://localhost:8501

### ¿Qué puedo hacer?
1. Ingresa una URL (ej: https://quotes.toscrape.com)
2. Ingresa un selector CSS (ej: `.quote .text::text`)
3. Click en "Extraer Datos"
4. ¡Listo! Descarga los resultados

**📖 Ver guía completa:** [GUIA_INTERFAZ_WEB.md](GUIA_INTERFAZ_WEB.md)

---

## 🎯 Opción 2: Scripts Python

### Prueba rápida:
```bash
python test_scrapling.py
```

### Ejemplos completos:
```bash
python example_scraper.py
```

### Crear tu propio script:
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
print(quotes)
```

---

## 🎯 Opción 3: Shell Interactivo

```bash
.\scrapling.bat shell
```

Útil para experimentar y probar selectores en tiempo real.

---

## 🎯 Opción 4: CLI (Línea de Comandos)

Extrae datos directamente sin programar:

```bash
.\scrapling.bat extract get "https://quotes.toscrape.com" quotes.html
```

---

## 📚 Recursos

- **Guía de la Interfaz Web**: [GUIA_INTERFAZ_WEB.md](GUIA_INTERFAZ_WEB.md)
- **README completo**: [README.md](README.md)
- **Documentación oficial**: https://scrapling.readthedocs.io
- **Código fuente**: [Scrapling/](Scrapling/)

---

## 🆘 ¿Necesitas ayuda?

1. **La interfaz web no se abre**
   - Revisa que se ejecutó sin errores
   - Abre http://localhost:8501 manualmente

2. **Comando 'scrapling' no reconocido**
   - Usa `.\scrapling.bat` en su lugar

3. **Errores de instalación**
   - Ejecuta: `pip install --user -r requirements.txt`

---

## 🎓 Ejemplos Rápidos

### Con la Interfaz Web:
1. Abre: `.\start_web.bat`
2. URL: `https://quotes.toscrape.com`
3. Selector: `.quote .text::text`
4. Click "Extraer Datos"

### Con Python:
```python
from scrapling.fetchers import Fetcher

# Extraer citas
page = Fetcher.get('https://quotes.toscrape.com/')
for quote in page.css('.quote'):
    text = quote.css('.text::text').get()
    author = quote.css('.author::text').get()
    print(f"{author}: {text}")
```

---

¡Empieza con la **Interfaz Web** si eres principiante! 🌐✨
