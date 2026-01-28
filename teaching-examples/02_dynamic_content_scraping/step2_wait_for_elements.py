"""
Step 2: Wait for Dynamic Elements
==================================

Goal: Wait for the data table to load before accessing it

Concepts:
- Explicit waits (WebDriverWait)
- Expected conditions
- Why waiting is important for dynamic content

Try it:
1. Run this file: python step2_wait_for_elements.py
2. See how we wait for specific elements
3. Notice the timeout handling

Dynamic websites load content with JavaScript, so we need to WAIT
for elements to appear before trying to extract data!
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("=" * 70)
print("WAITING FOR DYNAMIC CONTENT")
print("=" * 70)
print()

# Setup driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Navigate
    url = "https://cafef.vn/du-lieu/Lich-su-giao-dich-vnindex-1.chn"
    print(f"Loading: {url}\n")
    driver.get(url)
    
    # Create a wait object (waits up to 20 seconds)
    wait = WebDriverWait(driver, 20)
    
    print("Waiting for table to load...")
    print("(This might take a few seconds)\n")
    
    # Wait for the specific table container using XPath
    # This XPath was found by inspecting the page
    table_xpath = '//*[@id="render-table-owner"]'
    
    # Wait until the element is present in the DOM
    table_element = wait.until(
        EC.presence_of_element_located((By.XPATH, table_xpath))
    )
    
    print("✅ Table found!")
    print(f"Element tag: {table_element.tag_name}")
    
    # Give it a bit more time for data to fully render
    time.sleep(2)
    
    # Find all rows in the table
    rows = table_element.find_elements(By.TAG_NAME, "tr")
    print(f"✅ Found {len(rows)} rows in the table\n")
    
    # Print first row as example
    if rows:
        print("=" * 70)
        print("FIRST ROW PREVIEW:")
        print("=" * 70)
        first_row = rows[0]
        cells = first_row.find_elements(By.TAG_NAME, "td")
        print(f"Number of columns: {len(cells)}")
        if cells:
            print(f"First column: {cells[0].text}")
            print(f"Second column: {cells[1].text}")
    
    input("\nPress ENTER to close...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("- Check your internet connection")
    print("- The website structure might have changed")
    print("- Try increasing the wait timeout")
    
finally:
    driver.quit()
    print("\n✅ Browser closed!")
    print("Next step: Extract data from all rows")
