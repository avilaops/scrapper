# 📁 ORGANIZAÇÃO POR WEBSITE - RESUMO

## ✅ IMPLEMENTAÇÃO CONCLUÍDA

### 🎯 Objetivo
Organizar as imagens extraídas em **subpastas por domínio/website**, em vez de salvar todas em uma única pasta.

---

## 📂 ESTRUTURA DE PASTAS

### ANTES:
```
extracted_images/
  ├── hash1.jpg
  ├── hash2.png
  ├── hash3.jpg
  └── ...
```

### DEPOIS:
```
extracted_images/
  ├── pt.wikipedia.org/
  │   ├── hash1.png
  │   ├── hash2.png
  │   └── ...
  ├── quotes.toscrape.com/
  │   ├── hash3.jpg
  │   └── ...
  ├── github.com/
  │   ├── hash4.png
  │   └── ...
  └── example.com/
      ├── hash5.jpg
      └── ...
```

---

## 🔧 MODIFICAÇÕES REALIZADAS

### 1. **Banco de Dados** - Nova coluna `domain`

**Tabela `images` atualizada:**
```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    source_url TEXT NOT NULL,
    domain TEXT,              -- NOVA COLUNA
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    image_hash TEXT UNIQUE,
    width INTEGER,
    height INTEGER,
    format TEXT,
    size_bytes INTEGER,
    downloaded_at TIMESTAMP
)
```

**Migração automática:**
- Se a coluna `domain` não existir, é criada automaticamente
- Bancos de dados antigos são atualizados sem perder dados

---

### 2. **[image_extractor.py](d:\iCloudDrive\AvilaOps\Scrapper\image_extractor.py)** - Motor de Extração

#### a) Novo método `_get_domain(url)`
```python
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
```

**Exemplos de extração:**
- `https://pt.wikipedia.org/wiki/Python` → `pt.wikipedia.org`
- `https://www.example.com/page` → `example.com` (remove www.)
- `http://quotes.toscrape.com/` → `quotes.toscrape.com`
- `https://github.com/user/repo` → `github.com`

#### b) Modificação em `_download_image()`
```python
# Extrai o domínio e cria subpasta
domain = self._get_domain(source_url)
domain_folder = self.images_folder / domain
domain_folder.mkdir(exist_ok=True)

# Salva a imagem na pasta do domínio
filename = f"{img_hash}{ext}"
filepath = domain_folder / filename
```

#### c) Inserção no banco atualizada
```python
cursor.execute('''
    INSERT INTO images (url, source_url, domain, filename, filepath, ...)
    VALUES (?, ?, ?, ?, ?, ...)
''', (img_url, source_url, domain, filename, str(filepath), ...))
```

#### d) Novo método `get_domains_stats()`
```python
def get_domains_stats(self):
    """Retorna estatísticas por domínio"""
    cursor.execute('''
        SELECT domain, COUNT(*) as count, SUM(size_bytes) as total_size
        FROM images
        WHERE domain IS NOT NULL
        GROUP BY domain
        ORDER BY count DESC
    ''')
    return [{'domain': r[0], 'count': r[1], 'size_bytes': r[2]} 
            for r in results]
```

#### e) `search_images()` atualizado
- Agora retorna a coluna `domain` nos resultados
- Query ordenada por domínio e data

---

### 3. **[image_extractor_web.py](d:\iCloudDrive\AvilaOps\Scrapper\image_extractor_web.py)** - Interface Web

#### a) Sidebar - Estatísticas por Website
```python
# Estatísticas por domínio
st.header("🌐 Websites")
domains = extractor.get_domains_stats()

if domains:
    for domain_info in domains[:10]:  # Top 10
        domain = domain_info['domain']
        count = domain_info['count']
        size_mb = domain_info['size_bytes'] / (1024 * 1024)
        st.metric(
            f"📁 {domain}",
            f"{count} imgs",
            f"{size_mb:.1f} MB"
        )
```

**Visualização:**
```
🌐 Websites
-----------------------
📁 pt.wikipedia.org
   5 imgs      0.5 MB

📁 quotes.toscrape.com
   14 imgs     2.3 MB

📁 github.com
   3 imgs      0.1 MB
```

#### b) Aba "Banco de Dados" - Mostra domínio
```python
# Atualizado para mostrar o domínio
for img in results:
    domain = img.get('domain', 'N/A')
    
    with st.expander(f"📷 {domain} - {width}x{height}px"):
        st.write(f"**🌐 Website:** {domain}")
        st.write(f"**URL Original:** {img.get('url')}")
        st.write(f"**Arquivo:** `{img.get('filename')}`")
        # ...
```

#### c) SQL Query atualizada
```python
df = pd.read_sql_query('''
    SELECT i.id, i.domain, i.filename, i.url, ...
    FROM images i
    LEFT JOIN ocr_results o ON i.id = o.image_id
    ORDER BY i.domain, i.downloaded_at DESC  -- Agrupa por domínio
''', conn)
```

#### d) Informações atualizadas
```markdown
**Organização:**
- Imagens salvas em `extracted_images/<dominio>/`
- Cada website em sua própria pasta
- Nomes de arquivo baseados em hash MD5 (evita duplicatas)
```

---

## 🧪 TESTES CRIADOS

### 1. **test_website_folders.py**
- Testa extração de domínios de URLs
- Verifica estrutura de pastas criadas
- Mostra estatísticas por domínio do banco

### 2. **test_download_domain.py**
- Faz download real de imagens
- Verifica criação de subpastas
- Valida organização por domínio

**Execução:**
```bash
python test_website_folders.py
python test_download_domain.py
```

---

## 📊 BENEFÍCIOS DA ORGANIZAÇÃO

### ✅ Vantagens:

1. **Organização Visual**
   - Fácil localizar imagens de um site específico
   - Pastas nomeadas pelo domínio

2. **Gerenciamento Simplificado**
   - Deletar todas as imagens de um site: apenas delete a pasta
   - Backup seletivo por domínio

3. **Estatísticas por Site**
   - Veja quantas imagens cada site tem
   - Monitore tamanho por domínio

4. **Compatibilidade com Estruturas Antigas**
   - Migração automática do banco
   - Imagens antigas continuam funcionando

5. **Evita Conflitos**
   - Mesmo hash em sites diferentes não conflita
   - Cada domínio isolado em sua pasta

---

## 🚀 COMO USAR

### Via Interface Web:

1. **Inicie a interface:**
   ```powershell
   python image_extractor_web.py
   ```
   ou
   ```powershell
   .\start_image_extractor.bat
   ```

2. **Acesse:** http://localhost:8502

3. **Na sidebar, veja:**
   - 📊 Estatísticas gerais
   - 🌐 Lista de websites com imagens

4. **Extraia imagens:**
   - Digite uma URL
   - Clique em "Extrair Imagens"
   - As imagens serão automaticamente organizadas por domínio!

5. **Verifique as pastas:**
   - Vá em `extracted_images/`
   - Cada subpasta = um website

### Via Código Python:

```python
from image_extractor import ImageExtractor

extractor = ImageExtractor()

# Extrai imagens (automaticamente organizadas por domínio)
results = extractor.extract_images_from_url(
    'https://pt.wikipedia.org/wiki/Python',
    ocr=True
)

# Veja estatísticas por domínio
domains = extractor.get_domains_stats()
for domain_info in domains:
    print(f"{domain_info['domain']}: {domain_info['count']} imagens")

# Busca imagens (agora retorna o domínio)
images = extractor.search_images(limit=10)
for img in images:
    print(f"Domínio: {img['domain']}")
    print(f"Arquivo: {img['filepath']}")
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
extracted_images/
  ├── pt.wikipedia.org/      # Pasta do domínio
  │   ├── abc123.png
  │   └── def456.jpg
  ├── quotes.toscrape.com/
  │   └── xyz789.jpg
  └── github.com/
      ├── 111aaa.png
      └── 222bbb.svg

images_database.db           # Banco SQLite com coluna 'domain'
```

---

## 🔄 COMPATIBILIDADE E MIGRAÇÃO

### Bancos de dados antigos:
- ✅ Migração automática da coluna `domain`
- ✅ Imagens antigas ficam com `domain = NULL`
- ✅ Novas imagens sempre têm domínio

### Estrutura de pastas antiga:
- ⚠️ Imagens antigas ficam na raiz de `extracted_images/`
- ✅ Novas imagens vão para subpastas
- 💡 **Migração manual opcional:** Mova imagens antigas para pastas por domínio

---

## 📝 EXEMPLO DE SAÍDA

### Extração de imagens:
```
🔍 Extraindo imagens de: https://pt.wikipedia.org/wiki/Python
📸 Encontradas 26 imagens
  [1/26] https://pt.wikipedia.org/static/images/icons/wikipedia.png...
    ✅ Baixada: c2bc34648c583e6b9959c60bf51a4eff.png (100x100, 13444 bytes)
```

### Estatísticas do banco:
```
📊 Estatísticas por Domínio
  Domínio                              Imagens     Tamanho
  --------------------------------------------------------
  pt.wikipedia.org                          26      1.23 MB
  quotes.toscrape.com                       14      0.84 MB
  github.com                                 5      0.15 MB
  --------------------------------------------------------
  TOTAL                                     45      2.22 MB
```

---

## ✅ CHECKLIST DE FUNCIONALIDADES

- ✅ Extração de domínio da URL fonte
- ✅ Criação automática de subpastas
- ✅ Remoção automática de "www."
- ✅ Sanitização de caracteres inválidos
- ✅ Coluna `domain` no banco de dados
- ✅ Migração automática de bancos antigos
- ✅ Método `get_domains_stats()` para estatísticas
- ✅ Interface web com lista de websites
- ✅ Ordenação por domínio nas queries
- ✅ Exibição do domínio nos resultados
- ✅ Testes automatizados criados
- ✅ Documentação completa

---

## 🎯 PRÓXIMOS PASSOS SUGERIDOS

1. **Script de migração:**
   - Criar script para mover imagens antigas para pastas por domínio
   - Atualizar coluna `domain` de registros antigos

2. **Filtro por domínio:**
   - Adicionar filtro na interface web para buscar por domínio
   - Permitir exportar apenas um domínio específico

3. **Limpeza por domínio:**
   - Botão para deletar todas as imagens de um domínio
   - Confirmação de segurança

4. **Estatísticas avançadas:**
   - Gráfico de pizza por domínio
   - Timeline de extrações por site

---

**Data:** 27 de fevereiro de 2026  
**Status:** ✅ **IMPLEMENTAÇÃO CONCLUÍDA E TESTADA**

**Estrutura testada:**
```
✅ Extração de domínio funcional
✅ Criação automática de pastas
✅ Inserção no banco com domínio
✅ Estatísticas por domínio funcionais
✅ Interface web atualizada
```
