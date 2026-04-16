"""
Configuração do Tesseract OCR
Este arquivo configura o caminho do Tesseract para os scripts Python
"""

import pytesseract
import os

# Caminho do executável do Tesseract no Windows
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configura o pytesseract para usar este caminho
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    print(f"✅ Tesseract configurado: {TESSERACT_PATH}")
else:
    print(f"⚠️  Tesseract não encontrado em: {TESSERACT_PATH}")
    print("   Por favor, atualize o caminho em tesseract_config.py")
