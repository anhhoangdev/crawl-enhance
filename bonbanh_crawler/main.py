import json
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from crawler import BonbanhCrawler

def main():
    print("Starting Bonbanh Crawler...")
    crawler = BonbanhCrawler()
    
    # Crawl pages 1 to 2 for a fast demo
    listings = crawler.crawl(start_page=1, end_page=2)
    
    print(f"\nSuccessfully crawled {len(listings)} listings.")
    
    # Save to JSON
    output_file = "bonbanh_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        data = [listing.model_dump() for listing in listings]
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Data saved to {output_file}")
    
    # Print sample data
    if listings:
        print("\nSample Listing:")
        print(listings[0].model_dump_json(indent=2))

if __name__ == "__main__":
    main()
