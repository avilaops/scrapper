"""
Script para limpar e melhorar os dados extraídos do site Vizzio Engenharia
"""

import json
import re
from pathlib import Path

def clean_menu_text(text):
    """Remove tags HTML do texto do menu"""
    # Extrai apenas o texto do parágrafo
    match = re.search(r'<p[^>]*>([^<]+)</p>', text)
    if match:
        return match.group(1)
    return text

def clean_menu_url(text):
    """Extrai a URL do href no HTML"""
    match = re.search(r'href="([^"]+)"', text)
    if match:
        return match.group(1)
    return "#"

def improve_data(json_file="vizzio_engenharia_data.json"):
    """Melhora os dados extraídos"""
    
    file_path = Path(__file__).parent / json_file
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🔧 Melhorando dados extraídos...")
    
    # Limpa menu
    if data["header"]["menu"]:
        cleaned_menu = []
        for item in data["header"]["menu"]:
            menu_text = clean_menu_text(item["text"])
            menu_url = clean_menu_url(item["text"])
            
            # Evita duplicatas
            if not any(m["text"] == menu_text for m in cleaned_menu):
                cleaned_menu.append({
                    "text": menu_text,
                    "url": menu_url
                })
        
        data["header"]["menu"] = cleaned_menu
        print(f"  ✅ Menu limpo: {len(cleaned_menu)} items")
    
    # Adiciona informações de contato do footer (WhatsApp encontrado)
    for link in data["footer"]["links"]:
        if "wa.me" in link["url"]:
            phone_match = re.search(r'(\d+)', link["url"])
            if phone_match:
                phone = phone_match.group(1)
                # Formata o telefone brasileiro
                if len(phone) >= 12:
                    formatted = f"+{phone[:2]} ({phone[2:4]}) {phone[4:9]}-{phone[9:]}"
                    if formatted not in data["contact"]["phone"]:
                        data["contact"]["phone"].append(formatted)
                        print(f"  ✅ Telefone encontrado: {formatted}")
    
    # Adiciona email do footer
    for link in data["footer"]["links"]:
        if "mailto:" in link["url"]:
            email = link["url"].replace("mailto:", "")
            if email not in data["contact"]["email"]:
                data["contact"]["email"].append(email)
                print(f"  ✅ Email encontrado: {email}")
    
    # Salva dados melhorados
    output_file = file_path.parent / "vizzio_engenharia_data_clean.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Dados melhorados salvos em: {output_file}")
    
    return data, output_file

def create_html_viewer(data, output_file="vizzio_site_viewer.html"):
    """Cria um visualizador HTML dos dados"""
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vizzio Engenharia - Dados Extraídos</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .card h3 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .card p {{
            color: #555;
        }}
        
        .menu-list {{
            list-style: none;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        
        .menu-list li a {{
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .menu-list li a:hover {{
            background: #5568d3;
            transform: translateY(-2px);
        }}
        
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .image-grid img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .contact-info {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
        }}
        
        .contact-info h3 {{
            margin-bottom: 10px;
        }}
        
        .contact-info a {{
            color: #fff;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .social-media {{
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }}
        
        .social-media a {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 5px;
            transition: all 0.3s;
        }}
        
        .social-media a:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .stat-box .number {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        .stat-box .label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        footer {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏗️ {data['metadata']['title']}</h1>
            <p>{data['metadata']['description']}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Dados extraídos em: {data['metadata']['extracted_at'][:10]}
            </p>
        </header>
        
        <div class="content">
            <!-- Estatísticas -->
            <div class="stats">
                <div class="stat-box">
                    <div class="number">{len(data['header']['menu'])}</div>
                    <div class="label">Páginas</div>
                </div>
                <div class="stat-box">
                    <div class="number">{len(data['all_images'])}</div>
                    <div class="label">Imagens</div>
                </div>
                <div class="stat-box">
                    <div class="number">{len(data['sections'])}</div>
                    <div class="label">Seções</div>
                </div>
                <div class="stat-box">
                    <div class="number">{len(data['all_links'])}</div>
                    <div class="label">Links</div>
                </div>
            </div>
            
            <!-- Menu/Navegação -->
            <div class="section">
                <h2>📋 Navegação do Site</h2>
                <ul class="menu-list">
"""
    
    # Menu
    for item in data['header']['menu']:
        html += f'                    <li><a href="{item["url"]}">{item["text"]}</a></li>\n'
    
    html += """                </ul>
            </div>
"""
    
    # Seções
    if data['sections']:
        html += """            <div class="section">
                <h2>📝 Seções do Site</h2>
                <div class="grid">
"""
        for section in data['sections']:
            html += f"""                    <div class="card">
                        <h3>{section['content']}</h3>
                        <p><span class="badge">{section['type'].replace('_', ' ').title()}</span></p>
                    </div>
"""
        html += """                </div>
            </div>
"""
    
    # Textos
    if data['all_texts']:
        html += """            <div class="section">
                <h2>📄 Conteúdo Textual</h2>
"""
        for text in data['all_texts'][:5]:  # Primeiros 5
            html += f'                <div class="card"><p>{text}</p></div>\n'
        html += """            </div>
"""
    
    # Imagens
    if data['all_images']:
        html += """            <div class="section">
                <h2>🖼️ Imagens do Site</h2>
                <div class="image-grid">
"""
        for img in data['all_images'][:12]:  # Primeiras 12
            alt = img['alt'] if img['alt'] else 'Imagem do site'
            html += f'                    <img src="{img["src"]}" alt="{alt}" loading="lazy">\n'
        html += """                </div>
            </div>
"""
    
    # Contato
    html += """            <div class="section">
                <h2>📞 Informações de Contato</h2>
                <div class="contact-info">
"""
    
    if data['contact']['phone']:
        html += '                    <h3>📱 Telefone</h3>\n'
        for phone in data['contact']['phone']:
            html += f'                    <p><a href="tel:{phone.replace(" ", "").replace("-", "")}">{phone}</a></p>\n'
    
    if data['contact']['email']:
        html += '                    <h3>📧 Email</h3>\n'
        for email in data['contact']['email']:
            html += f'                    <p><a href="mailto:{email}">{email}</a></p>\n'
    
    if data['contact']['social_media']:
        html += '                    <h3>🌐 Redes Sociais</h3>\n'
        html += '                    <div class="social-media">\n'
        for social in data['contact']['social_media']:
            html += f'                        <a href="{social["url"]}" target="_blank">{social["network"]}</a>\n'
        html += '                    </div>\n'
    
    html += """                </div>
            </div>
        </div>
        
        <footer>
            <p>{}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Dados extraídos com Scrapling | JSON disponível para recriação do site
            </p>
        </footer>
    </div>
</body>
</html>""".format(data['footer']['text'])
    
    # Salva HTML
    output_path = Path(__file__).parent / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n🌐 Visualizador HTML criado: {output_path}")
    
    return output_path

def main():
    print("=" * 60)
    print("🔧 MELHORAMENTO DE DADOS - VIZZIO ENGENHARIA")
    print("=" * 60)
    
    # Melhora dados
    data, json_file = improve_data()
    
    # Cria visualizador HTML
    html_file = create_html_viewer(data)
    
    print("\n" + "=" * 60)
    print("✅ PROCESSO CONCLUÍDO!")
    print("=" * 60)
    print(f"\n📄 Arquivos gerados:")
    print(f"  • JSON limpo: {json_file}")
    print(f"  • Visualizador: {html_file}")
    print(f"\n💡 Abra o arquivo HTML no navegador para ver os dados!")
    print("=" * 60)

if __name__ == "__main__":
    main()
