# 🌐 Guía de la Interfaz Web de Scrapling

## Cómo Usar la Interfaz

### 1️⃣ Iniciar la Interfaz

```bash
.\start_web.bat
```

Se abrirá automáticamente en tu navegador en: **http://localhost:8501**

---

## 📋 Características de la Interfaz

### Panel Izquierdo - Configuración
- **Tipo de Fetcher**: Elige entre HTTP (rápido) o Stealth (anti-bot)
- **Ayuda integrada**: Selectores CSS comunes y ejemplos

### Panel Principal

#### 🌐 URL a Scrapear
- Ingresa la URL completa del sitio (ej: https://quotes.toscrape.com)

#### 🎯 Selector CSS
- Usa selectores CSS para extraer datos específicos
- Ejemplos:
  - `.quote` - Elementos con clase "quote"
  - `.text::text` - Solo el texto
  - `a::attr(href)` - Atributo href de enlaces

#### 📦 Tipo de Extracción
- **Todos los elementos**: Extrae todos los matches
- **Primer elemento**: Solo el primero
- **Texto solamente**: Solo el contenido de texto
- **HTML completo**: El HTML de la página

---

## 🎓 Ejemplos Prácticos

### Ejemplo 1: Extraer Citas de Quotes to Scrape

1. **URL**: `https://quotes.toscrape.com`
2. **Selector CSS**: `.quote .text::text`
3. **Tipo**: Todos los elementos
4. Click en **🚀 Extraer Datos**

**Resultado**: Lista de todas las citas de la página

---

### Ejemplo 2: Extraer Títulos de Hacker News

1. **URL**: `https://news.ycombinator.com`
2. **Selector CSS**: `.titleline > a::text`
3. **Tipo**: Todos los elementos
4. Click en **🚀 Extraer Datos**

**Resultado**: Todos los títulos de noticias

---

### Ejemplo 3: Extraer Enlaces

1. **URL**: `https://example.com`
2. **Selector CSS**: `a::attr(href)`
3. **Tipo**: Todos los elementos
4. Click en **🚀 Extraer Datos**

**Resultado**: Todos los enlaces de la página

---

## 📊 Pestañas de Resultados

### 📦 Datos Extraídos
- Muestra todos los elementos encontrados
- Cada elemento es expandible
- Botones para descargar como JSON o TXT

### 🔍 Vista Previa
- Título de la página
- Primeros 500 caracteres de contenido
- Útil para verificar que la página se cargó correctamente

### 📝 Información
- Status Code de la respuesta
- URL final (después de redirecciones)
- Cantidad de elementos encontrados

---

## 💡 Selectores CSS Útiles

| Selector | Descripción | Ejemplo |
|----------|-------------|---------|
| `.clase` | Por clase CSS | `.product` |
| `#id` | Por ID | `#main-content` |
| `tag` | Por etiqueta HTML | `h1`, `p`, `div` |
| `::text` | Solo texto | `.title::text` |
| `::attr(name)` | Atributo específico | `a::attr(href)` |
| `>` | Hijo directo | `.container > .item` |
| Espacio | Descendiente | `.list .item` |

---

## 💾 Exportar Datos

Después de extraer datos, puedes descargarlos en:

1. **JSON**: Formato estructurado, ideal para programación
   - Click en **💾 Descargar como JSON**

2. **TXT**: Formato de texto simple
   - Click en **💾 Descargar como TXT**

---

## 🛑 Detener la Interfaz

Para cerrar la aplicación web:
1. Ve a la terminal/consola donde se inició
2. Presiona **Ctrl + C**
3. Confirma si se solicita

---

## 🔧 Solución de Problemas

### La interfaz no se abre
- Verifica que el comando se ejecutó sin errores
- Abre manualmente: http://localhost:8501

### No encuentra elementos
- Verifica el selector CSS usando las herramientas de desarrollador del navegador (F12)
- Intenta con selectores más generales primero (ej: `div`, `.content`)

### Error al cargar la página
- Verifica que la URL es correcta y comienza con http:// o https://
- Algunos sitios bloquean scraping automático

---

## 📚 Recursos Adicionales

- [Documentación de Scrapling](https://scrapling.readthedocs.io)
- [Tutorial de Selectores CSS](https://www.w3schools.com/cssref/css_selectors.php)
- [GitHub de Scrapling](https://github.com/D4Vinci/Scrapling)

---

¡Disfruta haciendo web scraping con una interfaz visual! 🕷️✨
