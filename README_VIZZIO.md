# 🏗️ Dados Extraídos - Vizzio Engenharia

## 📋 Resumo da Extração

✅ **Extração concluída com sucesso!**

Todos os dados do site **Vizzio Engenharia** (https://vizzioengenharia.com.br/) foram extraídos e organizados em formato JSON para facilitar a recriação do site.

---

## 📂 Arquivos Gerados

### 1. **vizzio_engenharia_data.json**
JSON bruto com todos os dados extraídos diretamente do site.

### 2. **vizzio_engenharia_data_clean.json** ⭐ RECOMENDADO
JSON limpo e organizado, pronto para uso. Inclui:
- Menu corrigido (sem HTML)
- Telefone formatado
- Email extraído
- Dados estruturados

### 3. **vizzio_site_viewer.html** 🌐
Visualizador web interativo dos dados extraídos.
**Como usar:** Abra no navegador para ver todos os dados de forma visual.

---

## 📊 O Que Foi Extraído

### ✅ Dados Coletados

| Categoria | Quantidade | Descrição |
|-----------|-----------|-----------|
| **Páginas** | 4 | Início, Projetos, Quem somos, Contato |
| **Imagens** | 17 | Logotipo, ícones, fotos |
| **Seções** | 3 | Missão, Visão, Valores |
| **Links** | 12 | Navegação e externos |
| **Textos** | 6 | Parágrafos de conteúdo |
| **Telefone** | 1 | +55 (17) 99600-3173 (WhatsApp) |
| **Email** | 1 | info@meusite.com |
| **Redes Sociais** | 1 | Instagram |

### 📝 Metadata do Site

```json
{
  "title": "Vizzio Engenharia | Projetos de Engenharia",
  "description": "Vizzio Engenharia - Projetos de Engenharia de forma única e incomparável! Estruturas em Madeira, Concreto armado e Protendido; Fundações; Instalações Hidráulicas e Elétricas. Tudo em BIM e compatibilizado internamente!",
  "url": "https://vizzioengenharia.com.br/"
}
```

### 🗂️ Estrutura do Menu

1. **Início** → https://www.vizzioengenharia.com.br
2. **Projetos** → https://www.vizzioengenharia.com.br/registration
3. **Quem somos** → https://www.vizzioengenharia.com.br/quem-somos
4. **Contato** → https://www.vizzioengenharia.com.br/contato

### 🎯 Seções Principais

- **Missão**
- **Visão**
- **Valores**

### 📞 Contato

- **Telefone/WhatsApp:** +55 (17) 99600-3173
- **Email:** info@meusite.com (pode ser um placeholder)
- **Instagram:** [@vizzioengenharia](https://instagram.com/vizzioengenharia)

---

## 🚀 Como Usar os Dados para Recriar o Site

### Opção 1: Visualizar no Navegador

```bash
# Abra o arquivo HTML
start vizzio_site_viewer.html
# ou
open vizzio_site_viewer.html  # Mac
```

### Opção 2: Usar o JSON Limpo

```python
import json

# Carregar dados
with open('vizzio_engenharia_data_clean.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Acessar informações
title = data['metadata']['title']
description = data['metadata']['description']
menu = data['header']['menu']
images = data['all_images']
contact = data['contact']

# Exemplo: Criar menu HTML
for item in menu:
    print(f'<a href="{item["url"]}">{item["text"]}</a>')
```

### Opção 3: Criar Site com Framework

#### **HTML + CSS + JS**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Vizzio Engenharia</title>
</head>
<body>
    <nav>
        <!-- Use data['header']['menu'] -->
    </nav>
    
    <main>
        <h1>Vizzio Engenharia</h1>
        <p><!-- Use data['metadata']['description'] --></p>
        
        <section>
            <h2>Missão</h2>
            <h2>Visão</h2>
            <h2>Valores</h2>
            <!-- Use data['sections'] -->
        </section>
    </main>
    
    <footer>
        <!-- Use data['footer'] -->
    </footer>
</body>
</html>
```

#### **React**
```jsx
import React from 'react';
import data from './vizzio_engenharia_data_clean.json';

function App() {
  return (
    <div>
      <header>
        <img src={data.header.logo} alt="Logo" />
        <nav>
          {data.header.menu.map((item, i) => (
            <a key={i} href={item.url}>{item.text}</a>
          ))}
        </nav>
      </header>
      
      <main>
        <h1>{data.metadata.title}</h1>
        <p>{data.metadata.description}</p>
        
        {data.sections.map((section, i) => (
          <section key={i}>
            <h2>{section.content}</h2>
          </section>
        ))}
      </main>
      
      <footer>
        <p>{data.footer.text}</p>
      </footer>
    </div>
  );
}

export default App;
```

#### **WordPress (Importar)**
```php
<?php
// Carregar JSON
$json = file_get_contents('vizzio_engenharia_data_clean.json');
$data = json_decode($json, true);

// Criar páginas
$pages = $data['header']['menu'];
foreach ($pages as $page) {
    wp_insert_post([
        'post_title' => $page['text'],
        'post_type' => 'page',
        'post_status' => 'publish'
    ]);
}
?>
```

---

## 🎨 Estrutura do JSON

```json
{
  "metadata": {
    "url": "URL do site",
    "title": "Título da página",
    "description": "Meta description",
    "extracted_at": "Data da extração"
  },
  "header": {
    "logo": "URL do logotipo",
    "menu": [
      {"text": "Nome da página", "url": "Link"}
    ]
  },
  "sections": [
    {"type": "heading_2", "content": "Título da seção"}
  ],
  "contact": {
    "phone": ["Telefones"],
    "email": ["Emails"],
    "social_media": [
      {"network": "Rede social", "url": "Link"}
    ]
  },
  "all_images": [
    {"src": "URL da imagem", "alt": "Texto alternativo"}
  ],
  "all_texts": ["Parágrafos de texto"],
  "footer": {
    "text": "Texto do rodapé",
    "links": [{"text": "Link", "url": "URL"}]
  }
}
```

---

## 🔍 Informações Técnicas

### Site Atual
- **Plataforma:** Wix
- **Domínio:** vizzioengenharia.com.br
- **Status:** Ativo (200 OK)

### Tecnologias Detectadas
- Wix (CMS/hospedagem)
- Imagens via CDN Wix (static.wixstatic.com)
- Design responsivo

### Características
- ✅ HTTPS habilitado
- ✅ Design moderno
- ✅ Imagens otimizadas (AVIF)
- ✅ Integração com WhatsApp
- ✅ Integração com Instagram

---

## 💡 Dicas para Recriação

### 1. **Mantenha a Identidade Visual**
- Use o logotipo extraído
- Mantenha as cores e estilo

### 2. **Estrutura Recomendada**
```
/
├── index.html (Início)
├── projetos.html (Projetos)
├── quem-somos.html (Quem somos)
├── contato.html (Contato)
├── css/
│   └── style.css
├── js/
│   └── main.js
└── images/
    └── (17 imagens extraídas)
```

### 3. **Seções Principais**
- **Hero:** Título + descrição + CTA
- **Sobre:** Missão, Visão, Valores
- **Projetos:** Galeria ou lista
- **Contato:** Formulário + telefone + redes sociais

### 4. **Funcionalidades Essenciais**
- [ ] Menu de navegação
- [ ] Botão WhatsApp flutuante
- [ ] Formulário de contato
- [ ] Galeria de imagens
- [ ] Links para Instagram
- [ ] Footer com copyright

### 5. **SEO**
Use os dados do metadata:
```html
<title>Vizzio Engenharia | Projetos de Engenharia</title>
<meta name="description" content="Vizzio Engenharia - Projetos de Engenharia...">
```

---

## 📱 Integração WhatsApp

O número encontrado está configurado para WhatsApp:

```html
<a href="https://wa.me/5517996003173?text=Excelente%20dia!%20Gostaria%20de%20fazer%20um%20orçamento%20com%20vocês!">
    WhatsApp
</a>
```

---

## 🖼️ Imagens Disponíveis

Todas as 17 imagens foram catalogadas no JSON com:
- URL completa
- Texto alternativo (quando disponível)
- Tipo/categoria

**Para baixar imagens:**
```python
import requests
from pathlib import Path

# Carregar JSON
with open('vizzio_engenharia_data_clean.json', 'r') as f:
    data = json.load(f)

# Baixar imagens
images_dir = Path('images')
images_dir.mkdir(exist_ok=True)

for i, img in enumerate(data['all_images']):
    url = img['src']
    response = requests.get(url)
    
    # Salvar
    filename = f"image_{i+1}.jpg"
    with open(images_dir / filename, 'wb') as f:
        f.write(response.content)
```

---

## ✅ Checklist de Recriação

- [ ] Baixar todas as imagens
- [ ] Criar estrutura de páginas (4 páginas)
- [ ] Implementar menu de navegação
- [ ] Adicionar seções de Missão/Visão/Valores
- [ ] Configurar formulário de contato
- [ ] Adicionar botão WhatsApp
- [ ] Integrar Instagram
- [ ] Adicionar footer com copyright
- [ ] Otimizar para mobile
- [ ] Adicionar SEO (title, description)
- [ ] Testar todos os links

---

## 🆘 Ajuda e Suporte

### Precisa de mais dados?

Execute novamente o script de extração:
```bash
python extract_vizzio.py
```

### Quer extrair dados adicionais?

Edite o script `extract_vizzio.py` e adicione novos seletores CSS.

### Problemas?

- Verifique se o site está online
- Confira se as URLs no JSON estão acessíveis
- Entre em contato com o proprietário do site original

---

## 📦 Arquivos Incluídos

```
vizzio_extraction/
├── README_VIZZIO.md                      ⭐ Este arquivo
├── extract_vizzio.py                     📜 Script de extração
├── improve_vizzio_data.py                🔧 Script de limpeza
├── vizzio_engenharia_data.json           📄 JSON bruto
├── vizzio_engenharia_data_clean.json     📄 JSON limpo (USE ESTE!)
└── vizzio_site_viewer.html               🌐 Visualizador web
```

---

## 🎉 Conclusão

Você agora tem **todos os dados necessários** para recriar o site da Vizzio Engenharia!

- ✅ Estrutura completa mapeada
- ✅ Conteúdo textual extraído
- ✅ Imagens catalogadas
- ✅ Informações de contato coletadas
- ✅ Menu e navegação prontos

**Próximos passos:**
1. Abra o `vizzio_site_viewer.html` para visualizar os dados
2. Use o `vizzio_engenharia_data_clean.json` como base
3. Escolha sua tecnologia (HTML, React, WordPress, etc.)
4. Recrie a estrutura usando os dados extraídos

**Boa sorte! 🚀**

---

*Dados extraídos em: 2026-03-09 | Scrapling v1.0*
