# Web Scraping Teaching Examples

A progressive learning path for web scraping, from beginner to advanced. Each level builds on the previous one.

---

## Learning Path

```
Level 1: Static HTML         →  Level 2: Dynamic Content  →  Level 3: API-Based
(BeautifulSoup)                  (Selenium)                   (Async)
   2-3 hours                        2-3 hours                     2-3 hours
```

---

## Three Levels

### Level 1: Static HTML Scraping 
Folder: `01_static_html_scraping/`

What you'll learn:
- HTTP requests with `requests` library
- HTML parsing with `BeautifulSoup`
- CSS selectors for data extraction
- Data validation with `Pydantic`
- Exporting to JSON

**Prerequisites:** Basic Python knowledge

**Target:** Scrape car listings from Bonbanh.com

---

### **Level 2: Dynamic Content Scraping**
📁 `02_dynamic_content_scraping/`

**What you'll learn:**
- Browser automation with `Selenium`
- Waiting for dynamic content to load
- XPath for precise element selection
- Table data extraction
- Exporting to CSV and JSON

**Prerequisites:** Complete Level 1

**Target:** Scrape VNINDEX stock data from CafeF.vn

---

### **Level 3: API-Based Scraping**
📁 `03_api_based_scraping/`

**What you'll learn:**
- Inspecting network requests (DevTools)
- Finding hidden API endpoints
- Asynchronous programming with asyncio
- Concurrent requests with aiohttp
- Rate limiting and semaphores

Prerequisites: Complete Level 2

Target: Scrape VNINDEX data from CafeF API (fast!)

---

## Quick Start

### Start from Level 1 (Recommended)
```bash
cd 01_static_html_scraping
pip install -r requirements.txt
python step1_basic_request.py
```

### Jump to a Specific Level
If you already know BeautifulSoup:
```bash
cd 02_dynamic_content_scraping
pip install -r requirements.txt
python step1_open_browser.py
```

---

## How to Use

For Students:
1. Follow in order: step1 → step2 → step3 → step4
2. Run after each step to see progress
3. Complete exercises in exercises.md
4. Experiment: Modify the code and see what happens

For Instructors (Live Coding):
1. Type the code, don't copy-paste (students learn by watching you think)
2. Run frequently to show output after small changes
3. Explain as you go using comments as talking points
4. Encourage questions and pause between steps

---

## Technical Requirements

All Levels:
- Python 3.8+
- pip (package manager)

Level 2 Only:
- Google Chrome browser
- Chrome will auto-download ChromeDriver

Level 3 Only:
- Basic understanding of JSON
- Familiarity with async/await (we'll teach it!)

---

## Speed Comparison

| Aspect | Level 1 (Static) | Level 2 (Selenium) | Level 3 (API) |
|--------|------------------|-------------------|---------------|
| Speed | Fast | Slow (browser) | Very Fast |
| Complexity | Low | Medium | Medium-High |
| Use Case | Static pages | Dynamic content | Best performance |
| JavaScript | No | Yes | N/A (direct API) |
| Detection Risk | Low | Medium | Low |

Rule of Thumb:
- Try Level 1 first (simplest)
- Use Level 2 if content loads via JavaScript
- Use Level 3 if you find an API (fastest)

---

## Learning Outcomes

After completing all three levels:

- Scrape data from any website (static or dynamic)
- Validate and structure scraped data
- Export data to JSON and CSV formats
- Use browser automation when needed
- Find and use hidden API endpoints
- Write efficient async scrapers
- Handle rate limiting and errors gracefully

---

## Legal & Ethical Considerations

Before scraping any website:

1. Read the website's robots.txt
2. Check Terms of Service
3. Respect rate limits (don't overload servers)
4. Use data responsibly
5. Never scrape personal data without consent

These examples are for educational purposes only.

---

## Need Help?

- Check the README.md in each level folder
- Review the exercises.md for practice problems
- Read the code comments carefully
- Try running the code step-by-step

Happy scraping!
