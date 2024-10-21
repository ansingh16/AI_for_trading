import os
import yfinance as yf
# get list of files in ../data/ directory
import glob
import pandas as pd
import sys
import tqdm

# get file name of files in a directory

tickers = [file.split('.')[0] for file in os.listdir('../../Data/data/eod-quotemedia/daily')]

sectors=[]
tickr=[]
for ticker in tqdm.tqdm(tickers):
    tick = yf.Ticker(ticker)
    try:
        sectors.append(tick.info['sector'])
        tickr.append(ticker)
    except:
        sectors.append('Others')
        tickr.append(ticker)

ticker_data = pd.DataFrame({'ticker': tickr, 'sector': sectors}).to_csv('../../Data/sectors.csv',index=False)