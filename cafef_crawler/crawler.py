from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from typing import List, Optional
from models import StockData
import re

class CafeFCrawler:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Setup Chrome driver with anti-detection measures"""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        
        # Anti-detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Additional anti-detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def _parse_float(self, text: str) -> float:
        """Parse number format, handling both 1,234.56 and 1.234,56"""
        if not text or text == '-': return 0.0
        
        # Heuristic: 
        # If ',' and '.' both exist:
        #   If last separator is '.', then ',' is thousand (Eng) -> remove ','
        #   If last separator is ',', then '.' is thousand (VN) -> remove '.' and replace ','
        
        # Simple approach based on observation (English format seems used)
        # Input: 1,802.91 -> 1802.91
        
        try:
            # Check for English format (standard in many frameworks)
            if '.' in text and ',' in text:
                if text.rfind('.') > text.rfind(','):
                    # 1,234.56 format
                    return float(text.replace(',', ''))
                else:
                    # 1.234,56 format
                    return float(text.replace('.', '').replace(',', '.'))
            elif ',' in text and '.' not in text:
                # 1,234 format (integer with comma) or 1,234 (decimal with comma)
                # Hard to distinguish 1,234 (1234) vs 1,234 (1.234) without context
                # Given typical stock data, 1,000 is likely 1000.
                return float(text.replace(',', ''))
            elif '.' in text and ',' not in text:
                 # 1.234 format or 1.234 (1234)
                 # Usually simple float
                 return float(text)
            else:
                 return float(text)
        except ValueError:
            return 0.0

    def crawl_history(self, url: str) -> List[StockData]:
        """Scrape VNINDEX trading history using XPath"""
        results = []
        try:
            print(f"Loading page: {url}")
            self.driver.get(url)
            
            wait = WebDriverWait(self.driver, 20)
            
            # User suggested using: //*[@id="render-table-owner"]
            # This is likely the tbody or container.
            target_xpath = '//*[@id="render-table-owner"]'
            
            print(f"Waiting for element: {target_xpath}")
            wait.until(EC.presence_of_element_located((By.XPATH, target_xpath)))
            
            # Wait for data to render
            time.sleep(3)
            
            # Find rows relative to the container
            # The path provided was //*[@id="render-table-owner"]/tr[1]/td[7]
            # So rows are direct 'tr' children of that element
            rows_xpath = f"{target_xpath}/tr"
            rows = self.driver.find_elements(By.XPATH, rows_xpath)
            
            print(f"Found {len(rows)} data rows")
            
            for row in rows:
                try:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    # If empty row or header row
                    if not cols: continue
                    
                    col_texts = [c.text.strip() for c in cols]
                    
                    # Typical columns map for VNINDEX
                    # 0: Date
                    # 1: Close
                    # 2: Adj Close
                    # 3: Change
                    # 4: % Change
                    # 5: Vol Match
                    # 6: Val Match
                    # 7: Vol Agree
                    # 8: Val Agree
                    # 9: Open
                    # 10: High
                    # 11: Low
                    
                    def get_val(idx):
                        return col_texts[idx] if idx < len(col_texts) else "0"

                    date_str = get_val(0)
                    if not date_str or "Ngày" in date_str: continue

                    stock_data = StockData(
                        date=date_str,
                        close_price=self._parse_float(get_val(1)),
                        adjusted_close_price=self._parse_float(get_val(2)),
                        change_value=self._parse_float(get_val(3)),
                        change_percent=self._parse_float(get_val(4).replace('%', '')),
                        match_volume=int(self._parse_float(get_val(5))),
                        match_value=int(self._parse_float(get_val(6))),
                        negotiated_volume=int(self._parse_float(get_val(7))),
                        negotiated_value=int(self._parse_float(get_val(8))),
                        open_price=self._parse_float(get_val(9)),
                        high_price=self._parse_float(get_val(10)),
                        low_price=self._parse_float(get_val(11))
                    )
                    results.append(stock_data)

                except Exception as e:
                    # print(f"Skipping row: {e}")
                    continue
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error crawling: {e}")
            try:
                print(f"Current Title: {self.driver.title}")
                print("Page Source Snippet:")
                print(self.driver.page_source[:2000])
            except: pass
        finally:
            self.driver.quit()
            
        return results
