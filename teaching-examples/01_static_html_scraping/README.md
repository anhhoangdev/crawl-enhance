# Level 1: Static HTML Scraping

Learn the fundamentals of web scraping using requests and BeautifulSoup.

---

## Learning Objectives

By the end of this level, you will:
- Understand HTTP requests and responses
- Parse HTML with BeautifulSoup
- Use CSS selectors to find elements
- Extract and structure data
- Validate data with Pydantic
- Export data to JSON

---

## Step-by-Step Guide

### Step 1: Basic HTTP Request (step1_basic_request.py)
Learn how to fetch a webpage using Python's `requests` library.

```bash
python step1_basic_request.py
```

**Key Concepts:**
- HTTP GET requests
- Response status codes
- Raw HTML content

---

### **Step 2: Parse HTML** (`step2_parse_html.py`)
Parse HTML and extract car titles using BeautifulSoup.

```bash
python step2_parse_html.py
```

**Key Concepts:**
- BeautifulSoup parser
- `find_all()` method
- CSS class selectors
- Extracting text from elements

---

### **Step 3: Extract Multiple Fields** (`step3_extract_data.py`)
Extract title, price, URL, and year from each listing.

```bash
python step3_extract_data.py
```

**Key Concepts:**
- CSS selectors (`.select_one()`)
- Extracting attributes (`get('href')`)
- Regular expressions for pattern matching
- Python dictionaries for data storage

---

### **Step 4: Complete Crawler** (`step4_with_models.py`)
Add Pydantic validation and save to JSON.

```bash
python step4_with_models.py
```

**Key Concepts:**
- Pydantic BaseModel
- Data validation
- JSON serialization
- Error handling

**Output:** `car_listings.json`

---

## 🛠️ Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

---

## 🎓 Exercises

See [`exercises.md`](./exercises.md) for hands-on practice!

---

## 💡 Tips for Live Coding

**For Instructors:**
1. Start with `step1` - show the raw HTML
2. Point out the HTML structure in browser DevTools
3. In `step2`, explain how BeautifulSoup makes parsing easy
4. In `step3`, show how regex extracts patterns
5. In `step4`, demonstrate Pydantic catching invalid data (try passing a string for `year`)

**For Students:**
- Type along, don't just copy-paste!
- Run the code after each change
- Use `print()` to debug
- Read error messages carefully

---

## 🔍 When to Use This Approach

✅ **Use static scraping when:**
- The data is already in the HTML (view source shows it)
- No JavaScript is required to load content
- Website doesn't have a public API

❌ **Don't use static scraping when:**
- Content loads dynamically with JavaScript → Use Level 2 (Selenium)
- Website has an API → Use Level 3 (API-based)

---

## 📖 Additional Resources

- [Requests Documentation](https://requests.readthedocs.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.php)

---

## ➡️ Next Level

Ready for dynamic content? **[Level 2: Dynamic Content Scraping →](../02_dynamic_content_scraping/)**
