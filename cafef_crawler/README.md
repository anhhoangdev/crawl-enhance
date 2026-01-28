# CafeF VNINDEX Crawler with Pydantic

> **📚 For Learning:**  
> If you're learning Selenium and browser automation, check out the **step-by-step examples** in:  
> [`../teaching-examples/02_dynamic_content_scraping/`](../teaching-examples/02_dynamic_content_scraping/)  
>  
> This folder contains the production-ready version. The teaching examples break down Selenium concepts progressively!

---

This project scrapes VNINDEX historical trading data from CafeF using **Selenium** and validation with **Pydantic**.

## Structure

- `models.py`: Defines `StockData` model (Open, Close, High, Low, Volume, etc.).
- `crawler.py`: Selenium-based crawler that extracts data and maps it to `StockData` objects.
- `main.py`: Entry point to run the crawler and export to JSON/CSV.

## How to Run

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the crawler:
    ```bash
    python main.py
    ```

3.  Output:
    - `vnindex_data.json`
    - `vnindex_data.csv`
