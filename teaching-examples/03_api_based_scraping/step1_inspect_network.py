"""
Step 1: How to Find API Endpoints
==================================

Goal: Learn to inspect network requests and find hidden APIs

This is a GUIDE file, not executable code!
Follow these instructions to discover API endpoints.

═══════════════════════════════════════════════════════════════════════

🔍 STEP-BY-STEP GUIDE: Finding Hidden APIs

1. Open the Website
   - Navigate to: https://cafef.vn/du-lieu/Lich-su-giao-dich-vnindex-1.chn
   - Let it fully load

2. Open Browser DevTools
   - Press F12 (or Right-click → Inspect)
   - Click the "Network" tab

3. Filter for XHR/Fetch Requests
   - In the Network tab, click "Fetch/XHR" or "XHR"
   - This shows only API calls, not images/CSS

4. Reload the Page
   - Press Ctrl+R or F5
   - Watch the Network tab populate with requests

5. Look for Suspicious URLs
   - Look for URLs ending in:
     * .ashx
     * .json
     * .php with parameters
     * /api/...
     * /Ajax/...
   
   - For CafeF, you should see:
     * PriceHistory.ashx ← THIS IS IT! 🎯

6. Click on the Request
   - Click "PriceHistory.ashx" in the Network tab
   - Go to the "Headers" tab
   - Find "Request URL"
   
   - Example:
     https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx
     ?Symbol=VNINDEX&PageIndex=1&PageSize=20

7. Identify Parameters
   - Symbol=VNINDEX    → Stock symbol
   - PageIndex=1       → Page number
   - PageSize=20       → Items per page

8. Check the Response
   - Click the "Response" or "Preview" tab
   - You should see JSON data with stock prices!
   
   - Example structure:
     {
       "Success": true,
       "Data": {
         "Data": [
           {
             "Ngay": "28/01/2026",
             "GiaDongCua": 1250.5,
             ...
           }
         ]
       }
     }

9. Test the API
   - Copy the full URL
   - Paste it in a new browser tab
   - You should see raw JSON!

═══════════════════════════════════════════════════════════════════════

🎯 KEY INSIGHTS:

✅ Many websites load data via APIs, even if they look like normal pages
✅ APIs are MUCH faster than Selenium (no browser needed!)
✅ Network tab is your best friend for finding APIs
✅ Look for JSON responses - they're easier to parse than HTML

⚠️ IMPORTANT:
- Not all websites have accessible APIs
- Some APIs require authentication
- Respect rate limits (don't spam!)
- Check robots.txt and Terms of Service

═══════════════════════════════════════════════════════════════════════

✏️ PRACTICE EXERCISE:

Try finding the API for another page on CafeF or a different website!

1. Open the page in browser
2. Open Network tab
3. Filter for XHR/Fetch
4. Reload page
5. Find the API call
6. Test it in a new tab

═══════════════════════════════════════════════════════════════════════

➡️ Next Step: step2_single_request.py
   Now that you know HOW to find APIs, let's actually USE one!
"""

print(__doc__)
