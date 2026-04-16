FROM python:3.11-slim

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    git \
    && rm -rf /var/lib/apt/lists/*

# Configure diretório de trabalho
WORKDIR /app

# Copie requirements e instale dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . .

# Exponha a porta do Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para iniciar o Streamlit
ENTRYPOINT ["streamlit", "run", "src/unified_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
