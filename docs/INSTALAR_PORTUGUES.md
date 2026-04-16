# 🇧🇷 Instalação do Idioma Português no Tesseract

## ✅ O arquivo foi baixado!

O arquivo `por.traineddata` foi baixado com sucesso para:
- **Temporário**: `%TEMP%\por.traineddata`
- **Backup local**: `D:\iCloudDrive\AvilaOps\Scrapper\tessdata\por.traineddata`

---

## 📋 Para instalar no Tesseract (2 opções):

### **Opção 1: Script Automático (RECOMENDADO)**

1. **Clique direito** em [install_portuguese.bat](install_portuguese.bat)
2. Selecione **"Executar como administrador"**
3. Pronto! O script vai copiar o arquivo para o Tesseract

### **Opção 2: Copiar Manualmente**

1. Abra o **Explorador de Arquivos** como Administrador:
   - Pressione `Win + X`
   - Selecione "Windows PowerShell (Admin)" ou "Terminal (Admin)"
   - Digite: `explorer.exe`

2. Navegue até: `C:\Program Files\Tesseract-OCR\tessdata\`

3. Copie o arquivo de uma dessas localizações:
   - `%TEMP%\por.traineddata` (pasta temporária)
   - `D:\iCloudDrive\AvilaOps\Scrapper\tessdata\por.traineddata` (backup local)

4. Cole em: `C:\Program Files\Tesseract-OCR\tessdata\`

---

## ✔️ Verificar Instalação

Após instalar, execute:

```bash
python test_ocr.py
```

Deve aparecer:
```
✅ Idiomas instalados: eng, osd, por
✅ Todos os idiomas necessários estão instalados
```

---

## 🚀 Usar Português no OCR

Depois de instalado, você pode usar `lang='por'`:

**Na interface web:**
- Idioma: Selecione "por" (português)

**No código Python:**
```python
from image_extractor import ImageExtractor

extractor = ImageExtractor()
stats = extractor.extract_images_from_url(
    "https://example.com",
    ocr=True,
    lang='por'  # ← Português!
)
```

---

## 🌐 Por Enquanto

Você pode usar `lang='eng'` (inglês) que já está instalado e funciona para:
- ✅ Números
- ✅ Datas
- ✅ Textos em inglês
- ✅ Símbolos e códigos

---

## 📱 Outros Idiomas

Se quiser outros idiomas, baixe de:
https://github.com/tesseract-ocr/tessdata/tree/main

Exemplos:
- `spa.traineddata` - Espanhol
- `fra.traineddata` - Francês
- `deu.traineddata` - Alemão
- `ita.traineddata` - Italiano

E copie para: `C:\Program Files\Tesseract-OCR\tessdata\`

---

✨ **O sistema está funcional, mesmo sem português! Use 'eng' por enquanto.**
