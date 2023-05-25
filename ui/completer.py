import pandas as pd
df = pd.read_csv('./data/Tickers.csv',header=None)
stock_lists = list(df[0])
stock_lists = [stock_name.split('.')[0].lower() for stock_name in stock_lists]