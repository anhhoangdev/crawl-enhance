# Level 3 Exercises: API-Based Scraping

Master async scraping with these challenges!

---

## 🎯 Exercise 1: Find Another API

**Difficulty:** ⭐⭐ Medium

**Task:** Use DevTools to find the API for a **different stock** on CafeF (e.g., VNM, VIC).

**Steps:**
1. Navigate to another stock's page
2. Open DevTools → Network tab
3. Filter for XHR
4. Reload and find the API call
5. Modify `step2_single_request.py` to use that API

**Success Criteria:**
- Successfully find the API endpoint
- Extract data for different stock
- Display results

---

## 🎯 Exercise 2: Change Page Size

**Difficulty:** ⭐ Easy

**Task:** Modify `step2_single_request.py` to fetch **50 records** instead of 20.

**Hint:** Change the `PageSize` parameter from 20 to 50.

**Success Criteria:**
- Gets 50 records in one request
- JSON shows all 50 records

---

## 🎯 Exercise 3: Add Progress Bar

**Difficulty:** ⭐⭐ Medium

**Task:** Add a progress indicator to show which pages are being fetched.

**Steps:**
1. Install: `pip install tqdm`
2. Import: `from tqdm import tqdm`
3. Wrap your page loop:
   ```python
   for i in tqdm(range(1, total_pages + 1), desc="Fetching"):
       # your code
   ```

**Success Criteria:**
- Visual progress bar shows during scraping
- Updates as each page completes

---

## 🎯 Exercise 4: Add Retry Logic

**Difficulty:** ⭐⭐⭐ Hard

**Task:** If a request fails, automatically retry up to 3 times.

**Steps:**
1. In `fetch_page()`, wrap the request in a retry loop
2. Use exponential backoff (wait 1s, then 2s, then 4s)
3. Log each retry attempt

**Hint:**
```python
for attempt in range(3):
    try:
        # make request
        break
    except Exception as e:
        if attempt < 2:
            await asyncio.sleep(2 ** attempt)
        else:
            raise
```

**Success Criteria:**
- Retries on failure
- Exponential backoff delays
- Logs retry attempts

---

## 🎯 Exercise 5: Scrape Date Range

**Difficulty:** ⭐⭐⭐ Hard

**Task:** Modify the scraper to fetch data for a **specific date range**.

**Steps:**
1. Update parameters to set `StartDate` and `EndDate`
2. Format: "dd/mm/yyyy"
3. Make it configurable via function arguments

**Example:**
```python
crawler.crawl(start_date="01/01/2026", end_date="31/01/2026")
```

**Success Criteria:**
- Only fetches data in specified range
- Date validation (start before end)
- Works with different date ranges

---

## 🎯 Exercise 6: Compare Multiple Stocks

**Difficulty:** ⭐⭐⭐⭐ Very Hard

**Task:** Scrape data for **multiple stocks concurrently** and compare them.

**Steps:**
1. Create a list of symbols: `["VNINDEX", "VNM", "VIC"]`
2. Fetch all stocks concurrently
3. Save each to separate CSV files
4. Create a comparison chart (optional: use matplotlib)

**Hint:**
```python
async def scrape_all_stocks(symbols):
    tasks = [scrape_symbol(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    return results
```

**Success Criteria:**
- Scrapes multiple stocks in parallel
- Separate files for each stock
- Comparison summary printed

---

## 🏆 Bonus Challenge: Rate Limit Calculator

**Difficulty:** ⭐⭐⭐⭐ Very Hard

**Task:** Create a smart rate limiter that adjusts based on server response time.

**Concept:**
- If server responds fast → increase concurrency
- If server slows down → decrease concurrency
- Track response times and adapt

**Hints:**
- Track response time for each request
- Calculate average response time
- Adjust semaphore limit dynamically

**Success Criteria:**
- Dynamically adjusts concurrency
- Doesn't overwhelm server
- Logs concurrency changes

---

## 🧪 Testing Your Solutions

Test async code carefully:

1. **Print statements** - Use them liberally in async functions
2. **Test small** - Start with 2-3 pages before scaling up
3. **Check output** - Verify JSON/CSV are valid
4. **Monitor network** - Use DevTools to see actual requests

---

## 💡 Debugging Async Code

**Common issues:**

1. **"Coroutine was never awaited"**
   - Forgot `await` keyword
   - Should be: `await fetch_page()` not `fetch_page()`

2. **"Event loop is closed"**
   - Windows-specific, use the fix in step3/step4

3. **Timeout errors**
   - Server is slow or rate limiting you
   - Reduce `max_concurrent`
   - Add delays between requests

**Pro tips:**
- Use `asyncio.create_task()` to see what's running
- Add `print(f"Starting {page}")` and `print(f"Done {page}")` to track execution
- Use `time.time()` to measure async speedup

---

## 🎓 Understanding Async

**Coffee Shop Analogy:**

**Synchronous (Sequential):**
```
Customer 1 orders → wait → receive → leave
Customer 2 orders → wait → receive → leave
Customer 3 orders → wait → receive → leave
Total: 15 minutes
```

**Asynchronous (Concurrent):**
```
Customer 1 orders ─┐
Customer 2 orders ─┼─→ All brewing in parallel
Customer 3 orders ─┘
All receive at once
Total: 5 minutes
```

**That's the power of async!** ⚡

---

## ✅ Solutions

Solutions available in `/solutions` folder, but challenge yourself first! 🚀
