# 🛠️ Interface Unificada - Scrapper Tools

## 📖 Visão Geral

A **Interface Unificada** combina todas as 3 ferramentas do projeto em uma única aplicação Streamlit, facilitando o acesso e navegação entre as diferentes funcionalidades.

## 🚀 Como Iniciar

### Windows

**PowerShell:**
```powershell
.\scripts\start_unified.ps1
```

**CMD:**
```cmd
scripts\start_unified.bat
```

### Acesso
- **URL:** http://localhost:8500
- **Porta:** 8500 (não conflita com as aplicações individuais)

## 📋 Estrutura da Interface

A interface possui **3 abas principais**:

### 🖼️ Aba 1: Extrator de Imagens

**Funcionalidades:**
- Extrair imagens de qualquer URL
- OCR (reconhecimento de texto) automático
- Busca no banco de dados de imagens
- Estatísticas e gráficos de imagens extraídas

**Sub-abas:**
1. **🔍 Extrair** - Extrair novas imagens de sites
2. **📂 Banco de Dados** - Buscar e visualizar imagens já extraídas
3. **📊 Análises** - Estatísticas e gráficos

**Como usar:**
1. Digite a URL do site
2. Marque se deseja fazer OCR
3. Escolha o idioma do OCR (português, inglês, espanhol)
4. Clique em "Extrair Imagens"
5. Visualize as imagens extraídas em grade

### 🕷️ Aba 2: Web Scraper

**Funcionalidades:**
- Scraping de qualquer site usando seletores CSS
- Modo HTTP rápido ou Stealth (anti-bot)
- Exportação em JSON
- Preview de dados extraídos

**Como usar:**
1. Digite a URL do site
2. Digite o seletor CSS (ex: `.quote`, `a::attr(href)`)
3. Escolha o tipo de extração:
   - Todos os elementos
   - Primeiro elemento
   - Texto apenas
   - HTML completo
4. Clique em "Extrair Dados"
5. Baixe os resultados em JSON

**Exemplos de Seletores:**
- `.classe` - Elementos por classe
- `#id` - Elemento por ID
- `tag` - Elementos por tag HTML
- `a::attr(href)` - Atributo href de links
- `::text` - Apenas texto

### 🔬 Aba 3: Analisador de Websites

**Funcionalidades:**
- Análise técnica completa de websites
- Detecção de tecnologias (CMS, frameworks, bibliotecas)
- Scores de SEO, Performance, Segurança e Acessibilidade
- Análise de estrutura HTML e JavaScript

**Como usar:**
1. Digite a URL do site
2. Clique em "Analisar Website"
3. Aguarde a análise (leva alguns segundos)
4. Visualize os resultados em cards organizados

**O que é analisado:**
- ✅ SEO (title, meta description, headings)
- ✅ Performance (tamanho da página, recursos)
- ✅ Segurança (HTTPS, headers)
- ✅ Acessibilidade (elementos semânticos)
- ✅ Tecnologias (CMS, frameworks, analytics)
- ✅ HTML (estrutura, elementos)

## 💡 Vantagens da Interface Unificada

### ✅ Benefícios

1. **Tudo em um lugar**
   - Não precisa abrir 3 janelas/portas diferentes
   - Fácil navegação entre ferramentas

2. **Economia de recursos**
   - Apenas 1 servidor Streamlit rodando
   - Menor uso de memória RAM

3. **Consistência visual**
   - Interface padronizada
   - Mesma aparência em todas as abas

4. **Workflow integrado**
   - Pode usar as 3 ferramentas em sequência
   - Exemplo: Analisar site → Extrair imagens → Fazer scraping

### 📊 Comparação

| Aspecto | Individual | Unificada |
|---------|-----------|-----------|
| **Portas** | 3 portas (8501-8503) | 1 porta (8500) |
| **Janelas** | 3 janelas do navegador | 1 janela com abas |
| **Memória** | ~300-500 MB | ~200-300 MB |
| **Navegação** | Trocar entre abas do navegador | Trocar entre abas na interface |
| **Iniciação** | 3 comandos | 1 comando |

## 🎯 Casos de Uso

### Caso 1: Pesquisa Completa de um Site

```
1. [Aba Analisador] - Analisar o site
   → Identificar tecnologias e estrutura
   
2. [Aba Extrator] - Extrair imagens do site
   → Baixar imagens e fazer OCR
   
3. [Aba Scraper] - Extrair dados específicos
   → Capturar conteúdo com seletores CSS
```

### Caso 2: Monitoramento de Site

```
1. [Aba Scraper] - Extrair dados periodicamente
2. [Aba Extrator] - Monitorar mudanças em imagens
3. [Aba Analisador] - Verificar alterações técnicas
```

### Caso 3: Análise de Conteúdo

```
1. [Aba Extrator] - Extrair todas as imagens
2. [Aba Extrator, Sub-aba Análises] - Ver estatísticas
3. [Aba Extrator, Sub-aba Banco] - Buscar por texto OCR
```

## 🔧 Configurações e Personalizações

### Porta Customizada

Edite o script de inicialização para mudar a porta:

**PowerShell (.ps1):**
```powershell
# Altere a última linha:
python -m streamlit run src/unified_app.py --server.port 9000
```

**CMD (.bat):**
```cmd
REM Altere a última linha:
python -m streamlit run src\unified_app.py --server.port 9000
```

### Desabilitar Ferramentas

Se alguma dependência estiver faltando, a interface automaticamente detecta e mostra um aviso, mas as outras ferramentas continuam funcionando.

**Exemplo:** Se Tesseract não estiver instalado:
- ❌ Extrator de Imagens: não funciona (mostra erro)
- ✅ Web Scraper: funciona normalmente
- ✅ Analisador: funciona normalmente

## 📦 Dependências

A interface unificada requer as mesmas dependências das aplicações individuais:

```bash
pip install -r requirements.txt
```

**Principais pacotes:**
- `streamlit` - Framework da interface web
- `scrapling` - Web scraping
- `pytesseract` - OCR
- `pillow` - Processamento de imagens
- `pandas` - Manipulação de dados
- `plotly` - Gráficos interativos
- `sqlite3` - Banco de dados (built-in no Python)

## 🆘 Troubleshooting

### Problema: Interface não abre

**Solução 1:** Verifique se a porta 8500 está livre
```powershell
# PowerShell
Get-NetTCPConnection -LocalPort 8500
```

**Solução 2:** Use outra porta
```bash
python -m streamlit run src/unified_app.py --server.port 8600
```

### Problema: Módulo não encontrado

**Solução:** Instale as dependências
```bash
pip install -r requirements.txt
```

### Problema: Tesseract não encontrado

A interface mostra um aviso na aba do Extrator, mas as outras abas funcionam.

**Solução:** Instale o Tesseract
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Execute: `scripts\install_portuguese.bat` (para OCR em Português)

### Problema: Scrapling não funciona

**Solução:** Verifique a instalação
```bash
pip install scrapling --upgrade
```

## 📈 Boas Práticas

### 1. Use a interface unificada como padrão
- Mais eficiente e organizado
- Melhor para workflows sequenciais

### 2. Use aplicações individuais quando:
- Precisar rodar vários processos em paralelo
- Quiser dedicar uma janela para monitoramento contínuo
- Estiver desenvolvendo/testando uma ferramenta específica

### 3. Salve seus dados regularmente
- O Extrator salva automaticamente no banco de dados
- O Analisador também salva automaticamente
- O Scraper permite download manual dos resultados

## 🔄 Atalhos e Dicas

### Navegação Rápida
- Use as abas no topo para trocar entre ferramentas
- Use as sub-abas dentro do Extrator para diferentes funções

### Sidebar
- Contém informações contextuais de cada ferramenta
- Mostra status e estatísticas
- Sempre visível para referência rápida

### Downloads
- JSON: Use para processar dados posteriormente
- CSV: Use para abrir no Excel

### Performance
- Limite os resultados mostrados (interface já limita a 20-50 itens)
- Use buscas específicas ao invés de "mostrar tudo"

## 📚 Arquivos Relacionados

- **Código:** [src/unified_app.py](../src/unified_app.py)
- **Scripts:** 
  - [scripts/start_unified.ps1](../scripts/start_unified.ps1)
  - [scripts/start_unified.bat](../scripts/start_unified.bat)
- **Documentação das ferramentas individuais:**
  - [GUIA_INTERFAZ_WEB.md](GUIA_INTERFAZ_WEB.md) - Web Scraper
  - [GUIA_EXTRATOR_IMAGENS.md](GUIA_EXTRATOR_IMAGENS.md) - Extrator
  - [SISTEMAS_ATIVOS.md](SISTEMAS_ATIVOS.md) - Visão geral de todos

## 🎨 Screenshots

### Interface Principal
```
┌─────────────────────────────────────────────┐
│  🛠️ Scrapper Tools - Suite Completa         │
│  Extração de Imagens • Web Scraping • Análise│
├─────────────────────────────────────────────┤
│                                             │
│  [🖼️ Extrator] [🕷️ Scraper] [🔬 Analisador]│
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │                                       │ │
│  │     Conteúdo da aba selecionada      │ │
│  │                                       │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

**💡 Dica Final:** Comece pela interface unificada e descubra qual ferramenta resolve melhor seu problema. Você pode usar todas as 3 em conjunto para análises completas!
