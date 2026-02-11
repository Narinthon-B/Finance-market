import yfinance as yf

# ค้นหาข่าวโดยใช้ Keyword หรือ Ticker
search = yf.Search("BBL.BK", max_results=5)

for news in search.news:
    print(f"หัวข้อ: {news.get('title')}")
    print(f"ลิงก์: {news.get('link')}")
    print("-" * 20)

