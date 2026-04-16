"""
Interface Web Unificada - Scrapper Tools
Combina 3 ferramentas em uma interface com abas:
1. Extrator de Imagens com OCR
2. Web Scraper (Scrapling)
3. Analisador Científico de Websites
"""

import streamlit as st
import sys
from pathlib import Path

# Configuração da página (DEVE ser a primeira chamada Streamlit)
st.set_page_config(
    page_title="Scrapper Tools - Suite Completa",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar paths para importações
project_root = Path(__file__).parent.parent

# Adicionar diretórios ao path
sys.path.insert(0, str(project_root / "src" / "image_extractor"))
sys.path.insert(0, str(project_root / "src" / "web_scraper"))
sys.path.insert(0, str(project_root / "src" / "website_analyzer"))
sys.path.insert(0, str(project_root / "Scrapling"))

# Importar módulos das aplicações
import sqlite3
import pandas as pd
import json
import os
from PIL import Image

# Importar funcionalidades específicas
try:
    import tesseract_config
    from image_extractor import ImageExtractor
    HAS_IMAGE_EXTRACTOR = True
except ImportError as e:
    HAS_IMAGE_EXTRACTOR = False
    IMAGE_EXTRACTOR_ERROR = str(e)

try:
    from scrapling.fetchers import Fetcher, StealthyFetcher
    HAS_SCRAPLING = True
except ImportError as e:
    HAS_SCRAPLING = False
    SCRAPLING_ERROR = str(e)

try:
    from website_analyzer import WebsiteAnalyzer
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_ANALYZER = True
except ImportError as e:
    HAS_ANALYZER = False
    ANALYZER_ERROR = str(e)

# ============================================================================
# TÍTULO PRINCIPAL E SIDEBAR
# ============================================================================

st.title("🛠️ Scrapper Tools - Suite Completa")
st.markdown("**Extração de Imagens • Web Scraping • Análise de Websites**")
st.markdown("---")

# Sidebar com informações gerais
with st.sidebar:
    st.header("ℹ️ Sobre")
    st.markdown("""
    **Scrapper Tools** combina 3 ferramentas poderosas:
    
    🖼️ **Extrator de Imagens**
    - Extração automática de imagens
    - OCR (Tesseract)
    - Banco de dados SQLite
    
    🕷️ **Web Scraper**
    - Powered by Scrapling
    - Seletores CSS
    - Modo Stealth
    
    🔬 **Analisador de Websites**
    - Análise técnica completa
    - SEO, Performance, Segurança
    - Tecnologias detectadas
    """)
    
    st.markdown("---")
    st.markdown("**Status das Ferramentas:**")
    st.write(f"🖼️ Extrator: {'✅' if HAS_IMAGE_EXTRACTOR else '❌'}")
    st.write(f"🕷️ Scrapling: {'✅' if HAS_SCRAPLING else '❌'}")
    st.write(f"🔬 Analisador: {'✅' if HAS_ANALYZER else '❌'}")

# ============================================================================
# TABS PRINCIPAIS
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "🖼️ Extrator de Imagens",
    "🕷️ Web Scraper",
    "🔬 Analisador de Websites"
])

# ============================================================================
# TAB 1: EXTRATOR DE IMAGENS
# ============================================================================

with tab1:
    if not HAS_IMAGE_EXTRACTOR:
        st.error(f"❌ Módulo Extrator de Imagens não disponível: {IMAGE_EXTRACTOR_ERROR}")
        st.info("Instale as dependências: `pip install pytesseract pillow`")
    else:
        # Inicializa o extrator
        @st.cache_resource
        def get_extractor():
            return ImageExtractor()
        
        extractor = get_extractor()
        
        # Sidebar específica do extrator
        with st.sidebar:
            st.markdown("---")
            st.header("📊 Estatísticas - Imagens")
            stats = extractor.get_statistics()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Imagens", stats['total_images'])
                st.metric("Com OCR", stats['total_ocr'])
            with col2:
                st.metric("Sessões", stats['total_sessions'])
                st.metric("Tamanho", f"{stats['total_size_mb']} MB")
        
        # Conteúdo principal
        st.header("🖼️ Extrator de Imagens com OCR")
        
        # Sub-tabs
        subtab1, subtab2, subtab3 = st.tabs(["🔍 Extrair", "📂 Banco de Dados", "📊 Análises"])
        
        # SUBTAB 1: Extrair Imagens
        with subtab1:
            st.subheader("Extrair Imagens de URL")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                url_img = st.text_input(
                    "URL do Site",
                    placeholder="https://example.com",
                    help="URL completa do site para extrair imagens",
                    key="url_img_extract"
                )
            
            with col2:
                do_ocr = st.checkbox("Fazer OCR", value=True, help="Extrair texto das imagens")
            
            col1, col2 = st.columns(2)
            
            with col1:
                download = st.checkbox("Baixar Imagens", value=True)
            
            with col2:
                lang = st.selectbox(
                    "Idioma OCR",
                    ["por", "eng", "spa"],
                    help="Idioma para reconhecimento de texto"
                )
            
            if st.button("🚀 Extrair Imagens", type="primary", use_container_width=True, key="extract_btn"):
                if not url_img:
                    st.error("❌ Por favor, digite uma URL")
                else:
                    with st.spinner("🔄 Extraindo imagens..."):
                        try:
                            stats_result = extractor.extract_images_from_url(
                                url_img,
                                download=download,
                                ocr=do_ocr,
                                lang=lang
                            )
                            
                            st.success("✅ Extração concluída!")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Encontradas", stats_result['total_found'])
                            col2.metric("Baixadas", stats_result['downloaded'])
                            col3.metric("OCR Processados", stats_result['ocr_processed'])
                            
                            if stats_result['errors'] > 0:
                                st.warning(f"⚠️ {stats_result['errors']} erro(s) durante a extração")
                            
                            # Mostra as imagens extraídas
                            if stats_result.get('images'):
                                st.subheader("🖼️ Imagens Extraídas")
                                
                                # Grid de imagens
                                cols = st.columns(4)
                                for idx, img_data in enumerate(stats_result['images'][:20]):
                                    with cols[idx % 4]:
                                        if os.path.exists(img_data['filepath']):
                                            img = Image.open(img_data['filepath'])
                                            st.image(img, use_container_width=True)
                                            st.caption(f"{img_data['width']}x{img_data['height']}")
                                            if 'ocr_text' in img_data and img_data['ocr_text']:
                                                with st.expander("📝 Texto OCR"):
                                                    st.text(img_data['ocr_text'])
                            
                            st.cache_resource.clear()
                            
                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")
        
        # SUBTAB 2: Banco de Dados
        with subtab2:
            st.subheader("🔍 Buscar Imagens no Banco")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_term = st.text_input(
                    "Buscar no texto OCR",
                    placeholder="Digite palavras-chave...",
                    key="search_ocr"
                )
            
            with col2:
                min_width = st.number_input("Largura mínima (px)", min_value=0, value=0)
            
            with col3:
                min_height = st.number_input("Altura mínima (px)", min_value=0, value=0)
            
            if st.button("🔍 Buscar", key="search_db_btn"):
                results = extractor.search_images(
                    search_term=search_term if search_term else None,
                    min_width=min_width if min_width > 0 else None,
                    min_height=min_height if min_height > 0 else None
                )
                
                if results:
                    st.success(f"✅ Encontradas {len(results)} imagem(ns)")
                    
                    for img in results[:20]:
                        with st.expander(f"📷 {img.get('domain', 'N/A')} - {img.get('width', 0)}x{img.get('height', 0)}px"):
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                filepath = img.get('filepath', '')
                                if filepath and os.path.exists(filepath):
                                    try:
                                        image = Image.open(filepath)
                                        st.image(image, use_container_width=True)
                                    except:
                                        st.warning("⚠️ Não foi possível carregar a imagem")
                            
                            with col2:
                                st.write(f"**🌐 Website:** {img.get('domain', 'N/A')}")
                                st.write(f"**Dimensões:** {img.get('width', 0)}x{img.get('height', 0)}px")
                                st.write(f"**Formato:** {img.get('format', 'N/A')}")
                                st.write(f"**Tamanho:** {img.get('size_bytes', 0):,} bytes")
                                
                                ocr_text = img.get('text_content')
                                if ocr_text:
                                    st.text_area("📝 Texto OCR", ocr_text, height=100, key=f"ocr_{img.get('id')}")
                else:
                    st.info("ℹ️ Nenhuma imagem encontrada")
        
        # SUBTAB 3: Análises
        with subtab3:
            st.subheader("📊 Estatísticas e Gráficos")
            
            conn = sqlite3.connect(extractor.db_path)
            
            # Análise por formato
            st.subheader("📸 Imagens por Formato")
            df_format = pd.read_sql_query('''
                SELECT format, COUNT(*) as count
                FROM images
                GROUP BY format
                ORDER BY count DESC
            ''', conn)
            
            if not df_format.empty:
                st.bar_chart(df_format.set_index('format'))
            else:
                st.info("Nenhuma imagem no banco ainda")
            
            conn.close()

# ============================================================================
# TAB 2: WEB SCRAPER
# ============================================================================

with tab2:
    if not HAS_SCRAPLING:
        st.error(f"❌ Módulo Scrapling não disponível: {SCRAPLING_ERROR}")
        st.info("Instale Scrapling: `pip install scrapling`")
    else:
        st.header("🕷️ Web Scraper - Scrapling")
        
        # Sidebar específica
        with st.sidebar:
            st.markdown("---")
            st.header("📖 Ajuda - Scrapling")
            st.markdown("""
            **Seletores CSS:**
            - `.classe` - Por classe
            - `#id` - Por ID
            - `tag` - Por etiqueta
            - `a::attr(href)` - Atributo
            - `::text` - Só texto
            """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🌐 Configuração")
            url_scrape = st.text_input(
                "URL",
                placeholder="https://example.com",
                help="URL completa do site",
                key="url_scrape"
            )
            
            css_selector = st.text_input(
                "Selector CSS",
                placeholder=".quote",
                help="Selector CSS para extrair elementos"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                fetcher_type = st.selectbox(
                    "Tipo de Fetcher",
                    ["HTTP (Rápido)", "Stealth (Anti-bot)"]
                )
            
            with col_b:
                extract_type = st.selectbox(
                    "Extrair",
                    ["Todos os elementos", "Primeiro elemento", "Texto apenas", "HTML completo"]
                )
            
            scrape_button = st.button("🚀 Extrair Dados", type="primary", use_container_width=True, key="scrape_btn")
        
        with col2:
            st.subheader("📊 Resultado")
            
            if scrape_button:
                if not url_scrape:
                    st.error("❌ Por favor ingresse uma URL")
                else:
                    with st.spinner("🔄 Extraindo dados..."):
                        try:
                            # Selecionar fetcher
                            if fetcher_type == "HTTP (Rápido)":
                                page = Fetcher.get(url_scrape)
                            else:
                                page = Fetcher.get(url_scrape)
                            
                            st.success(f"✅ Página carregada: {page.status}")
                            
                            if css_selector:
                                elements = page.css(css_selector)
                                
                                if extract_type == "Todos os elementos":
                                    data = elements.getall()
                                elif extract_type == "Primeiro elemento":
                                    data = [elements.get()] if elements else []
                                elif extract_type == "Texto apenas":
                                    data = [elem.text for elem in elements]
                                else:
                                    data = [str(page.html)]
                                
                                if data:
                                    st.write(f"**Encontrados: {len(data)} elemento(s)**")
                                    
                                    for idx, item in enumerate(data[:20], 1):
                                        with st.expander(f"Elemento {idx}"):
                                            st.code(str(item)[:1000], language="html")
                                    
                                    # Download
                                    st.download_button(
                                        "💾 Baixar JSON",
                                        data=json.dumps(data, indent=2, ensure_ascii=False),
                                        file_name="scraped_data.json",
                                        mime="application/json",
                                        key="download_json"
                                    )
                                else:
                                    st.warning("⚠️ Nenhum elemento encontrado")
                            else:
                                st.info("Digite um selector CSS")
                        
                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")

# ============================================================================
# TAB 3: ANALISADOR DE WEBSITES
# ============================================================================

with tab3:
    if not HAS_ANALYZER:
        st.error(f"❌ Módulo Analisador não disponível: {ANALYZER_ERROR}")
        st.info("Verifique as dependências do analisador")
    else:
        # Inicializa o analisador
        @st.cache_resource
        def get_analyzer():
            return WebsiteAnalyzer()
        
        analyzer = get_analyzer()
        
        st.header("🔬 Analisador Científico de Websites")
        
        # Sidebar específica
        with st.sidebar:
            st.markdown("---")
            st.header("📊 Estatísticas - Análises")
            
            conn = sqlite3.connect(analyzer.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM website_analyses')
            total_analyses = cursor.fetchone()[0]
            conn.close()
            
            st.metric("Total de Análises", total_analyses)
        
        url_analyze = st.text_input(
            "🌐 URL do website",
            placeholder="https://example.com",
            help="Digite a URL completa do website que deseja analisar",
            key="url_analyze"
        )
        
        if st.button("🚀 Analisar Website", type="primary", use_container_width=True, key="analyze_btn"):
            if not url_analyze:
                st.error("❌ Por favor, digite uma URL")
            else:
                with st.spinner("🔬 Analisando website..."):
                    try:
                        analysis = analyzer.analyze_website(url_analyze)
                        
                        if analysis:
                            st.success("✅ Análise concluída!")
                            
                            # Métricas principais
                            st.subheader("📊 Scores Gerais")
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                seo_score = analysis['seo']['seo_score']
                                st.metric("SEO", f"{seo_score}/100")
                            
                            with col2:
                                perf_score = analysis['performance']['optimization_score']
                                st.metric("Performance", f"{perf_score}/100")
                            
                            with col3:
                                sec_score = analysis['security']['security_score']
                                st.metric("Segurança", f"{sec_score}/100")
                            
                            with col4:
                                acc_score = analysis['html_analysis']['accessibility_score']
                                st.metric("Acessibilidade", f"{acc_score}/100")
                            
                            # Detalhes em colunas
                            col_left, col_right = st.columns(2)
                            
                            with col_left:
                                st.subheader("🔍 Tecnologias")
                                
                                cms = analysis['technologies'].get('cms')
                                if cms:
                                    st.success(f"**CMS:** {cms}")
                                
                                frameworks = analysis['technologies'].get('frameworks', [])
                                if frameworks:
                                    st.write("**Frameworks:**")
                                    for fw in frameworks:
                                        st.write(f"  • {fw}")
                                
                                st.markdown("---")
                                st.subheader("📄 HTML")
                                html = analysis['html_analysis']
                                st.write(f"**Elementos:** {html['total_elements']}")
                                st.write(f"**Imagens:** {html['images']}")
                                st.write(f"**Links:** {html['links']}")
                            
                            with col_right:
                                st.subheader("📊 SEO")
                                seo = analysis['seo']
                                
                                if seo['title']:
                                    st.write(f"**Title ({seo['title_length']} caracteres):**")
                                    st.info(seo['title'])
                                
                                if seo['meta_description']:
                                    st.write(f"**Meta Description ({seo['meta_description_length']} caracteres):**")
                                    st.info(seo['meta_description'])
                                
                                st.markdown("---")
                                st.subheader("🔒 Segurança")
                                sec = analysis['security']
                                
                                if sec['https_enabled']:
                                    st.success("✓ HTTPS habilitado")
                                else:
                                    st.error("✗ HTTPS não habilitado")
                        
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><b>🛠️ Scrapper Tools Suite</b> | Extração • Scraping • Análise</p>
    <p><small>Powered by Scrapling • Tesseract • Plotly • SQLite</small></p>
</div>
""", unsafe_allow_html=True)
