"""
Script de prueba rápida para verificar que Scrapling funciona correctamente
"""

from scrapling.fetchers import Fetcher

def test_basic_fetch():
    """Prueba básica de scraping HTTP"""
    print("🚀 Probando Scrapling...")
    print("-" * 50)
    
    try:
        # Hacer una petición simple
        page = Fetcher.get('https://quotes.toscrape.com/')
        
        # Extraer título
        title = page.css('title::text').get()
        print(f"✅ Título de la página: {title}")
        
        # Extraer citas
        quotes = page.css('.quote')
        print(f"✅ Encontradas {len(quotes)} citas")
        
        # Mostrar la primera cita
        if quotes:
            first_quote = quotes[0]
            text = first_quote.css('.text::text').get()
            author = first_quote.css('.author::text').get()
            print(f"\n📖 Primera cita:")
            print(f"   {text}")
            print(f"   - {author}")
        
        print("\n✅ ¡Scrapling funciona correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_basic_fetch()
