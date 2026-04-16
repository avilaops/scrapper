"""
Teste de organização por website
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

def test_domain_extraction():
    """Testa extração de domínio"""
    print("=" * 70)
    print("  🧪 TESTE DE EXTRAÇÃO DE DOMÍNIO")
    print("=" * 70)
    
    extractor = ImageExtractor()
    
    test_urls = [
        "https://pt.wikipedia.org/wiki/Python",
        "https://www.example.com/page",
        "http://quotes.toscrape.com/",
        "https://httpbin.org/html",
        "https://github.com/user/repo",
    ]
    
    print("\n📋 Testando extração de domínios:")
    for url in test_urls:
        domain = extractor._get_domain(url)
        print(f"  {url:50s} → {domain}")
    
    print("\n" + "=" * 70)

def test_folder_organization():
    """Testa se as pastas estão sendo criadas corretamente"""
    print("\n🔍 TESTE DE ORGANIZAÇÃO DE PASTAS")
    print("=" * 70)
    
    images_folder = Path("extracted_images")
    
    if not images_folder.exists():
        print("  ⚠️  Pasta extracted_images não existe ainda")
        return
    
    # Lista subpastas (domínios)
    domains = [d for d in images_folder.iterdir() if d.is_dir()]
    
    if not domains:
        print("  ⚠️  Nenhuma subpasta de domínio encontrada")
        return
    
    print(f"\n  📁 Encontradas {len(domains)} pasta(s) de websites:\n")
    
    for domain_folder in sorted(domains):
        images = list(domain_folder.glob("*.*"))
        total_size = sum(img.stat().st_size for img in images)
        
        print(f"  🌐 {domain_folder.name}")
        print(f"     📸 {len(images)} imagem(ns)")
        print(f"     💾 {total_size / 1024:.1f} KB")
        
        # Mostra primeiras 3 imagens
        for img in images[:3]:
            print(f"        - {img.name}")
        if len(images) > 3:
            print(f"        ... e mais {len(images) - 3}")
        print()
    
    print("=" * 70)

def test_database_domains():
    """Testa estatísticas de domínios no banco"""
    print("\n📊 TESTE DE ESTATÍSTICAS POR DOMÍNIO")
    print("=" * 70)
    
    extractor = ImageExtractor()
    domains = extractor.get_domains_stats()
    
    if not domains:
        print("  ⚠️  Nenhum domínio no banco de dados")
        return
    
    print(f"\n  Domínios cadastrados: {len(domains)}\n")
    print(f"  {'Domínio':<35} {'Imagens':>10} {'Tamanho':>12}")
    print(f"  {'-' * 60}")
    
    for domain_info in domains:
        domain = domain_info['domain']
        count = domain_info['count']
        size_mb = domain_info['size_bytes'] / (1024 * 1024)
        
        print(f"  {domain:<35} {count:>10} {size_mb:>11.2f} MB")
    
    print(f"  {'-' * 60}")
    
    total_images = sum(d['count'] for d in domains)
    total_size = sum(d['size_bytes'] for d in domains) / (1024 * 1024)
    
    print(f"  {'TOTAL':<35} {total_images:>10} {total_size:>11.2f} MB")
    
    print("\n" + "=" * 70)

def main():
    """Função principal"""
    print("\n" + "=" * 70)
    print("  TESTE DE ORGANIZAÇÃO POR WEBSITE")
    print("=" * 70)
    
    # 1. Testa extração de domínio
    test_domain_extraction()
    
    # 2. Testa organização de pastas
    test_folder_organization()
    
    # 3. Testa estatísticas do banco
    test_database_domains()
    
    print("\n" + "=" * 70)
    print("  ✅ TODOS OS TESTES CONCLUÍDOS")
    print("=" * 70)

if __name__ == "__main__":
    main()
