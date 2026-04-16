# 🚀 Guia de Deploy - Aplicação Streamlit

## 📋 Índice
1. [Streamlit Cloud (Recomendado - Grátis)](#streamlit-cloud)
2. [Heroku](#heroku)
3. [Railway](#railway)
4. [Render](#render)
5. [VPS (Servidor Próprio)](#vps-servidor-próprio)
6. [Docker](#docker)

---

## 1️⃣ Streamlit Cloud (Recomendado - Grátis)

### ✅ Vantagens
- **100% Gratuito** para projetos públicos
- Deploy automático via GitHub
- HTTPS configurado automaticamente
- Zero configuração de servidor
- Domínio gratuito: `seu-app.streamlit.app`

### 📝 Passos

#### Passo 1: Preparar o Projeto
```bash
# 1. Crie/atualize o .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore
echo "data/*.db" >> .gitignore
echo ".env" >> .gitignore
```

#### Passo 2: Criar Repositório GitHub
```bash
# Inicialize o Git (se ainda não iniciou)
git init

# Adicione os arquivos
git add .
git commit -m "Initial commit - Streamlit App"

# Crie um repositório no GitHub e conecte
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git branch -M main
git push -u origin main
```

#### Passo 3: Deploy no Streamlit Cloud
1. Acesse: https://streamlit.io/cloud
2. Clique em **"New app"**
3. Conecte sua conta GitHub
4. Selecione:
   - **Repository:** seu repositório
   - **Branch:** main
   - **Main file path:** `src/unified_app.py`
5. Clique em **"Deploy!"**

#### ⚙️ Configurações Adicionais (Opcional)
Crie `.streamlit/config.toml` para customizar:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true
```

---

## 2️⃣ Heroku

### 📝 Arquivos Necessários

**1. Criar `Procfile`:**
```
web: streamlit run src/unified_app.py --server.port=$PORT --server.address=0.0.0.0
```

**2. Criar `setup.sh`:**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

**3. Atualizar `requirements.txt`** (adicionar):
```
streamlit>=1.31.0
```

### 🚀 Deploy
```bash
# 1. Instale Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login no Heroku
heroku login

# 3. Crie o app
heroku create seu-app-nome

# 4. Deploy
git push heroku main

# 5. Abra o app
heroku open
```

---

## 3️⃣ Railway

### ✅ Vantagens
- $5 de crédito grátis por mês
- Deploy automático via GitHub
- Interface moderna e simples

### 📝 Passos
1. Acesse: https://railway.app/
2. Conecte sua conta GitHub
3. Clique em **"New Project"** → **"Deploy from GitHub repo"**
4. Selecione seu repositório
5. Railway detecta automaticamente o Streamlit
6. Configure as variáveis de ambiente (se necessário)
7. Deploy automático!

**Configuração Automática:**
Railway detecta o `requirements.txt` e configura tudo automaticamente.

---

## 4️⃣ Render

### ✅ Vantagens
- Plano gratuito disponível
- Deploy automático via GitHub
- SSL grátis

### 📝 Passos
1. Acesse: https://render.com/
2. Crie uma conta e conecte GitHub
3. Clique em **"New +"** → **"Web Service"**
4. Selecione seu repositório
5. Configure:
   - **Name:** seu-app-nome
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run src/unified_app.py --server.port=$PORT --server.address=0.0.0.0`
6. Clique em **"Create Web Service"**

---

## 5️⃣ VPS (Servidor Próprio)

### 📋 Requisitos
- VPS com Ubuntu/Debian
- Acesso SSH
- Domínio (opcional)

### 📝 Setup Completo

#### 1. Conecte ao Servidor
```bash
ssh usuario@seu-servidor.com
```

#### 2. Instale Dependências
```bash
# Atualize o sistema
sudo apt update && sudo apt upgrade -y

# Instale Python e pip
sudo apt install python3 python3-pip python3-venv -y

# Instale Tesseract (necessário para OCR)
sudo apt install tesseract-ocr tesseract-ocr-por -y

# Instale Nginx (servidor web)
sudo apt install nginx -y
```

#### 3. Configure o Projeto
```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
cd SEU_REPO

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

#### 4. Configure Systemd Service
Crie `/etc/systemd/system/streamlit-app.service`:
```ini
[Unit]
Description=Streamlit App
After=network.target

[Service]
Type=simple
User=seu-usuario
WorkingDirectory=/home/seu-usuario/SEU_REPO
Environment="PATH=/home/seu-usuario/SEU_REPO/venv/bin"
ExecStart=/home/seu-usuario/SEU_REPO/venv/bin/streamlit run src/unified_app.py --server.port=8501 --server.address=localhost

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Ative o serviço
sudo systemctl daemon-reload
sudo systemctl enable streamlit-app
sudo systemctl start streamlit-app

# Verifique status
sudo systemctl status streamlit-app
```

#### 5. Configure Nginx (Proxy Reverso)
Crie `/etc/nginx/sites-available/streamlit-app`:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

```bash
# Ative a configuração
sudo ln -s /etc/nginx/sites-available/streamlit-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. Configure SSL com Let's Encrypt (HTTPS)
```bash
# Instale Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenha certificado SSL
sudo certbot --nginx -d seu-dominio.com

# Teste renovação automática
sudo certbot renew --dry-run
```

---

## 6️⃣ Docker

### 📝 Criar `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instale Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    && rm -rf /var/lib/apt/lists/*

# Copie arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/unified_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 📝 Criar `docker-compose.yml`
```yaml
version: '3.8'

services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### 🚀 Executar
```bash
# Build e executar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

---

## 🔒 Segurança e Boas Práticas

### 1. Variáveis de Ambiente
Nunca commite senhas/chaves. Use `.env`:
```bash
# .env
API_KEY=sua-chave-secreta
DATABASE_URL=sua-url-banco
```

No Streamlit Cloud, adicione em **Settings → Secrets**:
```toml
[secrets]
api_key = "sua-chave-secreta"
database_url = "sua-url-banco"
```

### 2. Ignorar Arquivos Sensíveis
```gitignore
# .gitignore
.env
*.db
__pycache__/
*.pyc
.venv/
data/*.db
.streamlit/secrets.toml
```

### 3. Limitar Uploads
No `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
```

---

## 📊 Monitoramento

### Logs no Streamlit Cloud
- Acesse o dashboard → seu app → **Logs**

### Logs no VPS
```bash
# Ver logs do serviço
sudo journalctl -u streamlit-app -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 🆘 Troubleshooting

### Problema: App não inicia
```bash
# Verifique logs
streamlit run src/unified_app.py --logger.level=debug
```

### Problema: Tesseract não encontrado
```bash
# Linux
sudo apt install tesseract-ocr tesseract-ocr-por

# Ou configure o caminho manualmente no código
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
```

### Problema: Porta em uso
```bash
# Linux
sudo lsof -i :8501
sudo kill -9 PID

# Windows
netstat -ano | findstr :8501
taskkill /PID numero /F
```

---

## 💡 Recomendações Finais

**Para Desenvolvimento/Teste:**
→ Streamlit Cloud (grátis, fácil, rápido)

**Para Produção Leve:**
→ Railway ou Render (pago mas simples)

**Para Produção Profissional:**
→ VPS com Nginx + SSL (controle total)

**Para Escalabilidade:**
→ Docker + Kubernetes (infraestrutura complexa)

---

## 📞 Suporte

- **Streamlit Docs:** https://docs.streamlit.io/
- **Community Forum:** https://discuss.streamlit.io/
- **GitHub Issues:** Para problemas específicos do projeto

---

**Última atualização:** Abril 2026
