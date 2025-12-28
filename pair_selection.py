print("pair_selection started")
from data_loader import fetch_pair_data
from statsmodels.tsa.stattools import adfuller
import numpy as np

def compute_correlation(stock_a, stock_b,period="2y"):
    prices=fetch_pair_data(stock_a, stock_b,period)
    corr=prices[stock_a].corr(prices[stock_b])
    return corr

def adf_test(stock_a, stock_b, period="2y"):
    prices = fetch_pair_data(stock_a, stock_b, period)

    if prices.empty or stock_a not in prices or stock_b not in prices:
        return None

    spread = prices[stock_a] - prices[stock_b]

    spread = spread.dropna()

    # 🔴 CRITICAL CHECK
    if len(spread) < 50:
        return None

    if spread.max() == spread.min():
        return None

    result = adfuller(spread)
    return result[1]
if __name__=="__main__":
    print("Running correlation + ADF test")

    stock_a = "HDFCBANK.NS"
    stock_b = "ICICIBANK.NS"

    corr=compute_correlation(stock_a, stock_b)
    print(f"Correlation: {corr:.2f}")

    p_value = adf_test(stock_a, stock_b)
    print(f"ADF p_value: {p_value:.4f}")

    if p_value < 0.05:
        print("Valid pair (mean-reverting)")
    else:
        print("Reject pair (not mean-reverting)")    