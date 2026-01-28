# Level 2 Exercises: Dynamic Content Scraping

Practice Selenium skills with these exercises!

**Note:** Now that you have step5 (pagination), you can scrape even MORE data!

---

## 🎯 Exercise 1: Change the Wait Timeout

**Difficulty:** ⭐ Easy

**Task:** Modify `step2_wait_for_elements.py` to use a **30-second** timeout instead of 20.

**Steps:**
1. Find the line: `wait = WebDriverWait(driver, 20)`
2. Change `20` to `30`
3. Run and observe

**Hint:** This is useful when the website is slow to load.

**Success Criteria:**
- Script waits up to 30 seconds
- Still works correctly

---

## 🎯 Exercise 2: Extract Change Percentage

**Difficulty:** ⭐⭐ Medium

**Task:** Add a `change_percent` field to extract the daily price change percentage.

**Steps:**
1. Update `models.py` to add: `change_percent: float = 0.0`
2. In `step4_complete_crawler.py`, extract from column index 4
3. Handle the "%" sign (strip it before converting to float)

**Hint:** 
```python
percent_text = cell_texts[4].replace('%', '')
change_percent = parse_float(percent_text)
```

**Success Criteria:**
- Model has new field
- JSON/CSV shows change percentages
- Handles missing values gracefully

---

## 🎯 Exercise 3: Increase Pagination Pages

**Difficulty:** ⭐⭐ Medium

**Task:** Modify `step5_pagination.py` to scrape **5 pages** instead of 3.

**Steps:**
1. Find the line: `data = scrape_with_pagination(max_pages=3)`
2. Change `3` to `5`
3. Run and watch it scrape more pages!

**Success Criteria:**
- Scrapes 5 pages successfully
- Collects ~100 records (20 per page)
- Single combined CSV file

---

## 🎯 Exercise 4: Add Headless Mode Option

**Difficulty:** ⭐⭐ Medium

**Task:** Add an option to run the browser in headless mode (invisible browser).

**Steps:**
1. Import: `from selenium.webdriver.chrome.options import Options`
2. Create options:
   ```python
   options = Options()
   options.add_argument('--headless')
   ```
3. Pass to driver: `driver = webdriver.Chrome(service=service, options=options)`

**Bonus:** Make it configurable via a variable `HEADLESS = True/False`

**Success Criteria:**
- Browser doesn't open visually
- Data still extracts correctly
- Can toggle headless on/off easily

---

## 🎯 Exercise 5: Add Volume Data

**Difficulty:** ⭐⭐⭐ Hard

**Task:** Extract trading volume data (usually in millions).

**Steps:**
1. Inspect the table to find which column has volume
2. Add `volume: int = 0` to the model
3. Extract and parse the value (handle commas and units)
4. Convert to integer

**Hint:** Volume might look like "1,234,567" or "1.23 triệu"

**Success Criteria:**
- Volume field in model
- Correctly parses various formats
- Shows in JSON/CSV output

---

## 🎯 Exercise 6: Smart Pagination Detection

**Difficulty:** ⭐⭐⭐⭐ Very Hard

**Task:** Improve pagination to automatically detect when to stop (no manual max_pages).

**Steps:**
1. In `scrape_with_pagination()`, remove the `max_pages` limit
2. Keep clicking "Next" until the button is disabled or missing
3. Add a safety limit (e.g., max 20 pages) to prevent infinite loops

**Hint:**
```python
page_num = 1
MAX_SAFETY_LIMIT = 20

while page_num <= MAX_SAFETY_LIMIT:
    # Scrape page
    if not click_next_page(driver):
        break  # No more pages
    page_num += 1
```

**Success Criteria:**
- Automatically scrapes all available pages
- Stops when no more "Next" button
- Has safety limit to prevent infinite loops
- Logs how many pages were found

---

## 🏆 Bonus Challenge: Scrape Backwards

**Difficulty:** ⭐⭐⭐⭐ Very Hard

**Task:** Create a scraper that clicks the "Previous" button to go backwards through pages.

**Why?** Sometimes you want the most recent data first, but it's on the last page!

**Steps:**
1. Navigate to the LAST page first (click "Last" or "Next" repeatedly)
2. Scrape the page
3. Click "Previous" to go backwards
4. Stop when you reach page 1

**Success Criteria:**
- Starts from last page
- Goes backwards clicking "Previous"
- Collects data in reverse chronological order

---

## 🧪 Testing Your Solutions

After each exercise:

1. **Visual Check**: Watch the browser in action
2. **Output Files**: Verify JSON/CSV are correct
3. **Data Quality**: Check for missing/incorrect values
4. **Error Handling**: What happens if the network fails?

---

## 💡 Debugging Tips

- Use `input("Paused...")` to freeze and inspect the browser
- Print `cell_texts` to see what's actually extracted
- Check DevTools (F12) to verify XPath selectors
- Use `time.sleep(10)` to slow things down

---

## ✅ Solutions

Solutions available in `/solutions` folder, but try it yourself first! 🚀
