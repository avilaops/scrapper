"""
Script de teste para verificar extração de diferentes formatos de imagem
"""

import sys
import os
from pathlib import Path

# Configuração do Tesseract
try:
    import tesseract_config
except ImportError:
    pass

from image_extractor import ImageExtractor

def test_format_detection():
    """Testa a detecção de formatos de imagem"""
    print("🧪 TESTE DE DETECÇÃO DE FORMATOS")
    print("=" * 60)
    
    extractor = ImageExtractor()
    
    # URLs de teste com diferentes formatos
    test_urls = [
        "https://example.com/image.jpg",
        "https://example.com/image.jpeg",
        "https://example.com/image.png",
        "https://example.com/image.gif",
        "https://example.com/image.webp",
        "https://example.com/image.bmp",
        "https://example.com/image.tiff",
        "https://example.com/image.tif",
        "https://example.com/image.ico",
        "https://example.com/image.svg",
        "https://example.com/image.heic",
        "https://example.com/image.heif",
        "https://example.com/IMAGE.PNG",  # Teste maiúscula
        "https://example.com/photo?format=jpg",  # Teste query string
    ]
    
    print("\n📋 Testando detecção de extensões:")
    for url in test_urls:
        ext = extractor._get_image_extension(url)
        status = "✅" if ext else "❌"
        print(f"  {status} {url:50s} → {ext}")
    
    print("\n" + "=" * 60)

def test_real_extraction():
    """Testa extração real de um site com múltiplos formatos"""
    print("\n🌐 TESTE DE EXTRAÇÃO REAL")
    print("=" * 60)
    
    # Wikipedia geralmente tem imagens em vários formatos (PNG, JPG, SVG)
    test_url = "https://pt.wikipedia.org/wiki/Imagem"
    
    print(f"\n🔍 Extraindo imagens de: {test_url}")
    print("   (Este site geralmente tem PNG, JPG e SVG)")
    
    extractor = ImageExtractor()
    
    try:
        resultados = extractor.extract_images_from_url(test_url, perform_ocr=False)
        
        print(f"\n📊 Resultados:")
        print(f"  ✅ Imagens encontradas: {resultados['images_found']}")
        print(f"  ✅ Imagens baixadas: {resultados['images_downloaded']}")
        
        if resultados['images_downloaded'] > 0:
            # Analisa formatos baixados
            stats = extractor.get_statistics()
            if stats and stats.get('total_images', 0) > 0:
                print(f"  📂 Total no banco: {stats['total_images']}")
                
                # Busca últimas imagens para ver formatos
                recent = extractor.search_images(limit=10)
                if recent:
                    formats = {}
                    for img in recent:
                        fmt = img.get('format', 'unknown')
                        formats[fmt] = formats.get(fmt, 0) + 1
                    
                    print(f"\n  📸 Formatos detectados:")
                    for fmt, count in formats.items():
                        print(f"     {fmt}: {count} imagem(ns)")
        
        print(f"\n✅ Teste concluído!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante extração: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("=" * 60)

def show_supported_formats():
    """Mostra todos os formatos suportados"""
    print("\n📋 FORMATOS SUPORTADOS")
    print("=" * 60)
    
    extractor = ImageExtractor()
    
    # Acessa o método privado para ver a lista
    supported = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', 
                '.tiff', '.tif', '.ico', '.svg', '.heic', '.heif']
    
    print("\nFormatos de imagem suportados:")
    for i, fmt in enumerate(supported, 1):
        print(f"  {i:2d}. {fmt}")
    
    print(f"\n✅ Total: {len(supported)} formatos")
    print("=" * 60)

def main():
    """Função principal de teste"""
    print("\n" + "=" * 60)
    print("  TESTE DE SUPORTE A FORMATOS DE IMAGEM")
    print("=" * 60)
    
    # 1. Mostra formatos suportados
    show_supported_formats()
    
    # 2. Testa detecção de formatos
    test_format_detection()
    
    # 3. Pergunta se quer fazer teste real
    print("\n⚠️  TESTE REAL")
    print("=" * 60)
    print("O teste real vai:")
    print("  • Acessar a Wikipedia")
    print("  • Baixar imagens de diferentes formatos")
    print("  • Salvar no banco de dados")
    print()
    
    resposta = input("Deseja executar o teste real? (s/n): ").strip().lower()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        test_real_extraction()
    else:
        print("\n⏭️  Teste real pulado.")
    
    print("\n" + "=" * 60)
    print("  ✅ TODOS OS TESTES CONCLUÍDOS")
    print("=" * 60)

if __name__ == "__main__":
    main()
