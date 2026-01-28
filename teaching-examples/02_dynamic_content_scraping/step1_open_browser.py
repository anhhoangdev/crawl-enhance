"""
Step 1: Open a Browser with Selenium
=====================================

Goal: Launch Chrome browser and navigate to CafeF

Concepts:
- Selenium WebDriver
- Browser automation basics
- ChromeDriver manager (auto-downloads driver)

Try it:
1. Run this file: python step1_open_browser.py
2. Watch Chrome open automatically!
3. Press Enter when you're done observing the page

Note: The browser will STAY OPEN so you can observe the page structure.
      This is helpful for learning and debugging!
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 70)
print("SELENIUM BROWSER AUTOMATION")
print("=" * 70)
print()

# Setup Chrome driver
print("Setting up Chrome driver...")
print("(First run will download ChromeDriver automatically)")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

print("✅ Browser launched successfully!\n")

# Navigate to CafeF VNINDEX page
url = "https://cafef.vn/du-lieu/Lich-su-giao-dich-vnindex-1.chn"
print(f"Navigating to: {url}")
driver.get(url)

print("✅ Page loaded!\n")
print("=" * 70)
print("OBSERVE THE BROWSER:")
print("=" * 70)
print("1. Notice the browser is controlled by automation")
print("2. The page might have dynamic content loading")
print("3. Look at the table structure")
print("4. Try opening DevTools (F12) to inspect elements")
print()

# Wait for user to observe
input("Press ENTER to close the browser...")

# Clean up
driver.quit()
print("\n✅ Browser closed!")
print("Next step: We'll add waiting for elements to load")
