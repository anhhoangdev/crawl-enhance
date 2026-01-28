import json
import sys
import os
import pandas as pd
from crawler import CafeFCrawler

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def main():
    print("Starting CafeF VNINDEX Crawler...")
    
    crawler = CafeFCrawler(headless=False)
    
    url = "https://cafef.vn/du-lieu/Lich-su-giao-dich-vnindex-1.chn"
    data = crawler.crawl_history(url)
    
    print(f"\nSuccessfully crawled {len(data)} trading days.")
    
    if data:
        # Save to JSON
        json_file = "vnindex_data.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json_data = [d.model_dump() for d in data]
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"JSON data saved to {json_file}")
        
        # Save to CSV using Pandas
        df = pd.DataFrame([d.model_dump() for d in data])
        csv_file = "vnindex_data.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"CSV data saved to {csv_file}")
        
        # Print sample
        print("\nSample Data (Last 3 days):")
        print(df.head(3))

if __name__ == "__main__":
    main()
