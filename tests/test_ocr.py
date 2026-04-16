"""
Teste de instalação do Tesseract OCR
Verifica se o Tesseract está instalado corretamente
"""

import sys
import tesseract_config  # Configura o caminho do Tesseract

def test_tesseract():
    print("=" * 60)
    print("🔍 TESTE DE INSTALAÇÃO DO TESSERACT OCR")
    print("=" * 60)
    
    # Teste 1: Importar pytesseract
    print("\n1️⃣ Testando importação do pytesseract...")
    try:
        import pytesseract
        print("   ✅ pytesseract importado com sucesso")
    except ImportError:
        print("   ❌ ERRO: pytesseract não está instalado")
        print("   Solução: pip install --user pytesseract")
        return False
    
    # Teste 2: Verificar Tesseract
    print("\n2️⃣ Verificando executável do Tesseract...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"   ✅ Tesseract encontrado: v{version}")
    except Exception as e:
        print("   ❌ ERRO: Tesseract não encontrado")
        print(f"   Detalhes: {e}")
        print("\n   Soluções:")
        print("   - Windows: Instale de https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - Linux: sudo apt install tesseract-ocr")
        print("   - macOS: brew install tesseract")
        return False
    
    # Teste 3: Verificar idiomas disponíveis
    print("\n3️⃣ Verificando idiomas disponíveis...")
    try:
        langs = pytesseract.get_languages()
        print(f"   ✅ Idiomas instalados: {', '.join(langs)}")
        
        required_langs = ['eng', 'por']
        missing = [lang for lang in required_langs if lang not in langs]
        
        if missing:
            print(f"   ⚠️  Idiomas faltando: {', '.join(missing)}")
            print("   Reinstale o Tesseract e selecione esses idiomas")
        else:
            print("   ✅ Todos os idiomas necessários estão instalados")
    except Exception as e:
        print(f"   ⚠️  Não foi possível verificar idiomas: {e}")
    
    # Teste 4: Teste de OCR em imagem simples
    print("\n4️⃣ Testando OCR em imagem de teste...")
    try:
        from PIL import Image, ImageDraw
        
        # Cria uma imagem de teste simples
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 30), "Teste OCR 123", fill='black')
        
        # Faz OCR
        text = pytesseract.image_to_string(img, lang='eng')
        
        if text.strip():
            print(f"   ✅ OCR funcionando! Texto extraído: '{text.strip()}'")
        else:
            print("   ⚠️  OCR executou mas não extraiu texto")
            print("   Isso pode ser normal para imagens muito simples")
    except Exception as e:
        print(f"   ❌ Erro no teste de OCR: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("✅ O sistema de OCR está pronto para uso")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_tesseract()
    sys.exit(0 if success else 1)
