# CafeF VNINDEX Crawler (Advanced - API-Based)

> **📚 For Learning:**  
> If you want to learn async API scraping from scratch, check out the **step-by-step examples** in:  
> [`../teaching-examples/03_api_based_scraping/`](../teaching-examples/03_api_based_scraping/)  
>  
> This folder contains the production-ready version. The teaching examples explain async concepts progressively!

---

This project scrapes VNINDEX data directly from the CafeF API using **asyncio** and **aiohttp** for maximum performance.

## Structure

- `models.py`: Full `StockData` model with Vietnamese field mappings
- `crawler.py`: Async crawler with rate limiting using semaphore
- `main.py`: Entry point to run the crawler and export to JSON/CSV
- `inspect_api.py`: Helper to inspect the API structure

## Performance

**Speed Comparison:**
- Selenium (synchronous): ~30-60 seconds for 200 records
- API (async): ~5-10 seconds for 200 records
- **5-6x faster!** ⚡

## How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the crawler:
    ```bash
    python main.py
    ```

3. Output:
    - `vnindex_advanced.json`
    - `vnindex_advanced.csv`

## Why API-Based?

- ✅ Much faster (no browser overhead)
- ✅ Lower resource usage
- ✅ More reliable (no JavaScript timing issues)
- ✅ Easier to scale

## When to Use

Use API-based scraping when:
- You've discovered an accessible API endpoint
- Speed and efficiency matter
- You need to scrape large amounts of data
- The API allows programmatic access

## Learn More

For a complete guide on finding and using APIs, see the teaching examples in [`../teaching-examples/03_api_based_scraping/`](../teaching-examples/03_api_based_scraping/).
