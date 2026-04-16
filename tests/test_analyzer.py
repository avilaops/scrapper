"""
Teste do Analisador Científico de Websites
"""

from website_analyzer import WebsiteAnalyzer

print("="*70)
print("  🧪 TESTE DO ANALISADOR CIENTÍFICO")
print("="*70)

# Cria o analisador
analyzer = WebsiteAnalyzer()

# URL de teste
test_url = "http://quotes.toscrape.com"

print(f"\n🌐 Analisando: {test_url}\n")

# Faz análise
analysis = analyzer.analyze_website(test_url)

if analysis:
    print(f"\n{'='*70}")
    print("✅ ANÁLISE CONCLUÍDA")
    print(f"{'='*70}")
    
    print(f"\n📊 ID da análise: {analysis['id']}")
    print(f"🌐 Domínio: {analysis['domain']}")
    
    print(f"\n🔍 TECNOLOGIAS DETECTADAS:")
    print(f"  CMS: {analysis['technologies'].get('cms', 'Não detectado')}")
    print(f"  Frameworks: {', '.join(analysis['technologies']['frameworks']) if analysis['technologies']['frameworks'] else 'Nenhum'}")
    print(f"  Analytics: {', '.join(analysis['technologies']['analytics']) if analysis['technologies']['analytics'] else 'Nenhum'}")
    
    print(f"\n📄 HTML:")
    print(f"  Total de elementos: {analysis['html_analysis']['total_elements']}")
    print(f"  Score semântico: {analysis['html_analysis']['semantic_score']:.0f}/100")
    print(f"  Score acessibilidade: {analysis['html_analysis']['accessibility_score']}/100")
    print(f"  Imagens: {analysis['html_analysis']['images']}")
    print(f"  Links: {analysis['html_analysis']['links']}")
    
    print(f"\n⚡ PERFORMANCE:")
    print(f"  Tamanho: {analysis['performance']['page_size_kb']} KB")
    print(f"  Recursos: {analysis['performance']['total_resources']}")
    print(f"  Score: {analysis['performance']['optimization_score']}/100")
    
    print(f"\n📊 SEO:")
    print(f"  Title: {analysis['seo']['title'][:60]}...")
    print(f"  Title Length: {analysis['seo']['title_length']} caracteres")
    print(f"  Meta Description: {'✓' if analysis['seo']['meta_description'] else '✗'}")
    print(f"  H1 Count: {analysis['seo']['h1_count']}")
    print(f"  Score: {analysis['seo']['seo_score']}/100")
    
    print(f"\n🔒 SEGURANÇA:")
    print(f"  HTTPS: {'✓' if analysis['security']['https_enabled'] else '✗'}")
    print(f"  Score: {analysis['security']['security_score']}/100")
    
    print(f"\n🎨 LAYOUT:")
    print(f"  Viewport: {'✓' if analysis['layout']['viewport_meta'] else '✗'}")
    print(f"  Tipo: {analysis['layout']['layout_type']}")
    print(f"  Responsivo: {len(analysis['layout']['responsive_indicators'])} indicadores")
    
    # Testa listagem
    print(f"\n{'='*70}")
    print("📋 HISTÓRICO DE ANÁLISES")
    print(f"{'='*70}")
    
    all_analyses = analyzer.get_all_analyses(limit=5)
    for a in all_analyses:
        print(f"\n  ID {a['id']}: {a['domain']}")
        print(f"    Data: {a['analyzed_at']}")
        print(f"    SEO: {a['seo_score']}/100 | Perf: {a['optimization_score']}/100 | Sec: {a['security_score']}/100")
    
    print(f"\n{'='*70}")
    print("✅ TESTE CONCLUÍDO COM SUCESSO")
    print(f"{'='*70}")

else:
    print("\n❌ Erro na análise")
