"""
Sistema de Extração de Imagens com OCR e Armazenamento em SQL
Extrai imagens (JPG, PNG, GIF, WebP, BMP, TIFF, ICO, SVG, HEIC, HEIF) de websites,
aplica OCR e salva em banco de dados
"""

import os
import sqlite3
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
from scrapling.fetchers import Fetcher
import tesseract_config  # Configura o caminho do Tesseract
import pytesseract
from PIL import Image
import json
import hashlib

class ImageExtractor:
    """Extrator de imagens com OCR e armazenamento SQL"""
    
    def __init__(self, db_path="data/images_database.db", images_folder="data/extracted_images"):
        self.db_path = db_path
        self.images_folder = Path(images_folder)
        self.images_folder.mkdir(parents=True, exist_ok=True)
        self._setup_database()
    
    def _setup_database(self):
        """Cria o banco de dados e tabelas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela para imagens
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                source_url TEXT NOT NULL,
                domain TEXT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                image_hash TEXT UNIQUE,
                width INTEGER,
                height INTEGER,
                format TEXT,
                size_bytes INTEGER,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Migração: adiciona coluna domain se não existir
        try:
            cursor.execute('ALTER TABLE images ADD COLUMN domain TEXT')
            conn.commit()
        except sqlite3.OperationalError:
            # Coluna já existe
            pass
        
        # Tabela para texto OCR
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocr_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER NOT NULL,
                text_content TEXT,
                confidence REAL,
                language TEXT DEFAULT 'por',
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (image_id) REFERENCES images (id)
            )
        ''')
        
        # Tabela para metadados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extraction_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT NOT NULL,
                images_found INTEGER,
                images_downloaded INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Banco de dados criado: {self.db_path}")
    
    def extract_images_from_url(self, url, download=True, ocr=True, lang='por'):
        """
        Extrai todas as imagens de uma URL
        
        Args:
            url: URL do site
            download: Se deve baixar as imagens
            ocr: Se deve fazer OCR nas imagens
            lang: Idioma do OCR (por, eng, spa, etc)
        
        Returns:
            dict com estatísticas da extração
        """
        print(f"\n🔍 Extraindo imagens de: {url}")
        session_id = self._start_session(url)
        
        # Extrai a página
        page = Fetcher.get(url)
        
        # Encontra todas as imagens
        images = page.css('img')
        print(f"📸 Encontradas {len(images)} imagens")
        
        stats = {
            'total_found': len(images),
            'downloaded': 0,
            'ocr_processed': 0,
            'errors': 0,
            'images': []
        }
        
        for idx, img in enumerate(images, 1):
            try:
                # Pega a URL da imagem
                img_url = img.attrib.get('src') or img.attrib.get('data-src')
                if not img_url:
                    continue
                
                # Converte para URL absoluta
                img_url = urljoin(url, img_url)
                
                # Verifica a extensão da imagem
                ext = self._get_image_extension(img_url)
                if not ext:
                    # Tenta detectar pela URL mesmo sem extensão clara
                    if any(fmt in img_url.lower() for fmt in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg']):
                        # Assume o formato mais comum
                        ext = '.jpg'
                    else:
                        continue
                
                print(f"  [{idx}/{len(images)}] {img_url[:80]}...")
                
                if download:
                    image_data = self._download_image(img_url, url, ext)
                    if image_data:
                        stats['downloaded'] += 1
                        stats['images'].append(image_data)
                        
                        # Só faz OCR em formatos raster (não em SVG, ICO)
                        skip_ocr_formats = ['.svg', '.ico']
                        if ocr and image_data['filepath'] and ext.lower() not in skip_ocr_formats:
                            ocr_text = self._perform_ocr(
                                image_data['filepath'],
                                image_data['id'],
                                lang
                            )
                            if ocr_text:
                                stats['ocr_processed'] += 1
                                image_data['ocr_text'] = ocr_text[:100] + '...' if len(ocr_text) > 100 else ocr_text
            
            except Exception as e:
                print(f"    ❌ Erro: {e}")
                stats['errors'] += 1
        
        self._end_session(session_id, stats)
        
        print(f"\n✅ Extração concluída!")
        print(f"   📥 Baixadas: {stats['downloaded']}")
        print(f"   📝 OCR processados: {stats['ocr_processed']}")
        print(f"   ❌ Erros: {stats['errors']}")
        
        return stats
    
    def _get_domain(self, url):
        """Extrai o domínio da URL"""
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        # Remove www. se existir
        if domain.startswith('www.'):
            domain = domain[4:]
        # Sanitiza para nome de pasta válido
        domain = domain.replace(':', '_').replace('/', '_')
        return domain or 'unknown'
    
    def _get_image_extension(self, url):
        """Retorna a extensão da imagem"""
        path = urlparse(url).path.lower()
        ext = os.path.splitext(path)[1]
        # Formatos suportados: JPG, PNG, GIF, WebP, BMP, TIFF, ICO, SVG
        supported = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', 
                    '.tiff', '.tif', '.ico', '.svg', '.heic', '.heif']
        if ext in supported:
            return ext
        # Se não tem extensão clara, tenta pelo tipo MIME no content-type
        return ''
    
    def _download_image(self, img_url, source_url, ext):
        """Baixa uma imagem e salva no banco de dados"""
        try:
            # Baixa a imagem
            response = requests.get(img_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            # Calcula hash para evitar duplicatas
            img_hash = hashlib.md5(response.content).hexdigest()
            
            # Verifica se já existe
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM images WHERE image_hash = ?', (img_hash,))
            existing = cursor.fetchone()
            
            if existing:
                print(f"    ⏭️  Imagem duplicada, pulando...")
                conn.close()
                return None
            
            # Extrai o domínio e cria subpasta
            domain = self._get_domain(source_url)
            domain_folder = self.images_folder / domain
            domain_folder.mkdir(exist_ok=True)
            
            # Salva a imagem na pasta do domínio
            filename = f"{img_hash}{ext}"
            filepath = domain_folder / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Para SVG e outros formatos vetoriais, não tentamos abrir com PIL
            if ext.lower() in ['.svg']:
                width = 0
                height = 0
                img_format = 'SVG'
                print(f"    ✅ Baixada: {filename} (SVG, {len(response.content)} bytes)")
            else:
                try:
                    # Abre a imagem para pegar metadados
                    img = Image.open(filepath)
                    width, height = img.size
                    img_format = img.format
                    print(f"    ✅ Baixada: {filename} ({width}x{height}, {len(response.content)} bytes)")
                except Exception as e:
                    # Se não conseguir abrir com PIL, salva sem metadados
                    width = 0
                    height = 0
                    img_format = ext.upper().replace('.', '')
                    print(f"    ✅ Baixada: {filename} ({img_format}, {len(response.content)} bytes)")
            
            # Salva no banco de dados
            cursor.execute('''
                INSERT INTO images (url, source_url, domain, filename, filepath, image_hash, 
                                  width, height, format, size_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (img_url, source_url, domain, filename, str(filepath), img_hash,
                  width, height, img_format, len(response.content)))
            
            image_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"    ✅ Baixada: {filename} ({width}x{height}, {len(response.content)} bytes)")
            
            return {
                'id': image_id,
                'url': img_url,
                'filename': filename,
                'filepath': str(filepath),
                'width': width,
                'height': height,
                'size': len(response.content)
            }
        
        except Exception as e:
            print(f"    ❌ Erro ao baixar: {e}")
            return None
    
    def _perform_ocr(self, filepath, image_id, lang='por'):
        """Realiza OCR na imagem"""
        try:
            # Abre a imagem
            img = Image.open(filepath)
            
            # Executa o OCR
            text = pytesseract.image_to_string(img, lang=lang)
            
            # Tenta pegar confiança (opcional)
            try:
                data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
                confidences = [float(c) for c in data['conf'] if c != '-1']
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            except:
                avg_confidence = None
            
            # Salva no banco de dados
            if text.strip():
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO ocr_results (image_id, text_content, confidence, language)
                    VALUES (?, ?, ?, ?)
                ''', (image_id, text.strip(), avg_confidence, lang))
                conn.commit()
                conn.close()
                
                print(f"    📝 OCR: {len(text.strip())} caracteres extraídos")
                return text.strip()
        
        except Exception as e:
            print(f"    ⚠️  OCR falhou: {e}")
            return None
    
    def _start_session(self, url):
        """Inicia uma sessão de extração"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO extraction_sessions (source_url, start_time, status)
            VALUES (?, ?, ?)
        ''', (url, datetime.now(), 'running'))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def _end_session(self, session_id, stats):
        """Finaliza uma sessão de extração"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE extraction_sessions
            SET images_found = ?, images_downloaded = ?, end_time = ?, status = ?
            WHERE id = ?
        ''', (stats['total_found'], stats['downloaded'], datetime.now(), 'completed', session_id))
        conn.commit()
        conn.close()
    
    def search_images(self, search_term=None, min_width=None, min_height=None, limit=None):
        """Busca imagens no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acessar por nome de coluna
        cursor = conn.cursor()
        
        query = '''
            SELECT i.id, i.url, i.source_url, i.domain, i.filename, i.filepath, 
                   i.image_hash, i.width, i.height, i.format, i.size_bytes,
                   i.downloaded_at, o.text_content, o.confidence
            FROM images i
            LEFT JOIN ocr_results o ON i.id = o.image_id
            WHERE 1=1
        '''
        params = []
        
        if search_term:
            query += ' AND o.text_content LIKE ?'
            params.append(f'%{search_term}%')
        
        if min_width:
            query += ' AND i.width >= ?'
            params.append(min_width)
        
        if min_height:
            query += ' AND i.height >= ?'
            params.append(min_height)
        
        query += ' ORDER BY i.downloaded_at DESC'
        
        if limit:
            query += f' LIMIT {int(limit)}'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        # Converte Row objects para dicionários
        return [dict(row) for row in results]
    
    def get_statistics(self):
        """Retorna estatísticas do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total de imagens
        cursor.execute('SELECT COUNT(*) FROM images')
        total_images = cursor.fetchone()[0]
        
        # Total de imagens com OCR
        cursor.execute('SELECT COUNT(*) FROM ocr_results')
        total_ocr = cursor.fetchone()[0]
        
        # Total de sessões
        cursor.execute('SELECT COUNT(*) FROM extraction_sessions')
        total_sessions = cursor.fetchone()[0]
        
        # Tamanho total
        cursor.execute('SELECT SUM(size_bytes) FROM images')
        total_size = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_images': total_images,
            'total_ocr': total_ocr,
            'total_sessions': total_sessions,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }
    
    def get_domains_stats(self):
        """Retorna estatísticas por domínio"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT domain, COUNT(*) as count, SUM(size_bytes) as total_size
            FROM images
            WHERE domain IS NOT NULL
            GROUP BY domain
            ORDER BY count DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'domain': r[0], 'count': r[1], 'size_bytes': r[2]} for r in results]
    
    def export_to_json(self, output_file='images_export.json'):
        """Exporta dados para JSON"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT i.*, o.text_content, o.confidence
            FROM images i
            LEFT JOIN ocr_results o ON i.id = o.image_id
        ''')
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Dados exportados para: {output_file}")
        return output_file


def main():
    """Exemplo de uso"""
    print("=" * 60)
    print("🖼️  EXTRATOR DE IMAGENS COM OCR E SQL")
    print("=" * 60)
    
    # Cria o extrator
    extractor = ImageExtractor()
    
    # Exemplo de URL (você pode mudar)
    url = input("\n📌 Digite a URL para extrair imagens: ").strip()
    if not url:
        url = "https://quotes.toscrape.com"
        print(f"   Usando URL padrão: {url}")
    
    # Pergunta sobre OCR
    do_ocr = input("\n🔤 Fazer OCR nas imagens? (s/n): ").strip().lower() == 's'
    
    if do_ocr:
        lang = input("   Idioma (por/eng/spa): ").strip() or 'por'
    else:
        lang = 'por'
    
    # Extrai imagens
    stats = extractor.extract_images_from_url(url, download=True, ocr=do_ocr, lang=lang)
    
    # Mostra estatísticas
    print("\n" + "=" * 60)
    print("📊 ESTATÍSTICAS DO BANCO DE DADOS")
    print("=" * 60)
    db_stats = extractor.get_statistics()
    for key, value in db_stats.items():
        print(f"   {key}: {value}")
    
    # Pergunta se quer exportar
    export = input("\n💾 Exportar dados para JSON? (s/n): ").strip().lower() == 's'
    if export:
        extractor.export_to_json()
    
    print(f"\n✅ Concluído! Imagens salvas em: {extractor.images_folder}")
    print(f"✅ Banco de dados: {extractor.db_path}")


if __name__ == "__main__":
    main()
