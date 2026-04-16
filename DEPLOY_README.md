# 🚀 Deploy Rápido

## Opções de Deploy

### 1️⃣ Deploy Automático com Scripts

#### Windows (PowerShell):
```powershell
.\deploy.ps1
```

#### Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

**Menu Interativo:**
- ✅ Deploy com Docker local
- ✅ Git push para cloud
- ✅ Teste local
- ✅ Ver logs
- ✅ Gerenciar containers

---

### 2️⃣ Streamlit Cloud (MAIS FÁCIL - GRÁTIS)

**Passo a Passo Rápido:**

1. **Crie repositório no GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

2. **Deploy:**
- Acesse: https://streamlit.io/cloud
- Conecte GitHub
- Selecione seu repositório
- Main file: `src/unified_app.py`
- Deploy!

✅ **Pronto em 2 minutos!**

---

### 3️⃣ Docker (Local ou VPS)

**Iniciar:**
```bash
docker-compose up -d
```

**Ver logs:**
```bash
docker-compose logs -f
```

**Parar:**
```bash
docker-compose down
```

**Acesse:** http://localhost:8501

---

### 4️⃣ Heroku

```bash
# 1. Instale Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Crie app
heroku create seu-app-nome

# 4. Deploy
git push heroku main

# 5. Abra
heroku open
```

---

### 5️⃣ Railway

1. Acesse: https://railway.app/
2. Conecte GitHub
3. Selecione repositório
4. Deploy automático!

---

### 6️⃣ VPS (Servidor Próprio)

Ver guia completo em: [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

---

## 📋 Checklist Pré-Deploy

- [ ] `requirements.txt` atualizado
- [ ] Variáveis sensíveis em `.env` (não commitadas)
- [ ] `.gitignore` configurado
- [ ] Testado localmente
- [ ] Repositório Git criado

---

## 🆘 Problemas Comuns

### Port 8501 em uso:
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <numero> /F

# Linux/Mac
lsof -i :8501
kill -9 <PID>
```

### Tesseract não encontrado:
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-por

# Windows
# Baixe e instale: https://github.com/UB-Mannheim/tesseract/wiki
```

### Dependências faltando:
```bash
pip install -r requirements.txt
```

---

## 📚 Documentação Completa

Para guia detalhado com todas as opções: **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)**

---

## 💡 Recomendação

**Iniciante:** Streamlit Cloud (grátis, fácil)  
**Avançado:** Docker + VPS (controle total)  
**Produção:** Railway/Render (pago, simples)

---

**Boa sorte com o deploy! 🚀**
