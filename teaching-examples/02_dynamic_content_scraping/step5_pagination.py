"""
Step 5: Pagination - Clicking Next Page
========================================

Goal: Scrape multiple pages by clicking the "Next" button

Concepts:
- Finding and clicking buttons with Selenium
- Waiting for page content to reload
- Detecting when there are no more pages
- Combining data from multiple pages

Try it:
1. Run this file: python step5_pagination.py
2. Watch the browser navigate through pages automatically!
3. See how we collect data from multiple pages

IMPORTANT: This will take longer since it loads multiple pages.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
        return float(text.replace(',', ''))
    except ValueError:
        return 0.0

def scrape_current_page(driver):
    """Scrape data from the current page"""
    results = []
    
    try:
        # Wait for table to be present
        wait = WebDriverWait(driver, 10)
        table_xpath = '//*[@id="render-table-owner"]'
        table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        
        # Give it time to fully render
        time.sleep(2)
        
        # Extract rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        print(f"  Found {len(rows)} rows on this page")
        
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue
                
                cell_texts = [c.text.strip() for c in cells]
                
                # Skip header rows
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
                
            except Exception:
                continue
        
    except Exception as e:
        print(f"  Error scraping page: {e}")
    
    return results

def click_next_page(driver):
    """
    Try to click the 'Next Page' button
    Returns True if successful, False if no more pages
    """
    try:
        # CafeF-specific XPath for the Next button
        next_button_xpath = '//*[@id="divStart"]/div/div[3]/div[3]'
        
        print(f"  Looking for Next button...")
        
        # Try to find the Next button
        try:
            next_button = driver.find_element(By.XPATH, next_button_xpath)
        except NoSuchElementException:
            print("  No Next button found - reached last page")
            return False
        
        # Check if button is disabled or hidden
        if not next_button.is_enabled() or not next_button.is_displayed():
            print("  Next button is disabled - reached last page")
            return False
        
        # Check if button has 'disabled' class
        button_class = next_button.get_attribute("class") or ""
        if "disabled" in button_class.lower():
            print("  Next button is disabled - reached last page")
            return False
        
        # Click the button
        print("  Clicking Next button...")
        next_button.click()
        
        # Wait for page to load
        # Method 1: Simple wait
        time.sleep(3)
        
        # Method 2: Wait for table to refresh (optional - uncomment for more reliability)
        # wait = WebDriverWait(driver, 10)
        # wait.until(EC.staleness_of(driver.find_element(By.XPATH, '//*[@id="render-table-owner"]')))
        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="render-table-owner"]')))
        
        print("  Page loaded successfully")
        return True
        
    except Exception as e:
        print(f"  Error clicking next: {e}")
        return False

def scrape_with_pagination(max_pages=3):
    """Scrape multiple pages by clicking 'Next' button"""
    print("=" * 70)
    print("SELENIUM PAGINATION SCRAPER")
    print(f"Will attempt to scrape up to {max_pages} pages")
    print("=" * 70)
    print()
    
    # Setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    all_data = []
    
    try:
        # Navigate to first page
        url = "https://cafef.vn/du-lieu/Lich-su-giao-dich-vnindex-1.chn"
        print(f"Loading: {url}")
        driver.get(url)
        
        page_num = 1
        
        while page_num <= max_pages:
            print(f"\n--- Page {page_num} ---")
            
            # Scrape current page
            page_data = scrape_current_page(driver)
            all_data.extend(page_data)
            print(f"  Collected {len(page_data)} records from page {page_num}")
            print(f"  Total so far: {len(all_data)} records")
            
            # Try to go to next page
            if page_num < max_pages:
                if not click_next_page(driver):
                    print(f"\n  Stopping - no more pages available")
                    break
            
            page_num += 1
        
        print(f"\n[OK] Scraping complete!")
        print(f"Total pages scraped: {page_num}")
        print(f"Total records collected: {len(all_data)}")
        
    except Exception as e:
        print(f"\n[ERROR] Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        driver.quit()
        print("\nBrowser closed")
    
    return all_data

def main():
    # Scrape data from multiple pages
    data = scrape_with_pagination(max_pages=3)
    
    if not data:
        print("\n[ERROR] No data collected!")
        return
    
    # Save to JSON
    json_file = "vnindex_pagination.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json_data = [d.model_dump() for d in data]
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVED] JSON: {json_file}")
    
    # Save to CSV
    df = pd.DataFrame([d.model_dump() for d in data])
    csv_file = "vnindex_pagination.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"[SAVED] CSV: {csv_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("DATA SUMMARY:")
    print("=" * 70)
    print(f"Total records: {len(data)}")
    print(f"Date range: {data[-1].date} to {data[0].date}")
    print()
    print("First 3 records:")
    print(df.head(3).to_string())
    
    print("\n[COMPLETE] Multi-page scraping successful!")
    print("\nKey Concept: Pagination allows you to scrape large datasets")
    print("            by automatically navigating through pages.")

if __name__ == "__main__":
    main()
