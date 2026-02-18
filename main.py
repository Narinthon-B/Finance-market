import yfinance as yf
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # Model for Analyzing Sentiment
from sqlalchemy import create_engine

analyzer = SentimentIntensityAnalyzer()

# function to analyze sentiment and return score compound
def get_sentiment(text):
   if not text:
      return 0
   return analyzer.polarity_scores(text)['compound']

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
        search_new = yf.Search(symbols, max_results=10)
        for item in search_new.news: 
            title = item.get('title')
            score = get_sentiment(title)

            all_new.append({
               'symbol' : symbols,
               'title' : title,
               'link' : item.get('link'),
               'publisher' : item.get('publisher'),
               'sentimentScore': score,
               'publishedAt': pd.to_datetime(item.get('providerPublishTime'), unit='s')
            })

    except Exception as e:
      print(f"Error fetching data for {symbols}: {e}")

  df_prices = pd.concat(all_prices)
  df_news = pd.DataFrame(all_new)

  return df_prices, df_news

# postgresql://[user]:[password]@[host]:[port]/[db_name]
db_url = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
engine = create_engine(db_url)

def save_to_database(df_prices, df_news):
   print("checking database")

   # check if data already exists
   try:
      existing_prices = pd.read_sql("SELECT \"Symbol\", \"Datetime\" FROM stock_prices", engine)

      df_prices['Datetime'] = pd.to_datetime(df_prices['Datetime'])
      existing_prices['Datetime'] = pd.to_datetime(existing_prices['Datetime'])

      new_prices = df_prices.merge(existing_prices, on=['Symbol', 'Datetime'], how='left', indicator=True)
      new_prices = new_prices[new_prices['_merge'] == 'left_only'].drop('_merge', axis=1)

      # save to database
      if not new_prices.empty:
         new_prices.to_sql('stock_prices', engine, index=False, if_exists='append')
         print(f"Saved {len(new_prices)} new prices to database")
      else:
         print("No new prices to save")
  
   # save to database
   except Exception as e:
      print(f"System Message: {e}")
      print(f"First time saving data to database")
      df_prices.to_sql('stock_prices', engine, index=False, if_exists='append')
      df_news.to_sql('stock_news', engine, index=False, if_exists='append')

symbol = ['BBL.BK', 'SCB.BK', 'KTB.BK']
interval = '1h'
period = '7d'
prices, news = get_ticker_data(symbol, interval, period)
print(f"Total prices: {prices}")
print(f"Total news: {news}")

save_to_database(prices, news)

print("\nTesting Data Read")
test_df = pd.read_sql("SELECT * FROM stock_news LIMIT 5", engine)
print(test_df)