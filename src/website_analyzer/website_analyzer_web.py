"""
Interface Web para Analisador Científico de Websites
Streamlit app para análise técnica completa de sites
"""

import streamlit as st
import sqlite3
import pandas as pd
import json
from pathlib import Path
import sys

# Adiciona o diretório src/website_analyzer ao path para importações
module_path = Path(__file__).parent
if str(module_path) not in sys.path:
    sys.path.insert(0, str(module_path))

from website_analyzer import WebsiteAnalyzer
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Analisador Científico de Websites",
    page_icon="🔬",
    layout="wide"
)

# Inicializa o analisador
@st.cache_resource
def get_analyzer():
    return WebsiteAnalyzer()

analyzer = get_analyzer()

# Título
st.title("🔬 Analisador Científico de Websites")
st.markdown("Análise técnica completa: tecnologias, layout, performance, SEO e segurança")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Estatísticas")
    
    # Conta análises
    conn = sqlite3.connect(analyzer.db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM website_analyses')
    total_analyses = cursor.fetchone()[0]
    conn.close()
    
    st.metric("Total de Análises", total_analyses)
    
    st.markdown("---")
    st.header("ℹ️ Sobre")
    st.info("""
    **O que analisamos:**
    
    🔍 **Tecnologias**
    - Frameworks JS/CSS
    - CMS detectado
    - Bibliotecas
    - Analytics
    
    📄 **HTML**
    - Estrutura semântica
    - Acessibilidade
    - Elementos
    
    ⚡ **Performance**
    - Tamanho da página
    - Recursos carregados
    - Otimizações
    
    📊 **SEO**
    - Meta tags
    - Open Graph
    - Schema.org
    
    🔒 **Segurança**
    - HTTPS
    - Headers
    - Vulnerabilidades
    
    🎨 **Layout**
    - Responsividade
    - Grid systems
    - Design patterns
    """)
    
    if st.button("🔄 Atualizar Página"):
        st.cache_resource.clear()
        st.rerun()

# Tabs principais
tab1, tab2, tab3 = st.tabs(["🔬 Nova Análise", "📊 Histórico", "📈 Comparação"])

# TAB 1: Nova Análise
with tab1:
    st.header("Analisar Website")
    
    url = st.text_input(
        "🌐 URL do website",
        placeholder="https://example.com",
        help="Digite a URL completa do website que deseja analisar"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚀 Analisar Website", type="primary", use_container_width=True):
            if not url:
                st.error("❌ Por favor, digite uma URL")
            else:
                with st.spinner("🔬 Analisando website... Isso pode levar alguns segundos..."):
                    try:
                        analysis = analyzer.analyze_website(url)
                        
                        if analysis:
                            st.success("✅ Análise concluída!")
                            
                            # Métricas principais
                            st.subheader("📊 Scores Gerais")
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                seo_score = analysis['seo']['seo_score']
                                color = "🟢" if seo_score >= 70 else "🟡" if seo_score >= 40 else "🔴"
                                st.metric("SEO", f"{seo_score}/100", delta=color)
                            
                            with col2:
                                perf_score = analysis['performance']['optimization_score']
                                color = "🟢" if perf_score >= 70 else "🟡" if perf_score >= 40 else "🔴"
                                st.metric("Performance", f"{perf_score}/100", delta=color)
                            
                            with col3:
                                sec_score = analysis['security']['security_score']
                                color = "🟢" if sec_score >= 70 else "🟡" if sec_score >= 40 else "🔴"
                                st.metric("Segurança", f"{sec_score}/100", delta=color)
                            
                            with col4:
                                acc_score = analysis['html_analysis']['accessibility_score']
                                color = "🟢" if acc_score >= 70 else "🟡" if acc_score >= 40 else "🔴"
                                st.metric("Acessibilidade", f"{acc_score}/100", delta=color)
                            
                            st.markdown("---")
                            
                            # Seções detalhadas
                            col_left, col_right = st.columns(2)
                            
                            with col_left:
                                # TECNOLOGIAS
                                st.subheader("🔍 Tecnologias Detectadas")
                                
                                cms = analysis['technologies'].get('cms')
                                if cms:
                                    st.success(f"**CMS:** {cms}")
                                else:
                                    st.info("**CMS:** Não detectado")
                                
                                frameworks = analysis['technologies'].get('frameworks', [])
                                if frameworks:
                                    st.write("**Frameworks:**")
                                    for fw in frameworks:
                                        st.write(f"  • {fw}")
                                
                                analytics = analysis['technologies'].get('analytics', [])
                                if analytics:
                                    st.write("**Analytics:**")
                                    for tool in analytics:
                                        st.write(f"  • {tool}")
                                
                                # HTML
                                st.markdown("---")
                                st.subheader("📄 Estrutura HTML")
                                
                                html = analysis['html_analysis']
                                st.write(f"**Total de elementos:** {html['total_elements']}")
                                st.write(f"**Elementos semânticos:** {html['semantic_elements']}")
                                st.write(f"**Imagens:** {html['images']}")
                                st.write(f"**Links:** {html['links']}")
                                st.write(f"**Formulários:** {html['forms']}")
                                
                                # Headings
                                if html['headings_structure']:
                                    st.write("**Estrutura de headings:**")
                                    for tag, count in html['headings_structure'].items():
                                        st.write(f"  • {tag}: {count}")
                                
                                # Acessibilidade
                                if html['accessibility_features']:
                                    st.write("**Recursos de acessibilidade:**")
                                    for feature in html['accessibility_features']:
                                        st.write(f"  ✓ {feature}")
                                
                                # JAVASCRIPT
                                st.markdown("---")
                                st.subheader("⚡ JavaScript")
                                
                                js = analysis['js_analysis']
                                st.write(f"**Total de scripts:** {js['total_scripts']}")
                                st.write(f"  • Externos: {js['external_scripts']}")
                                st.write(f"  • Inline: {js['inline_scripts']}")
                                st.write(f"  • Async: {js['async_scripts']}")
                                st.write(f"  • Defer: {js['defer_scripts']}")
                                
                                if js['libraries']:
                                    st.write("**Bibliotecas detectadas:**")
                                    for lib in js['libraries']:
                                        st.write(f"  • {lib}")
                            
                            with col_right:
                                # PERFORMANCE
                                st.subheader("⚡ Performance")
                                
                                perf = analysis['performance']
                                
                                # Gráfico de tamanho
                                fig = go.Figure(go.Indicator(
                                    mode="gauge+number",
                                    value=perf['page_size_kb'],
                                    title={'text': "Tamanho da Página (KB)"},
                                    gauge={
                                        'axis': {'range': [None, 2000]},
                                        'bar': {'color': "darkblue"},
                                        'steps': [
                                            {'range': [0, 500], 'color': "lightgreen"},
                                            {'range': [500, 1000], 'color': "yellow"},
                                            {'range': [1000, 2000], 'color': "red"}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 4},
                                            'thickness': 0.75,
                                            'value': 1000
                                        }
                                    }
                                ))
                                fig.update_layout(height=250)
                                st.plotly_chart(fig, use_container_width=True)
                                
                                st.write(f"**Total de recursos:** {perf['total_resources']}")
                                st.write(f"  • Imagens: {perf['total_images']}")
                                st.write(f"  • Scripts: {perf['total_scripts']}")
                                st.write(f"  • Stylesheets: {perf['total_stylesheets']}")
                                
                                if perf['recommendations']:
                                    st.write("**Recomendações:**")
                                    for rec in perf['recommendations']:
                                        if '✓' in rec:
                                            st.success(rec)
                                        else:
                                            st.warning(rec)
                                
                                # SEO
                                st.markdown("---")
                                st.subheader("📊 SEO")
                                
                                seo = analysis['seo']
                                
                                if seo['title']:
                                    st.write(f"**Title ({seo['title_length']} caracteres):**")
                                    st.info(seo['title'])
                                
                                if seo['meta_description']:
                                    st.write(f"**Meta Description ({seo['meta_description_length']} caracteres):**")
                                    st.info(seo['meta_description'])
                                
                                st.write(f"**H1 na página:** {seo['h1_count']}")
                                
                                if seo['og_tags']:
                                    st.write(f"**Open Graph tags:** {len(seo['og_tags'])}")
                                
                                if seo['structured_data']:
                                    st.write(f"**Structured Data (Schema.org):** ✓ Detectado")
                                
                                if seo['issues']:
                                    st.write("**Problemas SEO:**")
                                    for issue in seo['issues']:
                                        st.error(f"• {issue}")
                                
                                # SEGURANÇA
                                st.markdown("---")
                                st.subheader("🔒 Segurança")
                                
                                sec = analysis['security']
                                
                                if sec['https_enabled']:
                                    st.success("✓ HTTPS habilitado")
                                else:
                                    st.error("✗ HTTPS não habilitado")
                                
                                if sec['vulnerabilities']:
                                    st.write("**Vulnerabilidades:**")
                                    for vuln in sec['vulnerabilities']:
                                        st.warning(f"• {vuln}")
                            
                            # Seção completa - Layout
                            st.markdown("---")
                            st.subheader("🎨 Layout e Design")
                            
                            layout = analysis['layout']
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if layout['viewport_meta']:
                                    st.success("✓ Viewport meta tag")
                                else:
                                    st.error("✗ Sem viewport meta tag")
                            
                            with col2:
                                st.write(f"**Tipo de layout:** {layout['layout_type']}")
                            
                            with col3:
                                if layout['responsive_indicators']:
                                    st.success(f"✓ Responsivo ({len(layout['responsive_indicators'])} indicadores)")
                            
                            # Exportar
                            st.markdown("---")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("💾 Exportar Análise (JSON)"):
                                    filename = analyzer.export_analysis_json(analysis['id'])
                                    if filename:
                                        with open(filename, 'r', encoding='utf-8') as f:
                                            st.download_button(
                                                "⬇️ Download JSON",
                                                f.read(),
                                                filename,
                                                "application/json"
                                            )
                            
                            with col2:
                                st.success(f"📊 Análise salva com ID: {analysis['id']}")
                            
                            st.cache_resource.clear()
                        
                    except Exception as e:
                        st.error(f"❌ Erro durante análise: {str(e)}")
                        st.exception(e)
    
    with col2:
        st.info("💡 Dica: A análise pode levar de 10 a 30 segundos")

# TAB 2: Histórico
with tab2:
    st.header("Histórico de Análises")
    
    analyses = analyzer.get_all_analyses(limit=100)
    
    if analyses:
        st.success(f"✅ {len(analyses)} análise(s) encontrada(s)")
        
        # Cria DataFrame
        df = pd.DataFrame(analyses)
        df['analyzed_at'] = pd.to_datetime(df['analyzed_at'])
        
        # Mostra tabela
        st.dataframe(
            df[['id', 'domain', 'analyzed_at', 'seo_score', 'optimization_score', 'security_score']],
            use_container_width=True,
            column_config={
                "id": "ID",
                "domain": "Domínio",
                "analyzed_at": st.column_config.DatetimeColumn("Data da Análise", format="DD/MM/YYYY HH:mm"),
                "seo_score": st.column_config.ProgressColumn("SEO", min_value=0, max_value=100),
                "optimization_score": st.column_config.ProgressColumn("Performance", min_value=0, max_value=100),
                "security_score": st.column_config.ProgressColumn("Segurança", min_value=0, max_value=100),
            }
        )
        
        # Gráficos de estatísticas
        st.markdown("---")
        st.subheader("📈 Estatísticas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de scores médios
            avg_scores = {
                'SEO': df['seo_score'].mean(),
                'Performance': df['optimization_score'].mean(),
                'Segurança': df['security_score'].mean()
            }
            
            fig = go.Figure(data=[
                go.Bar(x=list(avg_scores.keys()), y=list(avg_scores.values()))
            ])
            fig.update_layout(
                title="Scores Médios",
                yaxis_title="Score (0-100)",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top domínios analisados
            domain_counts = df['domain'].value_counts().head(10)
            
            fig = go.Figure(data=[
                go.Pie(labels=domain_counts.index, values=domain_counts.values)
            ])
            fig.update_layout(title="Top 10 Domínios Analisados")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detalhes de uma análise
        st.markdown("---")
        st.subheader("🔍 Ver Detalhes de uma Análise")
        
        analysis_id = st.selectbox(
            "Selecione uma análise:",
            options=df['id'].tolist(),
            format_func=lambda x: f"ID {x} - {df[df['id']==x]['domain'].values[0]} ({df[df['id']==x]['analyzed_at'].values[0]})"
        )
        
        if st.button("📊 Carregar Análise"):
            full_analysis = analyzer.get_analysis(analysis_id)
            
            if full_analysis:
                st.json(full_analysis)
                
                # Botão de exportar
                if st.button("💾 Exportar esta análise"):
                    filename = analyzer.export_analysis_json(analysis_id)
                    if filename:
                        with open(filename, 'r', encoding='utf-8') as f:
                            st.download_button(
                                "⬇️ Download JSON",
                                f.read(),
                                filename,
                                "application/json"
                            )
    else:
        st.info("ℹ️ Nenhuma análise realizada ainda. Faça a primeira análise na aba 'Nova Análise'!")

# TAB 3: Comparação
with tab3:
    st.header("Comparação de Websites")
    
    analyses = analyzer.get_all_analyses()
    
    if len(analyses) >= 2:
        st.info("Selecione duas análises para comparar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            analysis1_id = st.selectbox(
                "Website 1:",
                options=[a['id'] for a in analyses],
                format_func=lambda x: next(a['domain'] for a in analyses if a['id'] == x)
            )
        
        with col2:
            analysis2_id = st.selectbox(
                "Website 2:",
                options=[a['id'] for a in analyses if a['id'] != analysis1_id],
                format_func=lambda x: next(a['domain'] for a in analyses if a['id'] == x)
            )
        
        if st.button("⚖️ Comparar"):
            a1 = next(a for a in analyses if a['id'] == analysis1_id)
            a2 = next(a for a in analyses if a['id'] == analysis2_id)
            
            # Gráfico de radar comparativo
            categories = ['SEO', 'Performance', 'Segurança']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=[a1['seo_score'], a1['optimization_score'], a1['security_score']],
                theta=categories,
                fill='toself',
                name=a1['domain']
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=[a2['seo_score'], a2['optimization_score'], a2['security_score']],
                theta=categories,
                fill='toself',
                name=a2['domain']
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title="Comparação de Scores"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela comparativa
            comparison_df = pd.DataFrame({
                'Métrica': ['SEO Score', 'Performance Score', 'Security Score'],
                a1['domain']: [a1['seo_score'], a1['optimization_score'], a1['security_score']],
                a2['domain']: [a2['seo_score'], a2['optimization_score'], a2['security_score']]
            })
            
            st.dataframe(comparison_df, use_container_width=True)
    else:
        st.info("ℹ️ São necessárias pelo menos 2 análises para comparação. Faça mais análises primeiro!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔬 Analisador Científico de Websites v1.0</p>
    <p>Análise completa de tecnologias, performance, SEO e segurança</p>
</div>
""", unsafe_allow_html=True)
