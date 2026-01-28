# Level 1 Exercises: Static HTML Scraping

Practice what you've learned with these exercises.

---

## Exercise 1: Scrape Page 2

Difficulty: Easy

Task: Modify step4_with_models.py to scrape page 2 instead of page 1.

**Hint:** Look at the `url` variable in the `fetch_car_listings()` function.

**Success Criteria:**
- Your script fetches page 2
- You get different car listings than page 1
- Output file is saved correctly

---

## 🎯 Exercise 2: Extract Origin Field

**Difficulty:** ⭐⭐ Medium

**Task:** Add a new field `origin` to extract whether the car is "Nhập khẩu" (imported) or "Lắp ráp" (assembled).

**Steps:**
1. Update `models.py` to add `origin: str = ""` field
2. In `step4_with_models.py`, search for these keywords in the container text
3. Set the origin accordingly

**Hint:** Use Python's `in` operator: `if "Nhập khẩu" in container_text:`

**Success Criteria:**
- Model has new `origin` field
- Output JSON shows origin for each car
- Default value is empty string if not found

---

## 🎯 Exercise 3: Scrape Multiple Pages

**Difficulty:** ⭐⭐ Medium

**Task:** Modify the crawler to scrape **pages 1, 2, and 3** and combine all results.

**Steps:**
1. Create a loop: `for page in range(1, 4):`
2. Call `fetch_car_listings(page)` for each page
3. Combine all results into one list
4. Save everything to one JSON file

**Hint:** Use list concatenation: `all_cars = [] → all_cars += page_cars`

**Success Criteria:**
- Scrapes 3 pages
- Approximately 30 listings total (10 per page)
- Single JSON file with all data

---

## 🎯 Exercise 4: Add Price Parsing

**Difficulty:** ⭐⭐⭐ Hard

**Task:** Convert price strings like "850 Triệu" to numeric values (850.0).

**Steps:**
1. Add `price_value: float = 0.0` field to the model
2. Write a function to parse price strings:
   - Extract numbers using regex: `re.findall(r'\d+', price)`
   - Handle "Triệu" (millions), "Tỷ" (billions)
   - Handle "Contact" → return 0.0
3. Set the `price_value` field

**Example:**
- "850 Triệu" → 850.0
- "1.5 Tỷ" → 1500.0
- "Contact" → 0.0

**Hint:** 
```python
import re
def parse_price(price_str):
    if "Contact" in price_str:
        return 0.0
    numbers = re.findall(r'[\d.]+', price_str)
    # ... your logic here
```

**Success Criteria:**
- Numeric price values in JSON
- Handles different formats correctly
- "Contact" listings have 0.0

---

## 🎯 Exercise 5: Add Error Logging

**Difficulty:** ⭐⭐⭐ Hard

**Task:** Add logging to track which listings fail to parse.

**Steps:**
1. Create a list: `failed_listings = []`
2. In the `except` block, store details about failed listings
3. After scraping, print a summary:
   - Total successful: X
   - Total failed: Y
   - Failed URLs: [list]

**Success Criteria:**
- Script tracks failed listings
- Prints summary at the end
- Shows URLs that failed to parse

---

## 🏆 Bonus Challenge: Scrape Different Website

**Difficulty:** ⭐⭐⭐⭐ Very Hard

**Task:** Apply what you've learned to scrape a **different website** of your choice.

**Requirements:**
1. Choose a website with static HTML content
2. Define appropriate Pydantic models
3. Extract at least 3 fields per item
4. Save to JSON

**Suggestions:**
- Product listings
- News articles
- Job postings
- Real estate listings

**Success Criteria:**
- Working crawler for new website
- Clean, validated data
- Proper error handling
- JSON output

---

## 🧪 Testing Your Solutions

After each exercise:

1. **Run the code** - Does it execute without errors?
2. **Check the output** - Is the JSON file valid?
3. **Inspect the data** - Are all fields populated correctly?
4. **Test edge cases** - What if a field is missing?

---

## 💡 Need Help?

- Re-read the step files for examples
- Check the model definition in `models.py`
- Use `print()` statements to debug
- Review BeautifulSoup documentation

---

## ✅ Solutions

Solutions are available in the `/solutions` folder (if you really need them!), but try to solve them yourself first. That's where the real learning happens! 🚀
