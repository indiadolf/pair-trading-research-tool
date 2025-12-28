TRANSACTION_COST = 0.0005
SLIPPAGE = 0.0002

print("Backtesting started")

from data_loader import fetch_pair_data
import numpy as np
import statsmodels.api as sm


def compute_hedge_ratio(price_a, price_b):
    price_b = sm.add_constant(price_b)
    model = sm.OLS(price_a, price_b).fit()
    return model.params[1]


def backtest_pair(stock_a, stock_b):
    prices = fetch_pair_data(stock_a, stock_b)

    price_a = prices[stock_a]
    price_b = prices[stock_b]

    beta = compute_hedge_ratio(price_a, price_b)
    print(f"Hedge Ratio (β): {beta:.4f}")

    spread = price_a - beta * price_b

    mean = spread.rolling(window=30).mean()
    std = spread.rolling(window=30).std()
    z_score = (spread - mean) / std

    position = 0
    entry_spread = 0.0
    pnl = 0.0
    trades = 0

    holding_days = 0
    MAX_HOLD = 20

    for i in range(30, len(spread)):
        z = z_score.iloc[i]
        current_spread = spread.iloc[i]

        if position != 0:
            holding_days += 1


        if position == 0 and z < -2:
            position = 1
            entry_spread = current_spread
            holding_days = 0
            trades += 1

        
        elif position == 0 and z > 2:
            position = -1
            entry_spread = current_spread
            holding_days = 0
            trades += 1

       
        elif position != 0 and holding_days >= MAX_HOLD:
            trade_pnl = (
                current_spread - entry_spread
                if position == 1
                else entry_spread - current_spread
            )

            cost = abs(entry_spread) * (TRANSACTION_COST + SLIPPAGE) * 2
            pnl += trade_pnl - cost
            position = 0
            holding_days = 0

       
        elif position != 0 and abs(z) < 0.5:
            trade_pnl = (
                current_spread - entry_spread
                if position == 1
                else entry_spread - current_spread
            )

            cost = abs(entry_spread) * (TRANSACTION_COST + SLIPPAGE) * 2
            pnl += trade_pnl - cost
            position = 0
            holding_days = 0

    return pnl, trades


if __name__ == "__main__":
    stock_a = "HDFCBANK.NS"
    stock_b = "ICICIBANK.NS"

    pnl, trades = backtest_pair(stock_a, stock_b)

    print(f"Total Trades: {trades}")
    print(f"Total P&L (spread units): {pnl:.2f}")