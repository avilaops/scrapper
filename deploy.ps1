# Script de Deploy Rápido - Streamlit App
# Execute este script para fazer deploy rapidamente

Write-Host "🚀 Deploy Rápido - Streamlit App" -ForegroundColor Green
Write-Host ""

# Função para menu
function Show-Menu {
    Write-Host "Escolha a opção de deploy:" -ForegroundColor Cyan
    Write-Host "1. Docker (Local)"
    Write-Host "2. Git Push (para Streamlit Cloud/Heroku/Railway)"
    Write-Host "3. Testar Localmente"
    Write-Host "4. Ver Logs Docker"
    Write-Host "5. Parar Docker"
    Write-Host "6. Sair"
    Write-Host ""
}

do {
    Show-Menu
    $choice = Read-Host "Digite o número da opção"
    
    switch ($choice) {
        '1' {
            Write-Host "`n📦 Iniciando deploy com Docker..." -ForegroundColor Yellow
            
            # Verificar se Docker está instalado
            if (Get-Command docker -ErrorAction SilentlyContinue) {
                Write-Host "✅ Docker encontrado!" -ForegroundColor Green
                
                # Build e start
                Write-Host "`n🔨 Fazendo build da imagem..."
                docker-compose build
                
                Write-Host "`n🚀 Iniciando containers..."
                docker-compose up -d
                
                Write-Host "`n✅ Deploy concluído!" -ForegroundColor Green
                Write-Host "🌐 Acesse: http://localhost:8501" -ForegroundColor Cyan
                
                # Mostrar logs
                Write-Host "`n📋 Logs (Ctrl+C para sair):"
                docker-compose logs -f
            } else {
                Write-Host "❌ Docker não encontrado. Instale em: https://www.docker.com/" -ForegroundColor Red
            }
        }
        
        '2' {
            Write-Host "`n📤 Preparando push para Git..." -ForegroundColor Yellow
            
            # Verificar se Git está instalado
            if (Get-Command git -ErrorAction SilentlyContinue) {
                Write-Host "✅ Git encontrado!" -ForegroundColor Green
                
                # Status
                Write-Host "`n📊 Status atual:"
                git status
                
                # Confirmar
                $confirm = Read-Host "`nDeseja fazer commit e push? (s/n)"
                
                if ($confirm -eq 's') {
                    $message = Read-Host "Digite a mensagem do commit"
                    
                    git add .
                    git commit -m "$message"
                    git push
                    
                    Write-Host "`n✅ Push concluído!" -ForegroundColor Green
                    Write-Host "🌐 Acesse seu dashboard de deploy:" -ForegroundColor Cyan
                    Write-Host "   - Streamlit Cloud: https://streamlit.io/cloud"
                    Write-Host "   - Heroku: https://dashboard.heroku.com/"
                    Write-Host "   - Railway: https://railway.app/"
                } else {
                    Write-Host "Operação cancelada." -ForegroundColor Yellow
                }
            } else {
                Write-Host "❌ Git não encontrado. Instale em: https://git-scm.com/" -ForegroundColor Red
            }
        }
        
        '3' {
            Write-Host "`n🧪 Testando localmente..." -ForegroundColor Yellow
            
            # Ativar ambiente virtual se existir
            if (Test-Path ".venv\Scripts\Activate.ps1") {
                Write-Host "✅ Ativando ambiente virtual..." -ForegroundColor Green
                & .\.venv\Scripts\Activate.ps1
            }
            
            Write-Host "`n🚀 Iniciando Streamlit..."
            Write-Host "🌐 Acesse: http://localhost:8501" -ForegroundColor Cyan
            Write-Host "⚠️ Pressione Ctrl+C para parar" -ForegroundColor Yellow
            Write-Host ""
            
            python -m streamlit run src/unified_app.py
        }
        
        '4' {
            Write-Host "`n📋 Logs do Docker..." -ForegroundColor Yellow
            Write-Host "Pressione Ctrl+C para sair" -ForegroundColor Gray
            Write-Host ""
            
            docker-compose logs -f
        }
        
        '5' {
            Write-Host "`n🛑 Parando containers Docker..." -ForegroundColor Yellow
            docker-compose down
            Write-Host "✅ Containers parados!" -ForegroundColor Green
        }
        
        '6' {
            Write-Host "`n👋 Até logo!" -ForegroundColor Green
            break
        }
        
        default {
            Write-Host "`n❌ Opção inválida!" -ForegroundColor Red
        }
    }
    
    if ($choice -ne '6') {
        Write-Host "`nPressione qualquer tecla para continuar..."
        $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
        Clear-Host
    }
    
} while ($choice -ne '6')
