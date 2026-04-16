"""
Script para extrair todas as informações do site Vizzio Engenharia
e salvar em JSON estruturado para recriação do site.
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Adiciona o Scrapling ao path
project_root = Path(__file__).parent
scrapling_path = project_root / "Scrapling"
if str(scrapling_path) not in sys.path:
    sys.path.insert(0, str(scrapling_path))

from scrapling.fetchers import Fetcher
import re

def clean_text(text):
    """Limpa e normaliza texto"""
    if not text:
        return ""
    # Remove espaços extras
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_all_data(url):
    """Extrai todas as informações do site"""
    
    print(f"🔍 Acessando {url}...")
    page = Fetcher.get(url)
    
    if not page:
        print("❌ Erro ao acessar o site")
        return None
    
    print(f"✅ Site acessado com sucesso! (Status: {page.status})")
    
    data = {
        "metadata": {
            "url": url,
            "extracted_at": datetime.now().isoformat(),
            "title": "",
            "description": "",
            "keywords": ""
        },
        "header": {
            "logo": "",
            "menu": []
        },
        "hero": {
            "title": "",
            "subtitle": "",
            "image": "",
            "cta_buttons": []
        },
        "sections": [],
        "services": [],
        "about": {
            "title": "",
            "description": "",
            "images": []
        },
        "contact": {
            "phone": [],
            "email": [],
            "address": "",
            "social_media": []
        },
        "footer": {
            "text": "",
            "links": [],
            "copyright": ""
        },
        "all_images": [],
        "all_links": [],
        "all_texts": []
    }
    
    # ========== METADATA ==========
    print("\n📋 Extraindo metadata...")
    
    title = page.css('title::text').get()
    data["metadata"]["title"] = clean_text(title) if title else ""
    
    meta_desc = page.css('meta[name="description"]::attr(content)').get()
    data["metadata"]["description"] = clean_text(meta_desc) if meta_desc else ""
    
    meta_keywords = page.css('meta[name="keywords"]::attr(content)').get()
    data["metadata"]["keywords"] = clean_text(meta_keywords) if meta_keywords else ""
    
    print(f"  • Title: {data['metadata']['title'][:50]}...")
    
    # ========== HEADER / MENU ==========
    print("\n🔝 Extraindo header e menu...")
    
    # Logo
    logo = page.css('header img::attr(src), .logo img::attr(src), nav img::attr(src)').get()
    if logo:
        data["header"]["logo"] = logo
        print(f"  • Logo: {logo}")
    
    # Menu items
    menu_links = page.css('nav a, header a, .menu a').getall()
    for item in menu_links:
        if isinstance(item, str):
            # É apenas texto
            if item.strip():
                data["header"]["menu"].append({
                    "text": clean_text(item),
                    "url": "#"
                })
    
    # Tenta extrair menu de outra forma
    menu_hrefs = page.css('nav a::attr(href), header a::attr(href), .menu a::attr(href)').getall()
    menu_texts = page.css('nav a::text, header a::text, .menu a::text').getall()
    
    for i, text in enumerate(menu_texts):
        if text and text.strip():
            href = menu_hrefs[i] if i < len(menu_hrefs) else "#"
            data["header"]["menu"].append({
                "text": clean_text(text),
                "url": href if href else "#"
            })
    
    print(f"  • Menu items: {len(data['header']['menu'])}")
    
    # ========== HEADINGS (H1, H2, H3) ==========
    print("\n📝 Extraindo títulos e seções...")
    
    # H1 (geralmente hero/título principal)
    h1_texts = page.css('h1::text').getall()
    for text in h1_texts:
        if text:
            clean_h1 = clean_text(text)
            if clean_h1:
                if not data["hero"]["title"]:
                    data["hero"]["title"] = clean_h1
                else:
                    data["sections"].append({
                        "type": "heading_1",
                        "content": clean_h1
                    })
    
    # H2 (títulos de seções)
    h2_texts = page.css('h2::text').getall()
    for text in h2_texts:
        if text:
            clean_h2 = clean_text(text)
            if clean_h2:
                data["sections"].append({
                    "type": "heading_2",
                    "content": clean_h2
                })
    
    # H3 (subtítulos)
    h3_texts = page.css('h3::text').getall()
    for text in h3_texts:
        if text:
            clean_h3 = clean_text(text)
            if clean_h3:
                data["sections"].append({
                    "type": "heading_3",
                    "content": clean_h3
                })
    
    print(f"  • H1: {len(h1_texts)} | H2: {len(h2_texts)} | H3: {len(h3_texts)}")
    
    # ========== PARÁGRAFOS ==========
    print("\n📄 Extraindo parágrafos...")
    
    paragraphs = page.css('p::text').getall()
    for i, p in enumerate(paragraphs):
        clean_p = clean_text(p)
        if clean_p and len(clean_p) > 20:  # Ignora parágrafos muito curtos
            data["all_texts"].append(clean_p)
            
            # Tenta identificar seções especiais
            if i < 3 and not data["hero"]["subtitle"]:
                data["hero"]["subtitle"] = clean_p
    
    print(f"  • Parágrafos: {len(data['all_texts'])}")
    
    # ========== IMAGENS ==========
    print("\n🖼️ Extraindo imagens...")
    
    img_srcs = page.css('img::attr(src)').getall()
    img_alts = page.css('img::attr(alt)').getall()
    
    for i, src in enumerate(img_srcs):
        if src:
            alt = img_alts[i] if i < len(img_alts) else ""
            
            img_data = {
                "src": src,
                "alt": clean_text(alt) if alt else "",
                "type": "image"
            }
            data["all_images"].append(img_data)
            
            # Hero image (primeira imagem grande ou imagem de banner)
            if not data["hero"]["image"] and any(keyword in src.lower() for keyword in ['banner', 'hero', 'slide', 'main']):
                data["hero"]["image"] = src
    
    print(f"  • Imagens: {len(data['all_images'])}")
    
    # ========== LINKS ==========
    print("\n🔗 Extraindo links...")
    
    link_hrefs = page.css('a::attr(href)').getall()
    link_texts = page.css('a::text').getall()
    link_classes = page.css('a::attr(class)').getall()
    
    for i, href in enumerate(link_hrefs):
        if href:
            text = link_texts[i] if i < len(link_texts) else ""
            classes = link_classes[i] if i < len(link_classes) else ""
            
            link_data = {
                "url": href,
                "text": clean_text(text) if text else "",
                "type": "link"
            }
            data["all_links"].append(link_data)
            
            # Identifica botões CTA
            if classes and any(keyword in classes.lower() for keyword in ['btn', 'button', 'cta']):
                if text:
                    data["hero"]["cta_buttons"].append({
                        "text": clean_text(text),
                        "url": href
                    })
    
    print(f"  • Links: {len(data['all_links'])}")
    
    # ========== SERVIÇOS ==========
    print("\n⚙️ Procurando seção de serviços...")
    
    # Procura por cards/items de serviço
    service_selectors = [
        ('.service', 'h2::text, h3::text, h4::text', 'p::text', 'img::attr(src)'),
        ('.servico', 'h2::text, h3::text, h4::text', 'p::text', 'img::attr(src)'),
        ('.card', 'h2::text, h3::text, h4::text', 'p::text', 'img::attr(src)'),
        ('article', 'h2::text, h3::text, h4::text', 'p::text', 'img::attr(src)'),
    ]
    
    # Tenta detectar serviços de forma mais simples
    # Procura por h3 ou h4 seguidos de parágrafos
    service_titles = page.css('h3::text, h4::text').getall()
    service_descs = page.css('p::text').getall()
    
    # Associa títulos com descrições
    for i, title in enumerate(service_titles[:10]):  # Limita a 10
        if title and clean_text(title):
            desc = service_descs[i] if i < len(service_descs) else ""
            data["services"].append({
                "title": clean_text(title),
                "description": clean_text(desc) if desc else "",
                "image": ""
            })
    
    if data["services"]:
        print(f"  • Serviços encontrados: {len(data['services'])}")
    
    # ========== CONTATO ==========
    print("\n📞 Procurando informações de contato...")
    
    # Telefones
    phone_pattern = r'(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?\d{4,5}[-\s]?\d{4}'
    all_text = page.text
    phones = re.findall(phone_pattern, all_text)
    data["contact"]["phone"] = list(set([p.strip() for p in phones]))
    
    # Emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, all_text)
    data["contact"]["email"] = list(set(emails))
    
    # Redes sociais
    social_patterns = {
        'facebook': 'Facebook',
        'instagram': 'Instagram',
        'linkedin': 'LinkedIn',
        'twitter': 'Twitter',
        'youtube': 'YouTube'
    }
    
    for pattern, network in social_patterns.items():
        social_links = page.css(f'a[href*="{pattern}"]::attr(href)').getall()
        for href in social_links:
            if href:
                data["contact"]["social_media"].append({
                    "network": network,
                    "url": href
                })
    
    print(f"  • Telefones: {len(data['contact']['phone'])}")
    print(f"  • Emails: {len(data['contact']['email'])}")
    print(f"  • Redes sociais: {len(data['contact']['social_media'])}")
    
    # ========== FOOTER ==========
    print("\n👣 Extraindo footer...")
    
    footer_texts = page.css('footer p::text').getall()
    if footer_texts:
        data["footer"]["text"] = " ".join([clean_text(t) for t in footer_texts if t])
    
    footer_link_hrefs = page.css('footer a::attr(href)').getall()
    footer_link_texts = page.css('footer a::text').getall()
    
    for i, href in enumerate(footer_link_hrefs):
        text = footer_link_texts[i] if i < len(footer_link_texts) else ""
        if href and text:
            data["footer"]["links"].append({
                "text": clean_text(text),
                "url": href
            })
    
    # Copyright
    copyright_text = page.css('*:contains("©")::text, *:contains("Copyright")::text').get()
    if copyright_text:
        data["footer"]["copyright"] = clean_text(copyright_text)
    
    return data

def save_to_json(data, filename="vizzio_engenharia_data.json"):
    """Salva os dados em JSON"""
    output_path = Path(__file__).parent / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return output_path

def main():
    url = "https://vizzioengenharia.com.br/"
    
    print("=" * 60)
    print("🕷️  EXTRATOR DE SITE - VIZZIO ENGENHARIA")
    print("=" * 60)
    
    # Extrai dados
    data = extract_all_data(url)
    
    if not data:
        print("\n❌ Falha ao extrair dados")
        return
    
    # Salva em JSON
    print("\n" + "=" * 60)
    print("💾 Salvando dados em JSON...")
    output_path = save_to_json(data)
    
    # Estatísticas
    print("\n" + "=" * 60)
    print("✅ EXTRAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"\n📄 Arquivo salvo em: {output_path}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"  • Title: {data['metadata']['title']}")
    print(f"  • Menu items: {len(data['header']['menu'])}")
    print(f"  • Seções: {len(data['sections'])}")
    print(f"  • Serviços: {len(data['services'])}")
    print(f"  • Imagens: {len(data['all_images'])}")
    print(f"  • Links: {len(data['all_links'])}")
    print(f"  • Textos: {len(data['all_texts'])}")
    print(f"  • Telefones: {len(data['contact']['phone'])}")
    print(f"  • Emails: {len(data['contact']['email'])}")
    print(f"  • Redes sociais: {len(data['contact']['social_media'])}")
    
    print(f"\n✨ Tamanho do arquivo: {output_path.stat().st_size / 1024:.2f} KB")
    print("\n🎉 Você pode usar este JSON para recriar o site!")
    print("=" * 60)

if __name__ == "__main__":
    main()
