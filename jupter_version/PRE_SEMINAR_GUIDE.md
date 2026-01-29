# 🕷️ Web Scraping Fundamentals

### Pre-Seminar Preparation Guide

---

## 👋 What's good!

I'm [@anhhoangdev](https://github.com/anhhoangdev) — your guide through this web scraping journey.

Data engineer by day, trail runner by sunset, and always got something playing in the headphones (lately it's been a lot of J. Cole and Kendrick). 🎧

> *Fun fact: I came up with half this curriculum while hiking in Đà Lạt. Mountains clear the mind, you know?* 🏔️

---

## 🎯 What this seminar is about

We're teaching you to **get data from the internet** — the right way.

Not some copy-paste StackOverflow tutorial. We're talking:
- Real websites
- Real techniques
- Real gotchas

By the end, you'll have scraped stock market data, car listings, and maybe your own side project idea.

---

## 📅 What we'll cover

| Module | Topic | Vibe |
|--------|-------|------|
| 1 | Static HTML Scraping | *"The fundamentals. No shortcuts."* |
| 2 | Dynamic Content | *"When JavaScript enters the chat."* |
| 3 | API-Based Scraping | *"The secret pro technique."* |

**Time**: ~4 hours  
**Level**: Beginner-friendly, but we move  
**Platform**: Google Colab 

---

## ✅ Before you show up

### Bring these:

- [x] A Google account (for Colab)
- [x] Chrome browser
- [x] Basic Python knowledge (you know what a `for` loop is)
- [x] Some water 💧 — we're going for 4 hours

### Quick concept check

If these sound foreign, spend 10 minutes googling:

| Term | ELI5 |
|------|------|
| **HTTP GET** | "Yo server, give me that page" |
| **HTML** | The skeleton/bones of a webpage |
| **JSON** | Data that looks like Python dicts |
| **API** | A backdoor to get data directly |

### Try this before the session

1. Open Chrome → Go to [CafeF](https://cafef.vn)
2. Press `F12` (DevTools)
3. Click **Network** tab
4. Reload the page
5. See all those requests flying in?

That's the matrix. We're about to read it. 🟢

---

## 🧠 The mental model

Web scraping has levels. Like a video game.

```
┌─────────────────────────────────────────────────┐
│  Level 3: API Calls     ← The cheat code 🎮     │
│  Level 2: Selenium      ← The heavy artillery   │
│  Level 1: requests+BS4  ← The foundation        │
└─────────────────────────────────────────────────┘
```

We always try Level 3 first. Then Level 1. Selenium is the last resort.

> *"Work smarter, not harder."*

---

## 🎯 What you'll walk away with

- ✅ Fetch and parse HTML like a pro
- ✅ Handle JavaScript-heavy sites
- ✅ Find hidden APIs (the real skill)
- ✅ Build async scrapers (10x faster)
- ✅ Validate messy data with Pydantic
- ✅ Confidence to scrape any website you encounter

---

## ⚠️ The ethics talk

Look, scraping is powerful. Uncle Ben was right about responsibility.

**Do:**
- ✅ Respect `robots.txt`
- ✅ Rate limit your requests
- ✅ Read the Terms of Service

**Don't:**
- ❌ Scrape personal data without consent  
- ❌ DDoS a site by accident
- ❌ Bypass authentication

---

## 📚 Optional reading

Want to get ahead? Here you go:

| Resource | Link |
|----------|------|
| BeautifulSoup docs | [crummy.com/software/BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| Selenium Python | [selenium-python.readthedocs.io](https://selenium-python.readthedocs.io/) |
| XPath cheatsheet | [devhints.io/xpath](https://devhints.io/xpath) |
| Pydantic | [docs.pydantic.dev](https://docs.pydantic.dev/) |

---

## 💻 The notebooks

We'll work through these in order:

1. **Module 1**: Static HTML → `01_static_html_scraping.ipynb`
2. **Module 2**: Dynamic Content → `02_dynamic_content_scraping.ipynb`  
3. **Module 3**: API Scraping → `03_api_based_scraping.ipynb`

Just click → Open in Colab → Run cells → Learn.

---

## ❓ Questions?

Bring 'em. No question is too basic.

The only dumb question is the one you didn't ask and then spent 2 hours debugging alone.

---

*See you at the seminar, fam.* ✌️

— anhhoangdev
