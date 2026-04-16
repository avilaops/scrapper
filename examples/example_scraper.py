"""
Example web scraper using Scrapling
This demonstrates basic and advanced features of the Scrapling library.
"""

from scrapling.fetchers import Fetcher, StealthyFetcher


def basic_scraping_example():
    """Basic HTTP scraping example"""
    print("=== Basic Scraping Example ===")
    
    # Fetch a page with simple HTTP request
    page = Fetcher.get('https://quotes.toscrape.com/')
    
    # Extract quotes using CSS selectors
    quotes = page.css('.quote')
    
    for quote in quotes[:3]:  # Show first 3 quotes
        text = quote.css('.text::text').get()
        author = quote.css('.author::text').get()
        print(f"{author}: {text}")
    
    print(f"\nTotal quotes found: {len(quotes)}\n")


def stealth_scraping_example():
    """Stealth mode scraping example (bypasses anti-bot protection)"""
    print("=== Stealth Scraping Example ===")
    
    # Use StealthyFetcher for sites with anti-bot protection
    # Note: This requires browser dependencies installed via 'scrapling install'
    try:
        page = StealthyFetcher.fetch(
            'https://quotes.toscrape.com/',
            headless=True,
            network_idle=True
        )
        
        quotes = page.css('.quote .text::text').getall()
        print(f"Found {len(quotes)} quotes using stealth mode")
        
    except Exception as e:
        print(f"Note: Stealth mode requires browser setup. Run 'scrapling install' first.")
        print(f"Error: {e}\n")


def advanced_selection_example():
    """Advanced element selection and navigation"""
    print("=== Advanced Selection Example ===")
    
    page = Fetcher.get('https://quotes.toscrape.com/')
    
    # Multiple selection methods
    quotes_css = page.css('.quote')
    quotes_xpath = page.xpath('//div[@class="quote"]')
    quotes_find = page.find_all('div', class_='quote')
    
    print(f"CSS selector found: {len(quotes_css)} quotes")
    print(f"XPath selector found: {len(quotes_xpath)} quotes")
    print(f"find_all method found: {len(quotes_find)} quotes")
    
    # Navigation example
    first_quote = page.css('.quote')[0]
    text = first_quote.css('.text::text').get()
    author = first_quote.css('.author::text').get()
    
    print(f"\nFirst quote: {text}")
    print(f"Author: {author}\n")


def session_example():
    """Session-based scraping for maintaining state"""
    print("=== Session Example ===")
    
    from scrapling.fetchers import FetcherSession
    
    with FetcherSession(impersonate='chrome') as session:
        # Multiple requests in the same session
        page1 = session.get('https://quotes.toscrape.com/')
        page2 = session.get('https://quotes.toscrape.com/page/2/')
        
        quotes_p1 = len(page1.css('.quote'))
        quotes_p2 = len(page2.css('.quote'))
        
        print(f"Page 1 quotes: {quotes_p1}")
        print(f"Page 2 quotes: {quotes_p2}")
        print(f"Total: {quotes_p1 + quotes_p2}\n")


def main():
    """Run all examples"""
    print("Scrapling Example Scripts\n")
    print("=" * 50 + "\n")
    
    try:
        basic_scraping_example()
        advanced_selection_example()
        session_example()
        # stealth_scraping_example()  # Uncomment after running 'scrapling install'
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have installed scrapling:")
        print("  pip install 'scrapling[all]'")
        print("  scrapling install  # For browser dependencies")


if __name__ == "__main__":
    main()
