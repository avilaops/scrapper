"""
Teste rápido de extração de imagens com múltiplos formatos
"""

import sys
import os

# Configuração do Tesseract
try:
    import tesseract_config
except ImportError:
    pass

from image_extractor import ImageExtractor

# URL de teste - Wikipedia BR tem imagens JPG, PNG e SVG
test_url = "https://pt.wikipedia.org/wiki/Python"

print("🧪 TESTE DE EXTRAÇÃO - MÚLTIPLOS FORMATOS")
print("=" * 60)
print(f"URL: {test_url}")
print("=" * 60)

extractor = ImageExtractor()

# Extrai sem OCR para ser mais rápido
print("\n🔍 Extraindo imagens...")
resultados = extractor.extract_images_from_url(test_url, ocr=False)

print("\n📊 RESULTADOS:")
print(f"  • Imagens encontradas: {resultados['total_found']}")
print(f"  • Imagens baixadas: {resultados['downloaded']}")

if resultados['downloaded'] > 0:
    # Busca as últimas imagens baixadas
    print("\n📸 FORMATOS BAIXADOS:")
    recent_images = extractor.search_images(limit=20)
    
    # Conta formatos
    format_counts = {}
    for img in recent_images:
        fmt = img.get('format', 'unknown').upper()
        format_counts[fmt] = format_counts.get(fmt, 0) + 1
    
    # Mostra estatísticas por formato
    for fmt in sorted(format_counts.keys()):
        count = format_counts[fmt]
        bar = "█" * min(count, 30)
        print(f"  {fmt:8s}: {bar} ({count})")
    
    # Mostra algumas imagens de exemplo
    print("\n📋 EXEMPLOS (últimas 5 imagens):")
    for i, img in enumerate(recent_images[:5], 1):
        filename = img.get('filename', 'N/A')
        fmt = img.get('format', 'N/A')
        width = img.get('width', 0)
        height = img.get('height', 0)
        print(f"  {i}. {filename[:40]:40s} | {fmt:5s} | {width}x{height}")

print("\n" + "=" * 60)
print("✅ Teste concluído!")
print("=" * 60)
