# 🕷️ crawl-enhance

**From zero to production-ready web scraper.**

By [@anhhoangdev](https://github.com/anhhoangdev)

---

## 👋 What's good!

So you took the seminar. Cool.

But here's the thing — those notebooks were just the warmup. This repo is where the real stuff lives.

You want to be a **pro data collector**? Here's the path:

```
📚 Notebooks (basics)  →  🏗️ BatDongSan Crawler (production)  →  🚀 Your own project
```

---

## 📂 What's in here

```
crawl-enhance/
├── jupter_version/          # 📚 Teaching materials (start here if new)
│   ├── PRE_SEMINAR_GUIDE.md
│   ├── 01_static_html_scraping.ipynb
│   ├── 02_dynamic_content_scraping.ipynb
│   └── 03_api_based_scraping.ipynb
│
├── batdongsan_crawler/      # 🏗️ Production-ready crawler (study this)
│   └── src/batdongsan/
│       ├── domain/          # Entities & business logic
│       ├── application/     # Use cases & orchestration
│       ├── infrastructure/  # HTTP, parsers, storage
│       └── interface/       # CLI
│
└── teaching-examples/       # 📝 Raw Python examples
```

---

## 🎓 The Learning Path

### Level 1: Beginner
**Go through the notebooks first.**

| Notebook | What you'll learn |
|----------|-------------------|
| [Module 1](jupter_version/01_static_html_scraping.ipynb) | `requests` + BeautifulSoup |
| [Module 2](jupter_version/02_dynamic_content_scraping.ipynb) | Selenium for JS-heavy sites |
| [Module 3](jupter_version/03_api_based_scraping.ipynb) | Async API scraping (the pro move) |

### Level 2: Intermediate
**Study the production crawler.**

The `batdongsan_crawler/` is a real-world example using:
- ✅ **Clean Architecture** — separated concerns, testable code
- ✅ **Cloudflare bypass** — using `curl_cffi`
- ✅ **Pydantic validation** — every record is typed and validated
- ✅ **Multi-format export** — JSON, CSV, JSONL
- ✅ **CLI interface** — proper command-line tool

```bash
# Try it yourself
cd batdongsan_crawler
pip install -e .
python -m batdongsan crawl --pages 5
```

### Level 3: Pro
**Build your own.**

Take what you learned and build a crawler for:
- Your favorite e-commerce site
- Job listings
- News aggregator
- Social media data

---

## 🏗️ Clean Architecture Crash Course

The production crawler follows Clean Architecture. Here's why it matters:

```
┌─────────────────────────────────────────────────┐
│                   INTERFACE                     │
│            (CLI, API, whatever)                 │
├─────────────────────────────────────────────────┤
│                  APPLICATION                    │
│           (SpiderService, use cases)            │
├─────────────────────────────────────────────────┤
│                    DOMAIN                       │
│     (Entities: PropertyListing, Location)       │
├─────────────────────────────────────────────────┤
│                INFRASTRUCTURE                   │
│    (HTTP clients, parsers, storage, config)     │
└─────────────────────────────────────────────────┘
```

**The rule**: Inner layers don't know about outer layers.

**Why care?**
- Easy to test (mock the infrastructure)
- Easy to swap components (new parser? just implement the interface)
- Easy to understand (each layer has one job)

---

## 🛠️ Key Patterns You'll See

| Pattern | Where | Why |
|---------|-------|-----|
| **Dependency Injection** | `container.py` | Swap implementations without changing code |
| **Repository Pattern** | Storage classes | Abstract away data persistence |
| **Strategy Pattern** | Parsers | Different parsing logic, same interface |
| **Rate Limiting** | HTTP client | Don't get banned |

---

## 📊 Speed Comparison

From Module 3, remember this:

| Method | 200 records | Notes |
|--------|-------------|-------|
| Selenium | ~60s | Browser overhead, JS rendering |
| requests + BS4 | ~10s | Good for static HTML |
| Async API | ~5s | 10x faster, the pro way |

---

## ⚠️ Ethics & Best Practices

Real talk:
- ✅ Respect `robots.txt`
- ✅ Rate limit (don't DDoS)
- ✅ Check Terms of Service
- ✅ Cache aggressively
- ❌ Don't scrape personal data without consent
- ❌ Don't bypass authentication

---

## 🚀 Quick Start

### For students (notebooks)
```bash
# Just open in Colab, no setup needed
```

### For developers (production crawler)
```bash
git clone https://github.com/anhhoangdev/crawl-enhance.git
cd crawl-enhance/batdongsan_crawler
pip install -e .
python -m batdongsan crawl --pages 3
```

---

## 📚 Resources

| Topic | Link |
|-------|------|
| BeautifulSoup | [docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| Selenium Python | [docs](https://selenium-python.readthedocs.io/) |
| aiohttp | [docs](https://docs.aiohttp.org/) |
| Pydantic | [docs](https://docs.pydantic.dev/) |
| curl_cffi | [GitHub](https://github.com/yifeikong/curl_cffi) |
| Clean Architecture | [The Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) |

---

## 🤝 Contributing

Found a bug? Want to add a new example?  
PRs welcome.

---

*Go build something cool.* ✌️

— [@anhhoangdev](https://github.com/anhhoangdev)
