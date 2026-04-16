"""
Teste final de extração de múltiplos formatos
"""

import sys
import os

# Configuração do Tesseract
try:
    import tesseract_config
except ImportError:
    pass

from image_extractor import ImageExtractor

def test_multiple_sites():
    """Testa extração em sites com diferentes formatos"""
    print("=" * 70)
    print("  🧪 TESTE FINAL - EXTRAÇÃO DE MÚLTIPLOS FORMATOS")
    print("=" * 70)
    
    extractor = ImageExtractor()
    
    # Sites de teste com diferentes formatos
    test_sites = [
        {
            'url': 'https://httpbin.org/html',
            'desc': 'Página HTML simples (teste PNG/JPG)'
        },
        {
            'url': 'https://example.com',
            'desc': 'Example.com (teste básico)'
        }
    ]
    
    all_formats = {}
    total_downloaded = 0
    
    for site in test_sites:
        print(f"\n{'='*70}")
        print(f"🌐 {site['desc']}")
        print(f"   URL: {site['url']}")
        print(f"{'='*70}")
        
        try:
            resultados = extractor.extract_images_from_url(site['url'], ocr=False)
            
            total_downloaded += resultados['downloaded']
            
            print(f"\n  📊 Resumo:")
            print(f"     Encontradas: {resultados['total_found']}")
            print(f"     Baixadas: {resultados['downloaded']}")
            print(f"     Erros: {resultados['errors']}")
            
        except Exception as e:
            print(f"\n  ❌ Erro: {e}")
    
    # Mostra estatísticas gerais do banco
    print(f"\n{'='*70}")
    print("  📈 ESTATÍSTICAS GERAIS DO BANCO DE DADOS")
    print(f"{'='*70}")
    
    stats = extractor.get_statistics()
    if stats:
        print(f"\n  Total de imagens no banco: {stats['total_images']}")
        print(f"  Tamanho total: {stats['total_size_bytes'] / 1024 / 1024:.2f} MB")
    
    # Busca todas as imagens para ver formatos
    all_images = extractor.search_images(limit=100)
    
    if all_images:
        # Conta formatos
        format_counts = {}
        for img in all_images:
            fmt = img.get('format', 'UNKNOWN')
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
        
        print(f"\n  📸 FORMATOS DETECTADOS:")
        print(f"  {'Formato':<15} {'Quantidade':>10}")
        print(f"  {'-'*27}")
        for fmt in sorted(format_counts.keys()):
            count = format_counts[fmt]
            print(f"  {fmt:<15} {count:>10}")
        
        total_formats = len(format_counts)
        print(f"  {'-'*27}")
        print(f"  {'TOTAL':<15} {len(all_images):>10}")
        print(f"\n  ✅ {total_formats} formato(s) diferente(s) encontrado(s)!")
    
    print(f"\n{'='*70}")
    print("  ✅ TESTE CONCLUÍDO")
    print(f"{'='*70}")

def show_current_database():
    """Mostra o estado atual do banco de dados"""
    print("\n📂 BANCO DE DADOS ATUAL")
    print("=" * 70)
    
    extractor = ImageExtractor()
    images = extractor.search_images(limit=20)
    
    if not images:
        print("  ⚠️  Banco de dados vazio")
        return
    
    print(f"\n  Últimas {len(images)} imagens:")
    print(f"  {'#':<4} {'Arquivo':<35} {'Formato':<8} {'Dimensões':<12} {'Tamanho'}")
    print(f"  {'-'*70}")
    
    for i, img in enumerate(images, 1):
        filename = img.get('filename', 'N/A')[:32]
        fmt = img.get('format', 'N/A')
        width = img.get('width', 0)
        height = img.get('height', 0)
        size_kb = img.get('size_bytes', 0) / 1024
        
        dims = f"{width}x{height}" if width > 0 else "N/A"
        
        print(f"  {i:<4} {filename:<35} {fmt:<8} {dims:<12} {size_kb:>6.1f} KB")
    
    print("=" * 70)

if __name__ == "__main__":
    # Primeiro mostra o que já tem no banco
    show_current_database()
    
    # Depois faz novos testes
    test_multiple_sites()
