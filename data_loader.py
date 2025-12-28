import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="2y"):
    data = yf.download(ticker, period=period, progress=False)
    return data

def fetch_pair_data(stock_a, stock_b, period="2y"):
    data = yf.download([stock_a, stock_b], period=period, progress=False)["Close"]
    data = data.dropna()
    return data



if __name__ == "__main__":
    print("data_loader.py test run")

    df = fetch_stock_data("HDFCBANK.NS")
    print(df.head())