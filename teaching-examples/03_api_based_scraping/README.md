# Level 3: API-Based Scraping

Learn to scrape data **directly from APIs** using async programming for maximum speed!

---

## 🎯 Learning Objectives

By the end of this level, you will:
- ✅ Discover hidden API endpoints using browser DevTools
- ✅ Make direct API calls (no browser needed!)
- ✅ Understand async/await programming
- ✅ Use aiohttp for concurrent requests
- ✅ Implement rate limiting with semaphores
- ✅ Map API fields with Pydantic aliases
- ✅ Achieve 5-10x speedup over Selenium!

---

## 📚 Step-by-Step Guide

### **Step 1: Inspect Network Tab** (`step1_inspect_network.py`)
Learn how to find hidden API endpoints.

```bash
python step1_inspect_network.py
```

**Key Concepts:**
- Browser DevTools Network tab
- XHR/Fetch filtering
- Identifying API patterns
- Testing APIs in browser

**Important:** This is a guide, not executable code. Read it carefully!

---

### **Step 2: Single API Request** (`step2_single_request.py`)
Make your first direct API call.

```bash
python step2_single_request.py
```

**Key Concepts:**
- Direct API calls with `requests`
- URL parameters
- JSON parsing
- Speed vs Selenium

---

### **Step 3: Async Requests** (`step3_async_requests.py`)
Fetch multiple pages concurrently.

```bash
python step3_async_requests.py
```

**Key Concepts:**
- `async`/`await` syntax
- `aiohttp` for async HTTP
- `asyncio.gather()` for parallelism
- Connection pooling

**Output:** `vnindex_async.json`

---

### **Step 4: Complete Crawler** (`step4_rate_limiting.py`)
Production-ready scraper with rate limiting.

```bash
python step4_rate_limiting.py
```

**Key Concepts:**
- Semaphore for concurrency control
- Rate limiting (respectful scraping)
- Pydantic field aliases
- OOP crawler design
- Error handling

**Outputs:**
- `vnindex_final.json`
- `vnindex_final.csv`

---

## 🛠️ Installation

```bash
pip install -r requirements.txt
```

---

## 🎓 Exercises

See [`exercises.md`](./exercises.md) for hands-on practice!

---

## 💡 Tips for Live Coding

**For Instructors:**
1. **Step 1**: Actually open DevTools, show Network tab, demonstrate finding APIs
2. **Step 2**: Compare speed to Selenium (it's instant!)
3. **Step 3**: Explain async vs sync with a coffee shop analogy:
   - Sync: Wait for each coffee to finish
   - Async: Take all orders, make them concurrently
4. **Step 4**: Show how semaphore prevents overwhelming the server

**For Students:**
- Async can be confusing at first - that's normal!
- Start with step2 (sync) to understand the API
- Then move to step3 to see async in action
- Don't worry about understanding every detail of async immediately

---

## 🔍 When to Use API Scraping

✅ **Use API scraping when:**
- You find an accessible API endpoint
- Need to scrape large amounts of data
- Speed is important
- Website's robots.txt allows it

❌ **Don't use API scraping when:**
- No API exists → Use Level 1 or 2
- API requires authentication you don't have
- API is explicitly blocked in robots.txt

**Speed Comparison:**
- **Selenium (Level 2):** 30-60 seconds for 200 records
- **API (Level 3):** 5-10 seconds for 200 records
- **5-6x faster!** ⚡

---

## 🐛 Troubleshooting

### "RuntimeError: Event loop is closed" (Windows)
Add this before `asyncio.run()`:
```python
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

### "Too many concurrent requests"
- Reduce `max_concurrent` in step4
- Default is 5, try 3 if you get errors

### Pydantic validation errors
- API structure might have changed
- Check the raw JSON response
- Update model field aliases if needed

---

## 📖 Additional Resources

- [aiohttp Documentation](https://docs.aiohttp.org/)
- [asyncio Tutorial](https://realpython.com/async-io-python/)
- [Pydantic Field Aliases](https://docs.pydantic.dev/latest/usage/model_config/)
- [Network Tab Guide](https://developer.chrome.com/docs/devtools/network/)

---

## 🎯 Key Takeaways

1. **Always check for APIs first** - They're the fastest option
2. **Async is powerful** - Use it for I/O-bound tasks (API calls)
3. **Be respectful** - Use rate limiting, don't overwhelm servers
4. **Pydantic aliases** - Handle different field names cleanly

---

## 🏆 You've Completed All 3 Levels!

Congratulations! You now know:
1. **Level 1**: Static HTML scraping (BeautifulSoup)
2. **Level 2**: Dynamic content scraping (Selenium)
3. **Level 3**: API-based scraping (async)

You can now scrape almost any website! 🚀

---

## ⬅️ Back to Main

Return to: **[Teaching Examples Overview](../README.md)**
