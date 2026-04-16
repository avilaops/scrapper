"""
Interface Web para Extrator de Imagens com OCR
Streamlit app para extrair imagens, fazer OCR e gerenciar banco de dados
"""

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import sys
import os

# Adiciona o diretório src/image_extractor ao path para importações
module_path = Path(__file__).parent
if str(module_path) not in sys.path:
    sys.path.insert(0, str(module_path))

import tesseract_config  # Configura o caminho do Tesseract
from image_extractor import ImageExtractor
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Extrator de Imagens + OCR",
    page_icon="🖼️",
    layout="wide"
)

# Inicializa o extrator
@st.cache_resource
def get_extractor():
    return ImageExtractor()

extractor = get_extractor()

# Título
st.title("🖼️ Extrator de Imagens com OCR e SQL")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Estatísticas do Banco")
    stats = extractor.get_statistics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Imagens", stats['total_images'])
        st.metric("Com OCR", stats['total_ocr'])
    with col2:
        st.metric("Sessões", stats['total_sessions'])
        st.metric("Tamanho", f"{stats['total_size_mb']} MB")
    
    st.markdown("---")
    
    # Estatísticas por domínio
    st.header("🌐 Websites")
    domains = extractor.get_domains_stats()
    
    if domains:
        for domain_info in domains[:10]:  # Top 10 domínios
            domain = domain_info['domain']
            count = domain_info['count']
            size_mb = domain_info['size_bytes'] / (1024 * 1024)
            st.metric(
                f"📁 {domain}" if len(domain) <= 20 else f"📁 {domain[:17]}...",
                f"{count} imgs",
                f"{size_mb:.1f} MB"
            )
    else:
        st.info("Nenhum website ainda")
    
    st.markdown("---")
    
    if st.button("🔄 Atualizar Estatísticas"):
        st.cache_resource.clear()
        st.rerun()
    
    if st.button("💾 Exportar para JSON"):
        output_file = extractor.export_to_json()
        st.success(f"Exportado: {output_file}")
    
    st.markdown("---")
    st.header("ℹ️ Informações")
    st.info("""
    **Formatos suportados:**
    - JPG/JPEG
    - PNG
    - GIF
    - WebP
    - BMP
    - TIFF
    - ICO
    - SVG
    - HEIC/HEIF
    
    **Organização:**
    - Imagens salvas em `extracted_images/<dominio>/`
    - Cada website em sua própria pasta
    - Nomes de arquivo baseados em hash MD5 (evita duplicatas)
    
    **OCR:**
    - Requer Tesseract instalado
    - Idiomas: por, eng, spa
    """)

# Tabs principais
tab1, tab2, tab3 = st.tabs(["🔍 Extrair Imagens", "📂 Banco de Dados", "📊 Análises"])

# TAB 1: Extrair Imagens
with tab1:
    st.header("Extrair Imagens de URL")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url = st.text_input(
            "URL do Site",
            placeholder="https://example.com",
            help="URL completa do site para extrair imagens"
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
    
    if st.button("🚀 Extrair Imagens", type="primary", use_container_width=True):
        if not url:
            st.error("❌ Por favor, digite uma URL")
        else:
            with st.spinner("🔄 Extraindo imagens..."):
                try:
                    stats_result = extractor.extract_images_from_url(
                        url,
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
                    if stats_result['images']:
                        st.subheader("🖼️ Imagens Extraídas")
                        
                        # Grid de imagens
                        cols = st.columns(4)
                        for idx, img_data in enumerate(stats_result['images'][:20]):  # Limita a 20
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
                    st.exception(e)

# TAB 2: Banco de Dados
with tab2:
    st.header("Banco de Dados de Imagens")
    
    # Busca
    st.subheader("🔍 Buscar Imagens")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input(
            "Buscar no texto OCR",
            placeholder="Digite palavras-chave..."
        )
    
    with col2:
        min_width = st.number_input("Largura mínima (px)", min_value=0, value=0)
    
    with col3:
        min_height = st.number_input("Altura mínima (px)", min_value=0, value=0)
    
    if st.button("🔍 Buscar"):
        results = extractor.search_images(
            search_term=search_term if search_term else None,
            min_width=min_width if min_width > 0 else None,
            min_height=min_height if min_height > 0 else None
        )
        
        if results:
            st.success(f"✅ Encontradas {len(results)} imagem(ns)")
            
            # Mostra resultados
            for img in results[:50]:  # Limita a 50
                domain = img.get('domain', 'N/A')
                width = img.get('width', 0)
                height = img.get('height', 0)
                
                with st.expander(f"📷 {domain} - {width}x{height}px"):
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
                        st.write(f"**🌐 Website:** {domain}")
                        st.write(f"**URL Original:** {img.get('url', 'N/A')[:80]}...")
                        st.write(f"**Fonte:** {img.get('source_url', 'N/A')[:80]}...")
                        st.write(f"**Dimensões:** {width}x{height}px")
                        st.write(f"**Formato:** {img.get('format', 'N/A')}")
                        st.write(f"**Tamanho:** {img.get('size_bytes', 0):,} bytes")
                        st.write(f"**Arquivo:** `{img.get('filename', 'N/A')}`")
                        
                        ocr_text = img.get('text_content')
                        ocr_conf = img.get('confidence')
                        if ocr_text:
                            st.write(f"**Confiança OCR:** {ocr_conf:.2f}%" if ocr_conf else "N/A")
                            st.text_area("📝 Texto OCR", ocr_text, height=100, key=f"ocr_{img.get('id')}")
        else:
            st.info("ℹ️ Nenhuma imagem encontrada")
    
    # Mostrar todas as imagens
    st.markdown("---")
    if st.button("📋 Mostrar Todas as Imagens"):
        conn = sqlite3.connect(extractor.db_path)
        df = pd.read_sql_query('''
            SELECT i.id, i.domain, i.filename, i.url, i.width, i.height, 
                   i.format, i.size_bytes, i.downloaded_at,
                   o.text_content
            FROM images i
            LEFT JOIN ocr_results o ON i.id = o.image_id
            ORDER BY i.domain, i.downloaded_at DESC
        ''', conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Download do DataFrame
            csv = df.to_csv(index=False)
            st.download_button(
                "💾 Baixar CSV",
                csv,
                "images_database.csv",
                "text/csv"
            )
        else:
            st.info("ℹ️ Banco de dados vazio")

# TAB 3: Análises
with tab3:
    st.header("📊 Análises e Relatórios")
    
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
    
    # Análise por dimensão
    st.subheader("📏 Distribuição de Tamanhos")
    df_sizes = pd.read_sql_query('''
        SELECT 
            CASE 
                WHEN width < 100 THEN 'Muito Pequena (< 100px)'
                WHEN width < 500 THEN 'Pequena (100-500px)'
                WHEN width < 1000 THEN 'Média (500-1000px)'
                ELSE 'Grande (> 1000px)'
            END as size_category,
            COUNT(*) as count
        FROM images
        GROUP BY size_category
    ''', conn)
    
    if not df_sizes.empty:
        st.bar_chart(df_sizes.set_index('size_category'))
    
    # Sessões de extração
    st.subheader("🕒 Histórico de Sessões")
    df_sessions = pd.read_sql_query('''
        SELECT id, source_url, images_found, images_downloaded, 
               start_time, end_time, status
        FROM extraction_sessions
        ORDER BY start_time DESC
        LIMIT 20
    ''', conn)
    
    if not df_sessions.empty:
        st.dataframe(df_sessions, use_container_width=True)
    
    # Top imagens com mais texto OCR
    st.subheader("📝 Imagens com Mais Texto (OCR)")
    df_ocr = pd.read_sql_query('''
        SELECT i.filename, i.width, i.height, 
               LENGTH(o.text_content) as text_length,
               o.confidence
        FROM images i
        JOIN ocr_results o ON i.id = o.image_id
        WHERE o.text_content IS NOT NULL
        ORDER BY text_length DESC
        LIMIT 10
    ''', conn)
    
    if not df_ocr.empty:
        st.dataframe(df_ocr, use_container_width=True)
    else:
        st.info("ℹ️ Nenhum texto OCR encontrado ainda")
    
    conn.close()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🖼️ Extrator de Imagens com OCR | Powered by Scrapling + Tesseract + SQLite</p>
    <p><small>Imagens salvas em: <code>extracted_images/</code> | Banco de dados: <code>images_database.db</code></small></p>
</div>
""", unsafe_allow_html=True)
