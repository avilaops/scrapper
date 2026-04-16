#!/bin/bash

# Script de Deploy Rápido - Streamlit App
# Execute com: bash deploy.sh

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploy Rápido - Streamlit App${NC}"
echo ""

# Função para menu
show_menu() {
    echo -e "${CYAN}Escolha a opção de deploy:${NC}"
    echo "1. Docker (Local)"
    echo "2. Git Push (para Streamlit Cloud/Heroku/Railway)"
    echo "3. Testar Localmente"
    echo "4. Ver Logs Docker"
    echo "5. Parar Docker"
    echo "6. Sair"
    echo ""
}

while true; do
    show_menu
    read -p "Digite o número da opção: " choice
    
    case $choice in
        1)
            echo -e "\n${YELLOW}📦 Iniciando deploy com Docker...${NC}"
            
            # Verificar se Docker está instalado
            if command -v docker &> /dev/null; then
                echo -e "${GREEN}✅ Docker encontrado!${NC}"
                
                # Build e start
                echo -e "\n🔨 Fazendo build da imagem..."
                docker-compose build
                
                echo -e "\n🚀 Iniciando containers..."
                docker-compose up -d
                
                echo -e "\n${GREEN}✅ Deploy concluído!${NC}"
                echo -e "${CYAN}🌐 Acesse: http://localhost:8501${NC}"
                
                # Mostrar logs
                echo -e "\n📋 Logs (Ctrl+C para sair):"
                docker-compose logs -f
            else
                echo -e "${RED}❌ Docker não encontrado. Instale em: https://www.docker.com/${NC}"
            fi
            ;;
        
        2)
            echo -e "\n${YELLOW}📤 Preparando push para Git...${NC}"
            
            # Verificar se Git está instalado
            if command -v git &> /dev/null; then
                echo -e "${GREEN}✅ Git encontrado!${NC}"
                
                # Status
                echo -e "\n📊 Status atual:"
                git status
                
                # Confirmar
                read -p $'\nDeseja fazer commit e push? (s/n): ' confirm
                
                if [ "$confirm" = "s" ]; then
                    read -p "Digite a mensagem do commit: " message
                    
                    git add .
                    git commit -m "$message"
                    git push
                    
                    echo -e "\n${GREEN}✅ Push concluído!${NC}"
                    echo -e "${CYAN}🌐 Acesse seu dashboard de deploy:${NC}"
                    echo "   - Streamlit Cloud: https://streamlit.io/cloud"
                    echo "   - Heroku: https://dashboard.heroku.com/"
                    echo "   - Railway: https://railway.app/"
                else
                    echo -e "${YELLOW}Operação cancelada.${NC}"
                fi
            else
                echo -e "${RED}❌ Git não encontrado. Instale em: https://git-scm.com/${NC}"
            fi
            ;;
        
        3)
            echo -e "\n${YELLOW}🧪 Testando localmente...${NC}"
            
            # Ativar ambiente virtual se existir
            if [ -f ".venv/bin/activate" ]; then
                echo -e "${GREEN}✅ Ativando ambiente virtual...${NC}"
                source .venv/bin/activate
            fi
            
            echo -e "\n🚀 Iniciando Streamlit..."
            echo -e "${CYAN}🌐 Acesse: http://localhost:8501${NC}"
            echo -e "${YELLOW}⚠️ Pressione Ctrl+C para parar${NC}"
            echo ""
            
            python -m streamlit run src/unified_app.py
            ;;
        
        4)
            echo -e "\n${YELLOW}📋 Logs do Docker...${NC}"
            echo "Pressione Ctrl+C para sair"
            echo ""
            
            docker-compose logs -f
            ;;
        
        5)
            echo -e "\n${YELLOW}🛑 Parando containers Docker...${NC}"
            docker-compose down
            echo -e "${GREEN}✅ Containers parados!${NC}"
            ;;
        
        6)
            echo -e "\n${GREEN}👋 Até logo!${NC}"
            exit 0
            ;;
        
        *)
            echo -e "\n${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    read -p "Pressione Enter para continuar..."
    clear
    
done
