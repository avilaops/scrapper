# 🌐 Configuração de Domínio Personalizado

## Domínio: scrapper.avilaops.com

### 📋 Configurações DNS Necessárias

Para configurar o domínio `scrapper.avilaops.com`, você precisa adicionar os seguintes registros DNS no seu provedor de domínio:

---

## 🎯 Opção 1: CNAME para Streamlit Cloud

Se estiver usando Streamlit Cloud:

```
Tipo: CNAME
Nome: scrapper
Valor: <seu-app>.streamlit.app
TTL: 3600
```

**Exemplo:**
```
CNAME  scrapper  ->  avilaops-scrapper.streamlit.app
```

---

## 🎯 Opção 2: A Record para VPS/Servidor

Se estiver hospedando em VPS próprio:

```
Tipo: A
Nome: scrapper
Valor: <IP-DO-SEU-SERVIDOR>
TTL: 3600
```

**Exemplo:**
```
A  scrapper  ->  203.0.113.50
```

**Opcional - IPv6:**
```
Tipo: AAAA
Nome: scrapper
Valor: <IPv6-DO-SEU-SERVIDOR>
TTL: 3600
```

---

## 🎯 Opção 3: CNAME para Railway/Render

### Railway:
```
CNAME  scrapper  ->  seu-app.up.railway.app
```

### Render:
```
CNAME  scrapper  ->  seu-app.onrender.com
```

---

## 🔒 SSL/HTTPS Automático

### Streamlit Cloud
- SSL configurado automaticamente
- Aguarde 10-15 minutos após configurar o DNS

### VPS com Nginx
Execute após configurar DNS:

```bash
# Instale Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenha certificado SSL
sudo certbot --nginx -d scrapper.avilaops.com

# Renovação automática já está configurada
sudo certbot renew --dry-run
```

### Railway/Render
- SSL automático incluído
- Aguarde propagação DNS (~5-30 minutos)

---

## 🧪 Verificar Configuração DNS

### Verificar CNAME:
```bash
dig scrapper.avilaops.com CNAME +short
# ou
nslookup scrapper.avilaops.com
```

### Verificar A Record:
```bash
dig scrapper.avilaops.com A +short
```

### Verificar SSL:
```bash
curl -I https://scrapper.avilaops.com
```

---

## ⚙️ Configuração por Plataforma

### 1. Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Vá em **Settings** do seu app
3. Clique em **Custom domain**
4. Digite: `scrapper.avilaops.com`
5. Streamlit mostrará o CNAME necessário
6. Configure no seu DNS:
   ```
   CNAME  scrapper  ->  [valor-mostrado-pelo-streamlit]
   ```
7. Aguarde propagação (10-30 min)

### 2. Nginx no VPS

Atualize `/etc/nginx/sites-available/streamlit-app`:

```nginx
server {
    listen 80;
    server_name scrapper.avilaops.com;

    # Redirecionar HTTP para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name scrapper.avilaops.com;

    # Certificados SSL (após Certbot)
    ssl_certificate /etc/letsencrypt/live/scrapper.avilaops.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/scrapper.avilaops.com/privkey.pem;

    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

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

Reinicie Nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Docker com Traefik (Proxy Reverso)

`docker-compose.production.yml`:

```yaml
version: '3.8'

services:
  scrapper:
    image: ghcr.io/avilaops/scrapper:latest
    networks:
      - web
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.scrapper.rule=Host(`scrapper.avilaops.com`)"
      - "traefik.http.routers.scrapper.entrypoints=websecure"
      - "traefik.http.routers.scrapper.tls.certresolver=letsencrypt"
      - "traefik.http.services.scrapper.loadbalancer.server.port=8501"
    volumes:
      - ./data:/app/data

  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=seu-email@avilaops.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    networks:
      - web

networks:
  web:
    external: true
```

---

## 🚀 Início Rápido

### Para avilaops.com

Adicione no seu DNS (exemplo com Cloudflare/Route53):

```
# CNAME para Streamlit Cloud
Type: CNAME
Name: scrapper
Target: avilaops-scrapper.streamlit.app
Proxy: DNS only (desabilitado) ou Proxied (se Cloudflare)
TTL: Auto

# OU A Record para VPS
Type: A
Name: scrapper
Target: SEU.IP.AQUI
TTL: Auto
```

---

## 🐛 Troubleshooting

### DNS não propaga
```bash
# Limpar cache DNS local
# Windows:
ipconfig /flushdns

# Linux:
sudo systemd-resolve --flush-caches

# Mac:
sudo dscacheutil -flushcache
```

### SSL não funciona
```bash
# Verificar portas abertas
sudo netstat -tlnp | grep -E ':80|:443'

# Verificar Nginx
sudo nginx -t
sudo systemctl status nginx

# Forçar renovação SSL
sudo certbot renew --force-renewal
```

### Streamlit não carrega
1. Verifique se o app está rodando: `docker ps`
2. Veja logs: `docker logs scrapper-app`
3. Teste local: `curl http://localhost:8501/_stcore/health`

---

## 📊 Tempo de Propagação DNS

| Provedor | Tempo Médio |
|----------|-------------|
| Cloudflare | 2-5 min |
| Route53 (AWS) | 1-2 min |
| GoDaddy | 10-30 min |
| Registro.br | 4-8 horas |
| Outros | 24-48 horas |

---

## 🔗 Links Úteis

- [DNS Checker](https://dnschecker.org/)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Certbot Docs](https://certbot.eff.org/)

---

## ✅ Checklist de Configuração

- [ ] DNS configurado (CNAME ou A Record)
- [ ] Propagação DNS verificada (`dig` ou `nslookup`)
- [ ] App acessível via IP/domínio temporário
- [ ] SSL configurado (HTTPS)
- [ ] Redirecionamento HTTP → HTTPS funcionando
- [ ] Domínio personalizado testado no navegador
- [ ] Certificado SSL válido (verificar cadeado verde)

---

**Configuração completa! 🎉**

Acesse: https://scrapper.avilaops.com
