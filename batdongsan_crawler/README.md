# BatDongSan.com.vn Crawler

A web crawler for batdongsan.com.vn using **Clean Architecture** and **curl-cffi** to bypass Cloudflare.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Basic crawl (2 pages, apartments + houses)
python -m batdongsan crawl --pages 2

# Crawl rentals
python -m batdongsan crawl -l cho-thue --pages 5

# Crawl specific property type
python -m batdongsan crawl -t can-ho-chung-cu --pages 10

# With more workers
python -m batdongsan crawl --concurrent 5 --pages 3

# Show all property types
python -m batdongsan types

# Full help
python -m batdongsan crawl --help
```

## Output

Files saved to `output/`:
- `batdongsan_*.jsonl` - JSON Lines (streaming)
- `batdongsan_*.csv` - CSV format

## Project Structure

```
src/batdongsan/
├── domain/          # Entities, Interfaces
├── application/     # SpiderService
├── infrastructure/  # HTTP, Parsers, Storage
├── interface/cli/   # CLI commands
└── container.py     # Dependency Injection
```

## Configuration

Environment variables (prefix `BATDONGSAN_`):
- `BATDONGSAN_MAX_CONCURRENT=5`
- `BATDONGSAN_DELAY_MIN=2.0`
- `BATDONGSAN_DELAY_MAX=4.0`
