# Bonbanh Crawler with Pydantic

> **📚 For Learning:**  
> If you're new to web scraping, check out the **simplified step-by-step examples** in:  
> [`../teaching-examples/01_static_html_scraping/`](../teaching-examples/01_static_html_scraping/)  
>  
> This folder contains the production-ready version. The teaching examples break down the concepts into digestible steps perfect for live coding!

---

This project is an example of how to build a robust web crawler using **Pydantic** for data validation and structure.

## Structure

- `models.py`: Defines the data schema using Pydantic. This ensures that every car listing we crawl matches a specific format and type (e.g., year is an integer, price is a string).
- `crawler.py`: Contains the logic to fetch pages from Bonbanh and parse the HTML into our Pydantic models.
- `main.py`: The entry point to run the crawler and save the data to `bonbanh_data.json`.

## Why Pydantic?

When crawling data, websites often have inconsistent formatting. Pydantic helps us:
1.  **Validate Data**: Ensure field types are correct (e.g., `year` is a number).
2.  **Handle Missing Data**: Define optional fields easily.
3.  **Serialize**: Convert our objects to JSON effortlessly.

## How to Run

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the crawler:
    ```bash
    python main.py
    ```

3.  Check the output in `bonbanh_data.json`.
