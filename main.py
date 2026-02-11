import yfinance as yf
import pandas as pd

# function to fetch data
def get_ticker_data(symbol, interval, period):
  all_prices = []
  all_new = []

  for symbols in symbol:
    try:
        print(f"Fetching data for {symbols}")
        stock = yf.Ticker(symbols)

        # fetch intraday data
        intraday_data = stock.history(interval=interval, period=period).reset_index()
        if not intraday_data.empty:
          intraday_data['Symbol'] = symbols
          all_prices.append(intraday_data)

        # fetch news
        search_new = yf.Search(symbols, max_results=5)
        for item in search_new.news: 
            all_new.append({
               'symbol' : symbols,
               'title' : item.get('title'),
               'link' : item.get('link'),
               'publisher' : item.get('publisher'),
               'publishedAt': pd.to_datetime(item.get('providerPublishTime'), unit='s')
            })

    except Exception as e:
      print(f"Error fetching data for {symbols}: {e}")

  df_prices = pd.concat(all_prices)
  df_news = pd.DataFrame(all_new)

  return df_prices, df_news

symbol = ['BBL.BK', 'SCB.BK', 'KTB.BK']
interval = '1h'
period = '7d'
prices, news = get_ticker_data(symbol, interval, period)

print(f"Total prices: {prices}")
print(f"Total news: {news}")
