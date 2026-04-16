# 🔍 Scrapper - GitHub Container Registry

## 🐳 Usando a Imagem do GHCR

### Pull e Execute

```bash
# Pull da última versão
docker pull ghcr.io/avilaops/scrapper:latest

# Execute
docker run -p 8501:8501 -v $(pwd)/data:/app/data ghcr.io/avilaops/scrapper:latest

# Acesse: http://localhost:8501
```

### Docker Compose com GHCR

Crie `docker-compose.ghcr.yml`:

```yaml
version: '3.8'

services:
  scrapper:
    image: ghcr.io/avilaops/scrapper:latest
    container_name: scrapper-app
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

Execute:
```bash
docker-compose -f docker-compose.ghcr.yml up -d
```

## 📦 Tags Disponíveis

- `latest` - Última versão da branch main
- `main` - Branch principal
- `v*` - Releases versionadas (ex: v1.0.0)
- `sha-*` - Commits específicos

## 🔒 Autenticação (se imagem privada)

```bash
# Crie um token em: https://github.com/settings/tokens
# Permissões: read:packages

# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u avilaops --password-stdin

# Pull
docker pull ghcr.io/avilaops/scrapper:latest
```

## 🚀 CI/CD Automático

Cada push para `main` automaticamente:
1. Faz build da imagem Docker
2. Testa a imagem
3. Publica no GHCR
4. Gera attestation de segurança

Veja: `.github/workflows/docker-publish.yml`

## 📊 Monitoramento

Veja as imagens publicadas em:
https://github.com/avilaops/scrapper/pkgs/container/scrapper

## 💡 Exemplos de Uso

### Desenvolvimento
```bash
docker run -it --rm -p 8501:8501 ghcr.io/avilaops/scrapper:latest
```

### Produção
```bash
docker run -d \
  --name scrapper-prod \
  -p 8501:8501 \
  -v /var/scrapper/data:/app/data \
  --restart unless-stopped \
  ghcr.io/avilaops/scrapper:latest
```

### Com Docker Swarm
```bash
docker service create \
  --name scrapper \
  --publish 8501:8501 \
  --mount type=volume,source=scrapper-data,target=/app/data \
  --replicas 3 \
  ghcr.io/avilaops/scrapper:latest
```

---

Para mais informações, veja [README.md](README.md) principal.
