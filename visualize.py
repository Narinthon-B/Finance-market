import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def analyze_data(prices_file, news_file, target_symbol):
  df_prices = pd.read_csv('files/stock_prices.csv')
  df_news = pd.read_csv('files/stock_news.csv')

  df_prices['Datetime'] = pd.to_datetime(df_prices['Datetime'])
  df_news['publishedAt'] = pd.to_datetime(df_news['publishedAt'])

  price_sub = df_prices[df_prices['Symbol'] == target_symbol].sort_values('Datetime')
  news_sub = df_news[df_news['symbol'] == target_symbol].copy()

  news_sub['time_grouped'] = news_sub['publishedAt'].dt.floor('h')
  sentiment_hourly = news_sub.groupby('time_grouped')['sentimentScore'].mean().reset_index()

  fig, ax1 = plt.subplots(figsize=(14, 7))

  color_price = 'tab:blue'
  ax1.set_xlabel('Datetime')
  ax1.set_ylabel('Price', color=color_price, fontsize=12)

  ax1.plot(price_sub['Datetime'], price_sub['Close'], color=color_price, label='Close Price', linewidth=2)
  ax1.tick_params(axis='y', labelcolor=color_price)

  ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
  ax1.xaxis.set_major_locator(mdates.HourLocator(interval=12))
  plt.xticks(rotation=45)

  ax2 = ax1.twinx()

  color_sent = 'tab:orange'
  ax2.set_ylabel('Sentiment Score (-1 to 1)', color=color_sent, fontsize=12)
  ax2.bar(sentiment_hourly['time_grouped'], sentiment_hourly['sentimentScore'], color=color_sent, alpha=0.5, width=0.03, label='Avg Sentiment')

  ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8)
  ax2.tick_params(axis='y', labelcolor=color_sent)

  plt.title(f"Price vs Sentiment CorrelationL {target_symbol}", fontsize=16)
  fig.tight_layout()
  plt.show()

df_prices = pd.read_csv('files/stock_prices.csv')
df_news = pd.read_csv('files/stock_news.csv')
analyze_data('df_prices', 'df_news', 'BBL.BK')
analyze_data('df_prices', 'df_news', 'SCB.BK')
analyze_data('df_prices', 'df_news', 'KTB.BK')