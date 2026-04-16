# 🖼️ Guia de Instalação - Extrator de Imagens com OCR

## 📋 Requisitos

### 1. Python e Dependências

```bash
pip install --user -r requirements.txt
```

Isso instalará:
- pytesseract (biblioteca Python para OCR)
- Pillow (processamento de imagens)
- pandas (análise de dados)
- streamlit (interface web)
- scrapling (web scraping)

---

### 2. Tesseract OCR (OBRIGATÓRIO)

O **Tesseract** é o motor de OCR. Você precisa instalá-lo separadamente.

#### 🪟 Windows

**Opção 1: Instalador Oficial**

1. Baixe o instalador: [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
   - Arquivo recomendado: `tesseract-ocr-w64-setup-5.x.x.exe`

2. Execute o instalador
   - ✅ **IMPORTANTE**: Anote o caminho de instalação (geralmente `C:\Program Files\Tesseract-OCR`)
   - ✅ Na instalação, selecione os idiomas adicionais:
     - **Portuguese** (por)
     - **English** (eng) 
     - **Spanish** (spa)

3. Adicione ao PATH do sistema:
   ```
   C:\Program Files\Tesseract-OCR
   ```
   
   Ou configure no Python:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

**Opção 2: Chocolatey**

Se você tem Chocolatey instalado:
```bash
choco install tesseract
```

#### 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-por tesseract-ocr-eng tesseract-ocr-spa
```

#### 🍎 macOS

```bash
brew install tesseract tesseract-lang
```

---

## ✅ Verificar Instalação

### Teste 1: Tesseract no Terminal

```bash
tesseract --version
```

Deve mostrar algo como:
```
tesseract 5.x.x
```

### Teste 2: Python

```bash
python test_ocr.py
```

---

## 🚀 Como Usar

### Opção 1: Interface Web (RECOMENDADO)

```bash
python -m streamlit run image_extractor_web.py
```

Abre em: http://localhost:8502

#### O que você pode fazer:
1. ✅ Extrair imagens de qualquer site
2. ✅ Fazer OCR automático em português/inglês/espanhol
3. ✅ Visualizar imagens no navegador
4. ✅ Buscar imagens por texto OCR
5. ✅ Ver estatísticas e análises
6. ✅ Exportar para JSON/CSV

---

### Opção 2: Script Python

```bash
python image_extractor.py
```

Modo interativo que pergunta:
- URL para extrair
- Se quer fazer OCR
- Idioma do OCR

---

### Opção 3: Usar no Código

```python
from image_extractor import ImageExtractor

# Cria o extrator
extractor = ImageExtractor()

# Extrai imagens de uma URL
stats = extractor.extract_images_from_url(
    "https://example.com",
    download=True,
    ocr=True,
    lang='por'
)

# Busca imagens com texto específico
results = extractor.search_images(search_term="invoice")

# Mostra estatísticas
print(extractor.get_statistics())

# Exporta para JSON
extractor.export_to_json()
```

---

## 📂 Estrutura de Arquivos

Após executar, será criado:

```
Scrapper/
├── extracted_images/          # 🖼️ Imagens baixadas
│   ├── abc123.png
│   ├── def456.jpg
│   └── ...
├── images_database.db         # 💾 Banco SQLite
└── images_export.json         # 📄 Export (opcional)
```

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `images`
Armazena metadados das imagens:
- id, url, source_url, filename, filepath
- width, height, format, size_bytes
- image_hash (para evitar duplicatas)
- downloaded_at

### Tabela: `ocr_results`
Armazena texto extraído por OCR:
- image_id (FK)
- text_content
- confidence (confiança do OCR)
- language
- processed_at

### Tabela: `extraction_sessions`
Histórico de extrações:
- source_url
- images_found, images_downloaded
- start_time, end_time, status

---

## 🔧 Configuração do Tesseract

Se o Tesseract não for encontrado automaticamente, configure manualmente:

### No Windows:

Crie um arquivo `tesseract_config.py`:

```python
import pytesseract

# Configure o caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

E importe no início dos scripts:
```python
import tesseract_config  # Importa a configuração
```

---

## 📝 Idiomas Disponíveis

O Tesseract suporta mais de 100 idiomas. Os principais:

- `por` - Português
- `eng` - Inglês
- `spa` - Espanhol
- `fra` - Francês
- `deu` - Alemão
- `ita` - Italiano
- `jpn` - Japonês
- `chi_sim` - Chinês Simplificado
- `ara` - Árabe

Para instalar novos idiomas no Windows:
1. Baixe arquivos `.traineddata` de: https://github.com/tesseract-ocr/tessdata
2. Coloque em: `C:\Program Files\Tesseract-OCR\tessdata\`

---

## 🆘 Solução de Problemas

### Erro: "tesseract is not installed"

**Solução**: Instale o Tesseract (veja seção 2 acima)

### Erro: "Failed to load language 'por'"

**Solução**: Instale o pacote de idioma português:
- Windows: Reinstale o Tesseract e selecione "Portuguese"
- Linux: `sudo apt install tesseract-ocr-por`

### OCR não extrai nada

**Possíveis causas**:
1. Imagem muito pequena ou de baixa qualidade
2. Texto em idioma diferente do configurado
3. Imagem sem texto

**Solução**: Verifique a imagem e tente outro idioma

### Erro: "Permission denied" ao salvar imagens

**Solução**: Execute com permissões adequadas ou escolha outro diretório

---

## 📊 Exemplos de Uso

### Exemplo 1: Extrair imagens de e-commerce

```python
from image_extractor import ImageExtractor

extractor = ImageExtractor()

# Extrai produtos
stats = extractor.extract_images_from_url(
    "https://example-shop.com/products",
    download=True,
    ocr=False  # Produtos geralmente não têm texto nas imagens
)

print(f"Baixadas {stats['downloaded']} imagens de produtos")
```

### Exemplo 2: Extrair documentos com OCR

```python
extractor = ImageExtractor()

# Extrai documentos
stats = extractor.extract_images_from_url(
    "https://example.com/documents",
    download=True,
    ocr=True,
    lang='por'
)

# Busca por palavra-chave
invoices = extractor.search_images(search_term="fatura")
print(f"Encontradas {len(invoices)} faturas")
```

### Exemplo 3: Análise de imagens grandes

```python
# Busca apenas imagens grandes (> 1000px)
large_images = extractor.search_images(min_width=1000, min_height=1000)

print(f"Encontradas {len(large_images)} imagens grandes")
```

---

## 🎓 Recursos Adicionais

- [Documentação Tesseract](https://tesseract-ocr.github.io/)
- [Documentação PyTesseract](https://pypi.org/project/pytesseract/)
- [Documentação Scrapling](https://scrapling.readthedocs.io/)

---

## ✨ Dicas de Uso

1. **Qualidade do OCR**: Imagens maiores e com boa resolução têm melhor taxa de reconhecimento
2. **Idioma correto**: Sempre use o idioma correto para melhores resultados
3. **Duplicatas**: O sistema detecta automaticamente imagens duplicadas pelo hash MD5
4. **Performance**: Desabilite OCR se não precisar de texto (muito mais rápido)
5. **Backup**: Faça backup regular do arquivo `images_database.db`

---

🎉 **Pronto para extrair imagens!**
