from data_loader import fetch_pair_data
import numpy as np

def compute_zscore(spread):
    mean = np.mean(spread)
    std=np.std(spread)
    z_score=(spread-mean)/std
    return z_score

def generate_signal(stock_a, stock_b):
    prices=fetch_pair_data(stock_a, stock_b)
    
    spread = prices[stock_a]-prices[stock_b]

    z_score = compute_zscore(spread)
    latest_z_score=z_score.iloc[-1]

    if latest_z_score > 2:
        signal = "SELL"
    elif latest_z_score < -2:
        signal="BUY"
    elif abs(latest_z_score) < 0.5:
        signal="EXIT"
    else:
        signal="HOLD"  

    return latest_z_score, signal          

if __name__ == "__main__":
    print("Running Z-score signal test")
    stock_a="HDFCBANK.NS"
    stock_b="ICICIBANK.NS"

    z_score,signal=generate_signal(stock_a, stock_b)

    print(f"Latest Z-score: {z_score:.2f}")
    print(f"Trading Signal: {signal}")


