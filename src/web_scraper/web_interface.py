"""
Interface Web para Scrapling usando Streamlit
Executar com: streamlit run web_interface.py
"""

import streamlit as st
import sys
from pathlib import Path
import json

# Adiciona o diretório Scrapling ao path para importações
project_root = Path(__file__).parent.parent.parent
scrapling_path = project_root / "Scrapling"
if str(scrapling_path) not in sys.path:
    sys.path.insert(0, str(scrapling_path))

try:
    from scrapling.fetchers import Fetcher, StealthyFetcher
except ImportError:
    st.error("ERRO: Módulo Scrapling não encontrado. Por favor, instale: pip install scrapling")
    st.stop()

# Configuración de la página
st.set_page_config(
    page_title="Scrapling Web Interface",
    page_icon="🕷️",
    layout="wide"
)

# Título
st.title("🕷️ Scrapling - Web Scraping Interface")
st.markdown("---")

# Sidebar con opciones
with st.sidebar:
    st.header("⚙️ Configuración")
    
    fetcher_type = st.selectbox(
        "Tipo de Fetcher",
        ["HTTP (Rápido)", "Stealth (Anti-bot)"],
        help="HTTP para sitios normales, Stealth para sitios con protección"
    )
    
    st.markdown("---")
    st.header("📖 Ayuda")
    st.markdown("""
    **Selectores CSS comunes:**
    - `.clase` - Por clase
    - `#id` - Por ID
    - `tag` - Por etiqueta
    - `a::attr(href)` - Atributo href
    - `::text` - Solo texto
    
    **Ejemplos:**
    - `.product-title::text`
    - `a.link::attr(href)`
    - `.price`
    """)

# Formulario principal
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🌐 URL a Scrapear")
    url = st.text_input(
        "URL",
        placeholder="https://example.com",
        help="URL completa del sitio web"
    )
    
    css_selector = st.text_input(
        "Selector CSS",
        placeholder=".quote",
        help="Selector CSS para extraer elementos"
    )
    
    extract_type = st.radio(
        "Extraer",
        ["Todos los elementos", "Primer elemento", "Texto solamente", "HTML completo"],
        horizontal=True
    )
    
    scrape_button = st.button("🚀 Extraer Datos", type="primary", use_container_width=True)

with col2:
    st.header("📊 Resultado")
    result_container = st.container()

# Área de resultados debajo
st.markdown("---")

if scrape_button:
    if not url:
        st.error("❌ Por favor ingresa una URL")
    else:
        with st.spinner("🔄 Extrayendo datos..."):
            try:
                # Seleccionar fetcher
                if fetcher_type == "HTTP (Rápido)":
                    page = Fetcher.get(url)
                else:
                    st.info("ℹ️ Modo Stealth requiere navegadores instalados (scrapling install)")
                    page = Fetcher.get(url)  # Fallback a HTTP
                
                # Mostrar información de la página
                with result_container:
                    st.success(f"✅ Página cargada: {page.status}")
                    
                    # Tabs para diferentes vistas
                    tab1, tab2, tab3 = st.tabs(["📦 Datos Extraídos", "🔍 Vista Previa", "📝 Información"])
                    
                    with tab1:
                        if css_selector:
                            elements = page.css(css_selector)
                            
                            if extract_type == "Todos los elementos":
                                data = elements.getall()
                            elif extract_type == "Primer elemento":
                                data = [elements.get()] if elements else []
                            elif extract_type == "Texto solamente":
                                data = [elem.text for elem in elements]
                            else:  # HTML completo
                                data = [str(page.html)]
                            
                            if data:
                                st.write(f"**Encontrados: {len(data)} elemento(s)**")
                                
                                # Mostrar datos
                                for idx, item in enumerate(data[:50], 1):  # Limitar a 50
                                    with st.expander(f"Elemento {idx}"):
                                        st.code(str(item)[:1000], language="html")
                                
                                # Botones de descarga
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.download_button(
                                        "💾 Descargar como JSON",
                                        data=json.dumps(data, indent=2, ensure_ascii=False),
                                        file_name="scraped_data.json",
                                        mime="application/json"
                                    )
                                with col_b:
                                    st.download_button(
                                        "💾 Descargar como TXT",
                                        data="\n".join(str(item) for item in data),
                                        file_name="scraped_data.txt",
                                        mime="text/plain"
                                    )
                            else:
                                st.warning("⚠️ No se encontraron elementos con ese selector")
                        else:
                            st.info("ℹ️ Ingresa un selector CSS para extraer datos específicos")
                    
                    with tab2:
                        st.subheader("Título de la página")
                        title = page.css('title::text').get()
                        st.write(title or "Sin título")
                        
                        st.subheader("Primeros 500 caracteres")
                        preview_text = page.text[:500]
                        st.text_area("Preview", preview_text, height=200)
                    
                    with tab3:
                        st.metric("Status Code", page.status)
                        st.metric("URL Final", url)
                        if css_selector:
                            elements_count = len(page.css(css_selector))
                            st.metric("Elementos encontrados", elements_count)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

# Ejemplos
with st.expander("💡 Ejemplos de uso"):
    st.markdown("""
    ### Ejemplo 1: Extraer citas
    - **URL**: `https://quotes.toscrape.com`
    - **Selector**: `.quote .text::text`
    - **Tipo**: Todos los elementos
    
    ### Ejemplo 2: Extraer títulos
    - **URL**: `https://news.ycombinator.com`
    - **Selector**: `.titleline > a::text`
    - **Tipo**: Todos los elementos
    
    ### Ejemplo 3: Extraer enlaces
    - **URL**: `https://example.com`
    - **Selector**: `a::attr(href)`
    - **Tipo**: Todos los elementos
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Powered by <a href='https://github.com/D4Vinci/Scrapling'>Scrapling</a> 🕷️</p>
    </div>
    """,
    unsafe_allow_html=True
)
