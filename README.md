# 📈 Pair Trading Research Tool

A **quantitative pair trading research application** built using Python and Streamlit.  
This tool helps analyze whether two stocks exhibit **mean-reverting behavior**, generate trading signals, and evaluate risk-adjusted performance through backtesting.

>  This project is for **educational and research purposes only**.  
> It does **not** provide financial advice or guarantee profits.

---

##  Live App
👉 https://pair-trading-research-tool-agexj8cwh7t5us8a3jvxmz.streamlit.app/

---

##  What This App Does

The app allows a user to:

- Select **two stocks** (Yahoo Finance symbols)
- Choose a **historical lookback period**
- Analyze whether the pair is statistically suitable for **pair trading**
- View:
  - Correlation
  - ADF cointegration test result
  - Z-score–based trading signal
  - Backtest performance
  - Estimated capital allocation & illustrative P&L
- Visualize:
  - Price movements
  - Spread behavior
  - Z-score over time

---

##  Methodology (In Simple Terms)

1. **Pair Selection**
   - Measures correlation between two stocks
   - Tests for cointegration using the **Augmented Dickey–Fuller (ADF) test**

2. **Signal Generation**
   - Constructs a market-neutral spread using a hedge ratio
   - Computes rolling **Z-scores**
   - Generates signals:
     - BUY / SELL (extreme deviation)
     - HOLD / EXIT (no edge)

3. **Risk-Aware Backtesting**
   - Transaction costs & slippage included
   - Maximum holding period enforced
   - Tracks:
     - Total P&L
     - Number of trades
     - **Maximum drawdown**

4. **Decision Support**
   - Provides an **investment recommendation**
   - Estimates **capital allocation**
   - Shows an **illustrative P&L range** (not a prediction)

---

##  Risk Metrics

- **Total P&L** (spread units)
- **Number of trades**
- **Maximum Drawdown**
  - Measures the worst peak-to-trough loss during backtesting
  - Helps assess downside risk

---

##  Known Limitations

- Past performance does **not** guarantee future results
- Assumes stable market relationships
- Uses historical data only (no real-time execution)
- Estimated P&L is **illustrative**, not predictive
- Rolling beta was tested but excluded due to instability

---

##  Tech Stack

- **Python**
- **Streamlit** (UI)
- **yfinance** (market data)
- **NumPy / Pandas**
- **Statsmodels** (ADF test)
- **Matplotlib** (visuals)

---

##  Project Structure
-pair-trading-research-tool/
│
├── app.py              # Streamlit app
├── data_loader.py      # Market data fetcher
├── pair_selection.py   # Correlation & ADF test
├── signal_engine.py    # Z-score signal logic
├── backtester.py       # Backtesting & risk metrics
├── requirements.txt
└── README.md

---

##  Authors

- **Parth Sharma**

---

##  Disclaimer

This application is intended **only for learning and research**.  
It should **not** be used for real trading or investment decisions.

---
