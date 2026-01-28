# Level 2: Dynamic Content Scraping

Learn browser automation with **Selenium** to scrape dynamically-loaded content.

---

## 🎯 Learning Objectives

By the end of this level, you will:
- ✅ Automate browsers with Selenium WebDriver
- ✅ Wait for dynamic content to load
- ✅ Use XPath selectors for precise targeting-
- ✅ Extract data from HTML tables
- ✅ Export to both JSON and CSV formats
- ✅ Handle JavaScript-rendered content

---

## 📚 Step-by-Step Guide

### **Step 1: Open Browser** (`step1_open_browser.py`)
Launch Chrome and navigate to the target page.

```bash
python step1_open_browser.py
```

**Key Concepts:**
- Selenium WebDriver setup
- ChromeDriver auto-installation
- Browser navigation
- Manual inspection time

---

### **Step 2: Wait for Elements** (`step2_wait_for_elements.py`)
Wait for dynamic content to load using explicit waits.

```bash
python step2_wait_for_elements.py
```

**Key Concepts:**
- WebDriverWait class
- Expected conditions
- Why waiting is critical
- Finding elements by XPath

---

### **Step 3: Extract Table** (`step3_extract_table.py`)
Extract data from the VNINDEX table.

```bash
python step3_extract_table.py
```

**Key Concepts:**
- XPath selectors
- Table row/cell navigation
- Text extraction
- Handling missing data

---

### **Step 4: Complete Crawler** (`step4_complete_crawler.py`)
Full implementation with Pydantic and export.

```bash
python step4_complete_crawler.py
```

**Key Concepts:**
- Complete scraping workflow
- Pydantic validation
- CSV export with Pandas
- Error handling

**Outputs:**
- `vnindex_data.json`
- `vnindex_data.csv`

---

### **Step 5: Pagination** (`step5_pagination.py`)
Scrape multiple pages by clicking the "Next" button.

```bash
python step5_pagination.py
```

**Key Concepts:**
- Finding and clicking buttons
- Waiting for page reload
- Detecting last page
- Combining data from multiple pages

**Outputs:**
- `vnindex_pagination.json`
- `vnindex_pagination.csv`

**Important:** This demonstrates a key real-world skill - most websites have pagination!

---

## 🛠️ Installation

```bash
pip install -r requirements.txt
```

**Note:** ChromeDriver will auto-download on first run!

---

## 🎓 Exercises

See [`exercises.md`](./exercises.md) for hands-on practice!

---

## 💡 Tips for Live Coding

**For Instructors:**
1. **Step 1**: Keep browser open, show DevTools (F12), inspect table structure
2. **Step 2**: Explain that delays/waits are ESSENTIAL for dynamic content
3. **Step 3**: Show how XPath is more precise than CSS selectors for tables
4. **Step 4**: Demonstrate both JSON and CSV outputs side-by-side

**For Students:**
- Watch the browser! Selenium is visible automation
- Use `time.sleep()` for debugging (see what's happening)
- Inspect elements with DevTools to find XPath
- Don't use headless mode while learning (you want to see it!)

---

## 🔍 When to Use Selenium

✅ **Use Selenium when:**
- Content loads via JavaScript
- Need to interact with the page (clicks, scrolling)
- Data isn't in initial HTML source
- Level 1 (static scraping) doesn't work

❌ **Don't use Selenium when:**
- Static HTML works (Level 1 is faster)
- An API exists (Level 3 is much faster)
- Just need simple data extraction

**Performance Note:** Selenium is slower than requests (opens real browser), but it's necessary for dynamic content!

---

## 🐛 Troubleshooting

### Browser doesn't open
- Check internet connection
- ChromeDriver will auto-install, be patient
- Try manually: `pip install webdriver-manager --upgrade`

### "Element not found" error
- Increase wait timeout (change `20` to `30`)
- Website structure may have changed
- Check XPath is still correct (inspect page)

### Data extraction issues
- Print `cell_texts` to see what's extracted
- Check column indices (they might change)
- Use `try/except` around cell access

---

## 📖 Additional Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- [XPath Cheatsheet](https://devhints.io/xpath)
- [Pandas CSV Guide](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html)

---

## ➡️ Next Level

Ready to get even faster? **[Level 3: API-Based Scraping →](../03_api_based_scraping/)**

Learn how to bypass the browser entirely and hit APIs directly!
