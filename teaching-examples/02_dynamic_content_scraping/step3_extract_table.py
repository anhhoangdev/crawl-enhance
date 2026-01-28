"""
Step 3: Extract Table Data
===========================

Goal: Extract stock data from the table and print it

Concepts:
- XPath selectors
- Table row/cell navigation
- Extracting text from elements
- Basic data cleaning

Try it:
1. Run this file: python step3_extract_table.py
2. See the extracted stock data
3. Notice how we handle missing/empty cells
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("=" * 70)
print("EXTRACTING TABLE DATA WITH XPATH")
print("=" * 70)
print()

# Setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Navigate and wait
    url = "https://cafef.vn/du-lieu/Lich-su-giao-dich-vnindex-1.chn"
    driver.get(url)
    
    wait = WebDriverWait(driver, 20)
    table_xpath = '//*[@id="render-table-owner"]'
    
    print("Waiting for table...")
    table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
    time.sleep(2)
    
    # Find all rows
    rows = table.find_elements(By.TAG_NAME, "tr")
    print(f"Found {len(rows)} rows\n")
    
    print("=" * 70)
    print("EXTRACTED DATA (First 5 rows):")
    print("=" * 70)
    
    # Extract data from each row
    for i, row in enumerate(rows[:5], 1):  # First 5 rows only
        cells = row.find_elements(By.TAG_NAME, "td")
        
        if not cells:
            continue
        
        # Extract text from each cell
        cell_data = [cell.text.strip() for cell in cells]
        
        # CafeF table structure (typical):
        # 0: Date
        # 1: Close Price
        # 2: Adjusted Close
        # 3: Change Value
        # 4: Change %
        # 5-11: Other data (volume, open, high, low, etc.)
        
        print(f"\n--- Row {i} ---")
        if len(cell_data) > 0:
            print(f"Date:        {cell_data[0] if len(cell_data) > 0 else 'N/A'}")
        if len(cell_data) > 1:
            print(f"Close Price: {cell_data[1] if len(cell_data) > 1 else 'N/A'}")
        if len(cell_data) > 9:
            print(f"Open Price:  {cell_data[9] if len(cell_data) > 9 else 'N/A'}")
        if len(cell_data) > 10:
            print(f"High Price:  {cell_data[10] if len(cell_data) > 10 else 'N/A'}")
        if len(cell_data) > 11:
            print(f"Low Price:   {cell_data[11] if len(cell_data) > 11 else 'N/A'}")
    
    print("\n" + "=" * 70)
    print("✅ Successfully extracted data from table!")
    print("=" * 70)
    
    input("\nPress ENTER to close...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()
    print("\n✅ Browser closed!")
    print("Next step: Add Pydantic models and export to JSON/CSV")
