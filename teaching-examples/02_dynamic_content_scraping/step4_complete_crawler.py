"""
Step 4: Complete Crawler with Export
=====================================

Goal: Full crawler with Pydantic validation and CSV/JSON export

Concepts:
- Complete scraping workflow
- Pydantic data validation
- Multiple export formats (JSON + CSV)
- Error handling

Try it:
1. Run this file: python step4_complete_crawler.py
2. Check outputs: vnindex_data.json and vnindex_data.csv
3. Examine the structured data!
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import pandas as pd
from models import StockData

def parse_float(text):
    """Convert text to float, handling various formats"""
    if not text or text == '-':
        return 0.0
    try:
        # Remove commas and convert
        return float(text.replace(',', ''))
    except ValueError:
        return 0.0

def scrape_vnindex():
    """Scrape VNINDEX trading data from CafeF"""
    print("=" * 70)
    print("COMPLETE VNINDEX CRAWLER")
    print("=" * 70)
    print()
    
    # Setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    results = []
    
    try:
        # Navigate
        url = "https://cafef.vn/du-lieu/Lich-su-giao-dich-vnindex-1.chn"
        print(f"Loading: {url}")
        driver.get(url)
        
        # Wait for table
        wait = WebDriverWait(driver, 20)
        table_xpath = '//*[@id="render-table-owner"]'
        print("Waiting for data table...")
        
        table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        time.sleep(2)
        
        # Extract rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        print(f"Found {len(rows)} rows")
        print("Extracting data...\n")
        
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue
                
                cell_texts = [c.text.strip() for c in cells]
                
                # Skip if date is missing or looks like header
                date = cell_texts[0] if len(cell_texts) > 0 else ""
                if not date or "Ngày" in date:
                    continue
                
                # Create StockData model
                stock_data = StockData(
                    date=cell_texts[0] if len(cell_texts) > 0 else "",
                    open_price=parse_float(cell_texts[9] if len(cell_texts) > 9 else "0"),
                    close_price=parse_float(cell_texts[1] if len(cell_texts) > 1 else "0"),
                    high_price=parse_float(cell_texts[10] if len(cell_texts) > 10 else "0"),
                    low_price=parse_float(cell_texts[11] if len(cell_texts) > 11 else "0")
                )
                
                results.append(stock_data)
                
            except Exception as e:
                # Skip invalid rows
                continue
        
        print(f"✅ Successfully extracted {len(results)} trading days\n")
        
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        driver.quit()
        print("Browser closed\n")
    
    return results

def main():
    # Scrape data
    data = scrape_vnindex()
    
    if not data:
        print("❌ No data extracted!")
        return
    
    # Save to JSON
    json_file = "vnindex_data.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json_data = [d.model_dump() for d in data]
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved to: {json_file}")
    
    # Save to CSV using Pandas
    df = pd.DataFrame([d.model_dump() for d in data])
    csv_file = "vnindex_data.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"💾 Saved to: {csv_file}")
    
    # Print sample
    print("\n" + "=" * 70)
    print("SAMPLE DATA (Last 3 days):")
    print("=" * 70)
    print(df.head(3).to_string())
    
    print("\n🎉 Complete! You've built a Selenium web scraper!")

if __name__ == "__main__":
    main()
