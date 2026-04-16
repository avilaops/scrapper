"""
Analisador Científico de Websites
Analisa tecnologias, layout, arquitetura, performance, SEO e estrutura completa
"""

import os
import sqlite3
import requests
import json
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, urljoin
from scrapling.fetchers import Fetcher
from collections import Counter
import hashlib

class WebsiteAnalyzer:
    """Analisador científico completo de websites"""
    
    def __init__(self, db_path="data/website_analysis.db"):
        self.db_path = db_path
        self._setup_database()
    
    def _setup_database(self):
        """Cria banco de dados para armazenar análises"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela principal de análises
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS website_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                domain TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                http_status INTEGER,
                response_time_ms INTEGER,
                page_size_bytes INTEGER,
                
                -- Tecnologias
                technologies TEXT,
                frameworks TEXT,
                cms TEXT,
                server TEXT,
                programming_languages TEXT,
                
                -- HTML
                html_version TEXT,
                total_elements INTEGER,
                semantic_score INTEGER,
                accessibility_score INTEGER,
                
                -- CSS
                css_frameworks TEXT,
                total_stylesheets INTEGER,
                inline_styles INTEGER,
                
                -- JavaScript
                js_frameworks TEXT,
                total_scripts INTEGER,
                total_libraries TEXT,
                
                -- Performance
                total_requests INTEGER,
                load_time_estimate_ms INTEGER,
                total_images INTEGER,
                optimization_score INTEGER,
                
                -- SEO
                meta_title TEXT,
                meta_description TEXT,
                meta_keywords TEXT,
                structured_data TEXT,
                seo_score INTEGER,
                
                -- Segurança
                https_enabled BOOLEAN,
                security_headers TEXT,
                security_score INTEGER,
                
                -- Layout/Design
                color_palette TEXT,
                typography TEXT,
                layout_type TEXT,
                responsive BOOLEAN,
                
                -- Dados brutos
                raw_html_path TEXT,
                full_report_json TEXT
            )
        ''')
        
        # Tabela de elementos HTML
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS html_elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER,
                element_type TEXT,
                count INTEGER,
                attributes TEXT,
                FOREIGN KEY (analysis_id) REFERENCES website_analyses (id)
            )
        ''')
        
        # Tabela de recursos (CSS, JS, imagens)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER,
                resource_type TEXT,
                url TEXT,
                size_bytes INTEGER,
                load_order INTEGER,
                FOREIGN KEY (analysis_id) REFERENCES website_analyses (id)
            )
        ''')
        
        # Tabela de tecnologias detectadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_technologies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER,
                tech_name TEXT,
                tech_category TEXT,
                version TEXT,
                confidence INTEGER,
                detection_method TEXT,
                FOREIGN KEY (analysis_id) REFERENCES website_analyses (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Banco de dados criado: {self.db_path}")
    
    def analyze_website(self, url):
        """
        Análise científica completa de um website
        """
        print(f"\n🔬 ANÁLISE CIENTÍFICA DE WEBSITE")
        print(f"{'='*70}")
        print(f"URL: {url}")
        print(f"{'='*70}\n")
        
        start_time = datetime.now()
        
        # Busca a página
        print("📡 Buscando página...")
        try:
            page = Fetcher.get(url)
            # Scrapling retorna um objeto seletor, precisa pegar o HTML dele
            response_text = str(page)  # Converte para string HTML
            response_time = 0
        except Exception as e:
            print(f"❌ Erro ao buscar página: {e}")
            return None
        
        # Estruturas de análise
        analysis = {
            'url': url,
            'domain': self._get_domain(url),
            'analyzed_at': datetime.now().isoformat(),
            'technologies': {},
            'html_analysis': {},
            'css_analysis': {},
            'js_analysis': {},
            'performance': {},
            'seo': {},
            'security': {},
            'layout': {},
            'resources': []
        }
        
        # 1. ANÁLISE DE TECNOLOGIAS
        print("🔍 1. Detectando tecnologias...")
        analysis['technologies'] = self._detect_technologies(page, response_text)
        
        # 2. ANÁLISE HTML
        print("📄 2. Analisando estrutura HTML...")
        analysis['html_analysis'] = self._analyze_html(page)
        
        # 3. ANÁLISE CSS
        print("🎨 3. Analisando CSS e estilos...")
        analysis['css_analysis'] = self._analyze_css(page)
        
        # 4. ANÁLISE JAVASCRIPT
        print("⚡ 4. Analisando JavaScript...")
        analysis['js_analysis'] = self._analyze_javascript(page)
        
        # 5. ANÁLISE DE PERFORMANCE
        print("⚡ 5. Analisando performance...")
        analysis['performance'] = self._analyze_performance(page, response_text)
        
        # 6. ANÁLISE SEO
        print("📊 6. Analisando SEO...")
        analysis['seo'] = self._analyze_seo(page)
        
        # 7. ANÁLISE DE SEGURANÇA
        print("🔒 7. Analisando segurança...")
        analysis['security'] = self._analyze_security(url, page)
        
        # 8. ANÁLISE DE LAYOUT/DESIGN
        print("🎨 8. Analisando layout e design...")
        analysis['layout'] = self._analyze_layout(page, response_text)
        
        # Salva análise no banco
        analysis_id = self._save_analysis(analysis)
        analysis['id'] = analysis_id
        
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n✅ Análise concluída em {elapsed:.2f}s")
        print(f"📊 ID da análise: {analysis_id}")
        
        return analysis
    
    def _get_domain(self, url):
        """Extrai domínio da URL"""
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain or 'unknown'
    
    def _detect_technologies(self, page, html):
        """Detecta tecnologias, frameworks e bibliotecas"""
        techs = {
            'detected': [],
            'frameworks': [],
            'cms': None,
            'server': None,
            'analytics': [],
            'cdn': []
        }
        
        html_lower = html.lower()
        
        # Detecta frameworks JavaScript
        js_frameworks = {
            'React': ['react', 'reactdom', '_react'],
            'Vue.js': ['vue.js', 'vue.min.js', '__vue__'],
            'Angular': ['angular', 'ng-app', 'ng-controller'],
            'jQuery': ['jquery', '$('],
            'Next.js': ['__next', '_next/static'],
            'Nuxt.js': ['__nuxt', '_nuxt/'],
            'Svelte': ['svelte'],
            'Ember.js': ['ember'],
            'Backbone.js': ['backbone'],
        }
        
        for framework, patterns in js_frameworks.items():
            if any(p in html_lower for p in patterns):
                techs['frameworks'].append(framework)
                techs['detected'].append({
                    'name': framework,
                    'category': 'JavaScript Framework',
                    'confidence': 90
                })
        
        # Detecta CMS
        cms_patterns = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Joomla': ['joomla', 'option=com_'],
            'Drupal': ['drupal', '/sites/default/'],
            'Magento': ['magento', 'mage/cookies'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Wix': ['wix.com', 'static.wixstatic.com'],
            'Squarespace': ['squarespace', 'static1.squarespace.com'],
        }
        
        for cms, patterns in cms_patterns.items():
            if any(p in html_lower for p in patterns):
                techs['cms'] = cms
                techs['detected'].append({
                    'name': cms,
                    'category': 'CMS',
                    'confidence': 95
                })
                break
        
        # Detecta CSS frameworks
        css_frameworks = {
            'Bootstrap': ['bootstrap', 'btn btn-', 'container'],
            'Tailwind CSS': ['tailwind', 'tw-'],
            'Foundation': ['foundation'],
            'Bulma': ['bulma'],
            'Material-UI': ['material-ui', 'mui'],
            'Semantic UI': ['semantic-ui'],
        }
        
        for framework, patterns in css_frameworks.items():
            if any(p in html_lower for p in patterns):
                techs['frameworks'].append(framework)
                techs['detected'].append({
                    'name': framework,
                    'category': 'CSS Framework',
                    'confidence': 85
                })
        
        # Detecta Analytics
        analytics_tools = {
            'Google Analytics': ['google-analytics.com', 'gtag.js', 'ga.js'],
            'Google Tag Manager': ['googletagmanager.com', 'gtm.js'],
            'Facebook Pixel': ['facebook.net', 'fbevents.js'],
            'Hotjar': ['hotjar.com'],
            'Mixpanel': ['mixpanel.com'],
        }
        
        for tool, patterns in analytics_tools.items():
            if any(p in html_lower for p in patterns):
                techs['analytics'].append(tool)
                techs['detected'].append({
                    'name': tool,
                    'category': 'Analytics',
                    'confidence': 95
                })
        
        # Detecta CDN
        cdn_patterns = {
            'Cloudflare': ['cloudflare'],
            'Akamai': ['akamai'],
            'AWS CloudFront': ['cloudfront.net'],
            'Fastly': ['fastly.net'],
        }
        
        for cdn, patterns in cdn_patterns.items():
            if any(p in html_lower for p in patterns):
                techs['cdn'].append(cdn)
        
        return techs
    
    def _analyze_html(self, page):
        """Analisa estrutura HTML"""
        html_analysis = {
            'total_elements': 0,
            'elements_count': {},
            'semantic_elements': 0,
            'semantic_score': 0,
            'accessibility_features': [],
            'accessibility_score': 0,
            'meta_tags': 0,
            'headings_structure': {},
            'forms': 0,
            'tables': 0,
            'lists': 0,
            'links': 0,
            'images': 0,
        }
        
        # Conta elementos
        all_elements = page.css('*')
        html_analysis['total_elements'] = len(all_elements)
        
        # Elementos semânticos HTML5
        semantic_tags = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer', 'figure', 'figcaption']
        for tag in semantic_tags:
            count = len(page.css(tag))
            if count > 0:
                html_analysis['elements_count'][tag] = count
                html_analysis['semantic_elements'] += count
        
        # Score semântico (0-100)
        html_analysis['semantic_score'] = min(100, (html_analysis['semantic_elements'] / max(1, html_analysis['total_elements'] / 10)) * 100)
        
        # Estrutura de headings
        for i in range(1, 7):
            h_count = len(page.css(f'h{i}'))
            if h_count > 0:
                html_analysis['headings_structure'][f'h{i}'] = h_count
        
        # Acessibilidade
        if page.css('[alt]'):
            html_analysis['accessibility_features'].append('Alt text in images')
        if page.css('[aria-label]'):
            html_analysis['accessibility_features'].append('ARIA labels')
        if page.css('[role]'):
            html_analysis['accessibility_features'].append('ARIA roles')
        if page.css('label[for]'):
            html_analysis['accessibility_features'].append('Form labels')
        
        html_analysis['accessibility_score'] = len(html_analysis['accessibility_features']) * 25
        
        # Outros elementos
        html_analysis['forms'] = len(page.css('form'))
        html_analysis['tables'] = len(page.css('table'))
        html_analysis['lists'] = len(page.css('ul, ol'))
        html_analysis['links'] = len(page.css('a'))
        html_analysis['images'] = len(page.css('img'))
        html_analysis['meta_tags'] = len(page.css('meta'))
        
        return html_analysis
    
    def _analyze_css(self, page):
        """Analisa CSS e estilos"""
        css_analysis = {
            'external_stylesheets': 0,
            'inline_styles': 0,
            'style_tags': 0,
            'css_frameworks': [],
            'preprocessors': []
        }
        
        # Conta stylesheets externos
        links = page.css('link[rel="stylesheet"]')
        css_analysis['external_stylesheets'] = len(links)
        
        # Conta estilos inline
        css_analysis['inline_styles'] = len(page.css('[style]'))
        
        # Conta tags style
        css_analysis['style_tags'] = len(page.css('style'))
        
        return css_analysis
    
    def _analyze_javascript(self, page):
        """Analisa JavaScript"""
        js_analysis = {
            'total_scripts': 0,
            'external_scripts': 0,
            'inline_scripts': 0,
            'libraries': [],
            'modules': False,
            'async_scripts': 0,
            'defer_scripts': 0
        }
        
        # Scripts
        scripts = page.css('script')
        js_analysis['total_scripts'] = len(scripts)
        
        for script in scripts:
            src = script.attrib.get('src', '')
            if src:
                js_analysis['external_scripts'] += 1
                
                # Detecta bibliotecas comuns
                src_lower = src.lower()
                if 'jquery' in src_lower:
                    js_analysis['libraries'].append('jQuery')
                if 'react' in src_lower:
                    js_analysis['libraries'].append('React')
                if 'vue' in src_lower:
                    js_analysis['libraries'].append('Vue.js')
                if 'angular' in src_lower:
                    js_analysis['libraries'].append('Angular')
            else:
                js_analysis['inline_scripts'] += 1
            
            # Atributos de carregamento
            if script.attrib.get('async'):
                js_analysis['async_scripts'] += 1
            if script.attrib.get('defer'):
                js_analysis['defer_scripts'] += 1
            if script.attrib.get('type') == 'module':
                js_analysis['modules'] = True
        
        js_analysis['libraries'] = list(set(js_analysis['libraries']))
        
        return js_analysis
    
    def _analyze_performance(self, page, html):
        """Analisa performance"""
        performance = {
            'page_size_bytes': len(html.encode('utf-8')),
            'page_size_kb': round(len(html.encode('utf-8')) / 1024, 2),
            'total_images': len(page.css('img')),
            'total_scripts': len(page.css('script')),
            'total_stylesheets': len(page.css('link[rel="stylesheet"]')),
            'total_resources': 0,
            'optimization_score': 0,
            'recommendations': []
        }
        
        performance['total_resources'] = (
            performance['total_images'] +
            performance['total_scripts'] +
            performance['total_stylesheets']
        )
        
        # Score de otimização
        score = 100
        
        if performance['page_size_kb'] > 1000:
            score -= 20
            performance['recommendations'].append('Página muito grande (>1MB)')
        
        if performance['total_scripts'] > 10:
            score -= 15
            performance['recommendations'].append('Muitos scripts carregados')
        
        if performance['total_images'] > 50:
            score -= 10
            performance['recommendations'].append('Muitas imagens na página')
        
        # Verifica lazy loading
        lazy_images = len(page.css('img[loading="lazy"]'))
        if lazy_images > 0:
            score += 10
            performance['recommendations'].append(f'{lazy_images} imagens com lazy loading ✓')
        
        performance['optimization_score'] = max(0, score)
        
        return performance
    
    def _analyze_seo(self, page):
        """Analisa SEO"""
        seo = {
            'title': '',
            'title_length': 0,
            'meta_description': '',
            'meta_description_length': 0,
            'meta_keywords': '',
            'canonical_url': '',
            'og_tags': {},
            'twitter_cards': {},
            'structured_data': [],
            'h1_count': 0,
            'seo_score': 0,
            'issues': [],
            'recommendations': []
        }
        
        # Title
        title_elem = page.css('title')
        if title_elem:
            seo['title'] = title_elem[0].text.strip()
            seo['title_length'] = len(seo['title'])
        
        # Meta description
        meta_desc = page.css('meta[name="description"]')
        if meta_desc and meta_desc[0].attrib.get('content'):
            seo['meta_description'] = meta_desc[0].attrib.get('content')
            seo['meta_description_length'] = len(seo['meta_description'])
        
        # Meta keywords
        meta_keywords = page.css('meta[name="keywords"]')
        if meta_keywords and meta_keywords[0].attrib.get('content'):
            seo['meta_keywords'] = meta_keywords[0].attrib.get('content')
        
        # Canonical
        canonical = page.css('link[rel="canonical"]')
        if canonical:
            seo['canonical_url'] = canonical[0].attrib.get('href', '')
        
        # Open Graph
        og_tags = page.css('meta[property^="og:"]')
        for tag in og_tags:
            prop = tag.attrib.get('property', '')
            content = tag.attrib.get('content', '')
            seo['og_tags'][prop] = content
        
        # Twitter Cards
        twitter_tags = page.css('meta[name^="twitter:"]')
        for tag in twitter_tags:
            name = tag.attrib.get('name', '')
            content = tag.attrib.get('content', '')
            seo['twitter_cards'][name] = content
        
        # Structured Data (JSON-LD)
        json_ld = page.css('script[type="application/ld+json"]')
        for script in json_ld:
            try:
                data = json.loads(script.text)
                seo['structured_data'].append(data)
            except:
                pass
        
        # H1
        seo['h1_count'] = len(page.css('h1'))
        
        # Calcula score
        score = 0
        
        if seo['title']:
            if 30 <= seo['title_length'] <= 60:
                score += 20
            else:
                seo['issues'].append('Title muito curto ou longo')
        else:
            seo['issues'].append('Sem title tag')
        
        if seo['meta_description']:
            if 120 <= seo['meta_description_length'] <= 160:
                score += 20
            else:
                seo['issues'].append('Meta description fora do tamanho ideal')
        else:
            seo['issues'].append('Sem meta description')
        
        if seo['h1_count'] == 1:
            score += 15
        elif seo['h1_count'] == 0:
            seo['issues'].append('Sem H1')
        else:
            seo['issues'].append('Múltiplos H1')
        
        if seo['canonical_url']:
            score += 10
        
        if seo['og_tags']:
            score += 15
        
        if seo['structured_data']:
            score += 20
        
        seo['seo_score'] = score
        
        return seo
    
    def _analyze_security(self, url, page):
        """Analisa segurança"""
        security = {
            'https_enabled': url.startswith('https'),
            'security_headers': [],
            'forms_with_action': 0,
            'external_resources': 0,
            'security_score': 0,
            'vulnerabilities': []
        }
        
        # HTTPS
        if security['https_enabled']:
            security['security_score'] += 30
        else:
            security['vulnerabilities'].append('Sem HTTPS')
        
        # Forms
        forms = page.css('form')
        for form in forms:
            if form.attrib.get('action'):
                security['forms_with_action'] += 1
        
        # Score final
        security['security_score'] = min(100, security['security_score'])
        
        return security
    
    def _analyze_layout(self, page, response_text):
        """Analisa layout e design"""
        layout = {
            'viewport_meta': False,
            'responsive_indicators': [],
            'grid_system': None,
            'color_scheme': 'light',
            'typography': {},
            'layout_type': 'unknown'
        }
        
        # Viewport
        viewport = page.css('meta[name="viewport"]')
        if viewport:
            layout['viewport_meta'] = True
            layout['responsive_indicators'].append('Viewport meta tag')
        
        # Media queries (aproximação)
        styles = page.css('style')
        for style in styles:
            if '@media' in style.text:
                layout['responsive_indicators'].append('Media queries detected')
                break
        
        # Grid systems
        html = response_text.lower()
        if 'col-' in html or 'grid' in html:
            layout['grid_system'] = 'Grid detected'
        
        # Layout type
        if page.css('header') and page.css('nav') and page.css('main'):
            layout['layout_type'] = 'Semantic HTML5'
        elif page.css('.container') or page.css('.wrapper'):
            layout['layout_type'] = 'Container-based'
        
        return layout
    
    def _save_analysis(self, analysis):
        """Salva análise no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO website_analyses (
                url, domain, technologies, frameworks, cms, server,
                total_elements, semantic_score, accessibility_score,
                total_stylesheets, inline_styles,
                total_scripts, total_libraries,
                page_size_bytes, total_images, optimization_score,
                meta_title, meta_description, seo_score,
                https_enabled, security_score,
                responsive, layout_type, full_report_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis['url'],
            analysis['domain'],
            json.dumps(analysis['technologies']['detected']),
            json.dumps(analysis['technologies']['frameworks']),
            analysis['technologies'].get('cms'),
            analysis['technologies'].get('server'),
            analysis['html_analysis']['total_elements'],
            int(analysis['html_analysis']['semantic_score']),
            analysis['html_analysis']['accessibility_score'],
            analysis['css_analysis']['external_stylesheets'],
            analysis['css_analysis']['inline_styles'],
            analysis['js_analysis']['total_scripts'],
            json.dumps(analysis['js_analysis']['libraries']),
            analysis['performance']['page_size_bytes'],
            analysis['performance']['total_images'],
            analysis['performance']['optimization_score'],
            analysis['seo']['title'],
            analysis['seo']['meta_description'],
            analysis['seo']['seo_score'],
            analysis['security']['https_enabled'],
            analysis['security']['security_score'],
            analysis['layout']['viewport_meta'],
            analysis['layout']['layout_type'],
            json.dumps(analysis, default=str)
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return analysis_id
    
    def get_analysis(self, analysis_id):
        """Recupera análise por ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM website_analyses WHERE id = ?', (analysis_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_all_analyses(self, limit=50):
        """Lista todas as análises"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, domain, analyzed_at, seo_score, 
                   optimization_score, security_score
            FROM website_analyses
            ORDER BY analyzed_at DESC
            LIMIT ?
        ''', (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def export_analysis_json(self, analysis_id, output_file=None):
        """Exporta análise para JSON"""
        analysis = self.get_analysis(analysis_id)
        
        if not analysis:
            print(f"❌ Análise {analysis_id} não encontrada")
            return None
        
        if not output_file:
            domain = analysis['domain']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"analysis_{domain}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Análise exportada: {output_file}")
        return output_file


def main():
    """Exemplo de uso"""
    print("="*70)
    print("🔬 ANALISADOR CIENTÍFICO DE WEBSITES")
    print("="*70)
    
    analyzer = WebsiteAnalyzer()
    
    url = input("\n🌐 Digite a URL para análise científica: ").strip()
    if not url:
        url = "https://example.com"
        print(f"   Usando URL padrão: {url}")
    
    # Analisa
    analysis = analyzer.analyze_website(url)
    
    if analysis:
        # Mostra resumo
        print(f"\n{'='*70}")
        print("📊 RESUMO DA ANÁLISE")
        print(f"{'='*70}")
        
        print(f"\n🔍 TECNOLOGIAS:")
        print(f"  CMS: {analysis['technologies'].get('cms', 'Não detectado')}")
        print(f"  Frameworks: {', '.join(analysis['technologies']['frameworks']) if analysis['technologies']['frameworks'] else 'Nenhum'}")
        
        print(f"\n📄 HTML:")
        print(f"  Total de elementos: {analysis['html_analysis']['total_elements']}")
        print(f"  Score semântico: {analysis['html_analysis']['semantic_score']:.0f}/100")
        print(f"  Score acessibilidade: {analysis['html_analysis']['accessibility_score']}/100")
        
        print(f"\n⚡ PERFORMANCE:")
        print(f"  Tamanho da página: {analysis['performance']['page_size_kb']} KB")
        print(f"  Total de recursos: {analysis['performance']['total_resources']}")
        print(f"  Score de otimização: {analysis['performance']['optimization_score']}/100")
        
        print(f"\n📊 SEO:")
        print(f"  Title: {analysis['seo']['title'][:50]}...")
        print(f"  Score SEO: {analysis['seo']['seo_score']}/100")
        
        print(f"\n🔒 SEGURANÇA:")
        print(f"  HTTPS: {'✓' if analysis['security']['https_enabled'] else '✗'}")
        print(f"  Score: {analysis['security']['security_score']}/100")
        
        # Pergunta se quer exportar
        export = input("\n💾 Exportar análise completa para JSON? (s/n): ").strip().lower()
        if export == 's':
            analyzer.export_analysis_json(analysis['id'])


if __name__ == "__main__":
    main()
