"""
Teste rápido de download com organização por domínio
"""

import sys
import os

# Configuração do Tesseract
try:
    import tesseract_config
except ImportError:
    pass

from image_extractor import ImageExtractor

print("=" * 70)
print("  🧪 TESTE DE DOWNLOAD COM ORGANIZAÇÃO POR DOMÍNIO")
print("=" * 70)

extractor = ImageExtractor()

# URL de teste
test_url = "https://quotes.toscrape.com"

print(f"\n🌐 Testando com: {test_url}")
print("   (Baixando sem OCR para ser rápido)")
print()

# Extrai
resultados = extractor.extract_images_from_url(test_url, ocr=False)

print(f"\n📊 Resultados:")
print(f"  Encontradas: {resultados['total_found']}")
print(f"  Baixadas: {resultados['downloaded']}")

# Verifica pastas criadas
from pathlib import Path

images_folder = Path("extracted_images")
domains = [d for d in images_folder.iterdir() if d.is_dir()]

print(f"\n📁 Pastas de domínios criadas:")
for domain_folder in sorted(domains):
    images = list(domain_folder.glob("*.*"))
    print(f"  🌐 {domain_folder.name}: {len(images)} imagem(ns)")
    for img in images[:3]:
        print(f"     - {img.name}")

# Testa estatísticas
print(f"\n📊 Estatísticas do banco:")
domains_stats = extractor.get_domains_stats()
for domain_info in domains_stats:
    print(f"  🌐 {domain_info['domain']}: {domain_info['count']} imagens")

print("\n" + "=" * 70)
print("✅ Teste concluído!")
print("=" * 70)
