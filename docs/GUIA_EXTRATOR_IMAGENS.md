# 🖼️ Guia Rápido - Extrator de Imagens com OCR

## 🎯 O que faz?

Este sistema:
1. **Acessa** qualquer site que você especificar
2. **Extrai** todas as imagens PNG e JPG
3. **Baixa** as imagens para seu computador
4. **Faz OCR** (extração de texto) das imagens
5. **Salva** tudo em um banco de dados SQLite
6. **Permite buscar** imagens por texto, tamanho, etc.

---

## ⚡ Início Rápido

### Passo 1: Instalar o Tesseract (APENAS UMA VEZ)

**Windows:**
1. Baixe: https://github.com/UB-Mannheim/tesseract/wiki
2. Execute o instalador `tesseract-ocr-w64-setup-x.x.x.exe`
3. **IMPORTANTE**: Marque para instalar idioma **Portuguese**
4. Anote o caminho (geralmente `C:\Program Files\Tesseract-OCR`)

### Passo 2: Testar

```bash
python test_ocr.py
```

Se aparecer ✅ tudo OK, prossiga!

Se aparecer ❌ erro, veja [INSTALACAO_OCR.md](INSTALACAO_OCR.md)

### Passo 3: Usar!

**Interface Web (RECOMENDADO):**
```bash
.\start_image_extractor.bat
```

Abre em: http://localhost:8502

**Ou via Script:**
```bash
python image_extractor.py
```

---

## 🌐 Usando a Interface Web

### 1. Extrair Imagens

1. Abra: http://localhost:8502
2. Aba "🔍 Extrair Imagens"
3. Digite a URL (ex: `https://example.com`)
4. Marque "Fazer OCR" se quiser extrair texto
5. Escolha o idioma: Português (por), Inglês (eng), etc.
6. Click "🚀 Extrair Imagens"

**Resultado:**
- Imagens baixadas em `extracted_images/`
- Dados salvos em `images_database.db`
- Texto OCR extraído automaticamente

### 2. Buscar no Banco de Dados

1. Aba "📂 Banco de Dados"
2. Digite palavras-chave para buscar no texto OCR
3. Ou filtre por largura/altura mínima
4. Click "🔍 Buscar"

**Exemplo:** Buscar "invoice" encontra todas as imagens com faturas

### 3. Ver Estatísticas

- Aba "📊 Análises"
- Veja distribuição por formato, tamanho
- Histórico de extrações
- Imagens com mais texto OCR

---

## 💻 Usando via Código Python

```python
from image_extractor import ImageExtractor

# Criar extrator
extractor = ImageExtractor()

# Extrair imagens de um site
stats = extractor.extract_images_from_url(
    "https://example.com/products",
    download=True,  # Baixar imagens
    ocr=True,       # Fazer OCR
    lang='por'      # Idioma português
)

# Ver resultado
print(f"Baixadas: {stats['downloaded']} imagens")
print(f"OCR: {stats['ocr_processed']} processados")

# Buscar imagens com texto específico
results = extractor.search_images(search_term="produto")
print(f"Encontradas {len(results)} imagens com 'produto'")

# Buscar imagens grandes
big_images = extractor.search_images(min_width=1000)

# Ver estatísticas
stats = extractor.get_statistics()
print(stats)

# Exportar tudo para JSON
extractor.export_to_json("meus_dados.json")
```

---

## 📊 Estrutura do Banco de Dados

### Tabela `images`
Armazena informações sobre cada imagem:
- URL original
- Site de origem
- Nome do arquivo
- Dimensões (largura x altura)
- Formato (PNG, JPG)
- Tamanho em bytes
- Hash MD5 (evita duplicatas)

### Tabela `ocr_results`
Texto extraído de cada imagem:
- Texto completo
- Confiança do OCR (%)
- Idioma usado
- Data de processamento

### Tabela `extraction_sessions`
Histórico de extrações:
- URL acessada
- Quantas imagens encontradas
- Quantas baixadas
- Horário de início/fim

---

## 📁 Onde ficam os Arquivos?

```
D:\iCloudDrive\AvilaOps\Scrapper\
├── extracted_images/      ← 🖼️ Suas imagens aqui
│   ├── abc123.png
│   ├── def456.jpg
│   └── ...
│
├── images_database.db     ← 💾 Banco de dados SQLite
└── images_export.json     ← 📄 Export (se você exportar)
```

---

## 🎯 Casos de Uso

### 1. E-commerce - Baixar produtos

```python
extractor.extract_images_from_url(
    "https://loja.com/produtos",
    download=True,
    ocr=False  # Produtos geralmente não têm texto
)
```

### 2. Documentos - Extrair faturas

```python
extractor.extract_images_from_url(
    "https://portal.com/faturas",
    download=True,
    ocr=True,
    lang='por'
)

# Depois buscar
faturas = extractor.search_images(search_term="R$")
```

### 3. Memes - Extrair texto

```python
extractor.extract_images_from_url(
    "https://site-de-memes.com",
    download=True,
    ocr=True,
    lang='por'
)

# Buscar memes específicos
memes = extractor.search_images(search_term="stonks")
```

---

## 🔧 Configurar Tesseract Manualmente

Se o OCR não funcionar, adicione no início dos seus scripts:

```python
import pytesseract

# Windows - Configure o caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 💾 Exportar Dados

### Via Interface Web:
- Sidebar → "💾 Exportar para JSON"

### Via Código:
```python
extractor.export_to_json('meus_dados.json')
```

### Via SQL direto:
```python
import sqlite3

conn = sqlite3.connect('images_database.db')
cursor = conn.cursor()

# Busca customizada
cursor.execute('''
    SELECT i.filename, o.text_content
    FROM images i
    JOIN ocr_results o ON i.id = o.image_id
    WHERE o.text_content LIKE '%total%'
''')

results = cursor.fetchall()
conn.close()
```

---

## ❓ FAQ

**P: O OCR não está funcionando**
R: Verifique se o Tesseract está instalado: `python test_ocr.py`

**P: OCR não reconhece nada**
R: Verifique se escolheu o idioma correto (por/eng/spa)

**P: Imagens duplicadas**
R: O sistema detecta automaticamente pelo hash MD5 e pula

**P: Como apagar o banco de dados?**
R: Delete o arquivo `images_database.db`

**P: Como ver o banco de dados?**
R: Use DB Browser for SQLite ou a interface web

---

## 🎓 Próximos Passos

1. ✅ Teste com `python test_ocr.py`
2. ✅ Inicie a interface: `.\start_image_extractor.bat`
3. ✅ Extraia imagens de sites
4. ✅ Explore o banco de dados
5. ✅ Exporte seus dados

**Guia completo:** [INSTALACAO_OCR.md](INSTALACAO_OCR.md)

---

## 🆘 Precisa de Ajuda?

- Ver logs de erro na interface web
- Executar `python test_ocr.py` para diagnóstico
- Ler [INSTALACAO_OCR.md](INSTALACAO_OCR.md) para detalhes

---

🎉 **Pronto para extrair e organizar imagens!**
