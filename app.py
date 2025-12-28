import matplotlib
matplotlib.use("Agg")

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from pair_selection import compute_correlation, adf_test
from signal_engine import generate_signal
from backtester import backtest_pair
from data_loader import fetch_pair_data


def map_lookback(lookback):
    return {"1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}[lookback]



st.set_page_config(page_title="Pair Trading Research Tool", layout="wide")

st.title("📈 Pair Trading Research Tool")
st.markdown("""
**Developed by Parth Sharma**  
_Pair Trading Research & Decision Support Tool_
""")
st.markdown("---")


st.header("🔍 Analyze a Stock Pair")

col1, col2 = st.columns(2)
with col1:
    stock_a = st.text_input("Stock A (Yahoo symbol)", "HDFCBANK.NS")
with col2:
    stock_b = st.text_input("Stock B (Yahoo symbol)", "ICICIBANK.NS")

col3, col4 = st.columns(2)
with col3:
    lookback = st.selectbox("Lookback Period", ["1 Year", "2 Years", "5 Years"], index=1)
with col4:
    advanced_mode = st.checkbox("Advanced Mode (Experimental)")

capital = st.number_input("Investment Amount (₹)", 10000, step=5000, value=50000)

if advanced_mode:
    st.info("Advanced mode enables exploratory analysis even for weak pairs.")

st.markdown("---")


analyze = st.button("🚀 Analyze Pair")

if analyze:
    period = map_lookback(lookback)

    with st.spinner("Fetching market data..."):
        prices = fetch_pair_data(stock_a, stock_b, period)

    if prices.empty:
        st.error("No market data available. Check ticker symbols.")
        st.stop()

    corr = compute_correlation(stock_a, stock_b)
    p_value = adf_test(stock_a, stock_b)
    z_score, signal = generate_signal(stock_a, stock_b)
    pnl, trades = backtest_pair(stock_a, stock_b)

   
    st.markdown("## 💡 Investment Decision")

    confidence = "Low"
    recommendation = "AVOID"

    if corr > 0.6 and p_value is not None and p_value < 0.05:
        confidence = "High"
        if signal in ["BUY", "SELL"]:
            recommendation = "CONSIDER TRADE"
    elif corr > 0.5:
        confidence = "Medium"
        if advanced_mode:
            recommendation = "EXPLORATORY ONLY"

    if recommendation == "CONSIDER TRADE":
        st.success("✅ Statistical edge detected. Trade may be considered.")
    elif recommendation == "EXPLORATORY ONLY":
        st.warning("⚠ Weak but interesting relationship. Exploratory only.")
    else:
        st.error("❌ No reliable statistical edge. Avoid trading.")

    
    beta = prices[stock_a].cov(prices[stock_b]) / prices[stock_b].var()
    alloc_a = capital / (1 + abs(beta))
    alloc_b = alloc_a * abs(beta)

    vol = prices[stock_a].pct_change().std()
    est_pnl = capital * vol * min(abs(z_score), 2)

    st.markdown("### 📈 Estimated Outcome (Illustrative)")
    st.write(f"• Allocate ₹{alloc_a:,.0f} in {stock_a}")
    st.write(f"• Allocate ₹{alloc_b:,.0f} in {stock_b}")
    st.info(f"Estimated short-term P&L range: ±₹{est_pnl:,.0f}")

   
    st.markdown("## 📊 Analysis")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(prices.index, prices[stock_a], label=stock_a)
    ax.plot(prices.index, prices[stock_b], label=stock_b)
    ax.legend()
    ax.set_title("Price Movement")
    st.pyplot(fig)

    spread = prices[stock_a] - beta * prices[stock_b]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(spread.index, spread)
    ax.axhline(spread.mean(), linestyle="--")
    ax.set_title("Spread (Mean Reversion)")
    st.pyplot(fig)

    rolling_mean = spread.rolling(30).mean()
    rolling_std = spread.rolling(30).std()
    z_series = (spread - rolling_mean) / rolling_std

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(z_series.index, z_series)
    ax.axhline(2, color="red", linestyle="--")
    ax.axhline(-2, color="green", linestyle="--")
    ax.axhline(0, color="black")
    ax.set_title("Z-Score")
    st.pyplot(fig)

   
    st.markdown("## 📊 Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Correlation", f"{corr:.2f}")
    c2.metric("ADF p-value", f"{p_value:.4f}" if p_value else "N/A")
    c3.metric("Z-Score", f"{z_score:.2f}")

    st.markdown("### 🚦 Trading Signal")
    st.success(signal)

    st.markdown("### 💰 Backtest Summary")
    st.write(f"Total Trades: {trades}")
    st.write(f"Total P&L (spread units): {pnl:.2f}")
    p_value_display = f"{p_value:.4f}" if p_value is not None else "N/A"
    st.markdown("### 📝 Explanation")
    st.info(
    f"""
    • The pair shows a correlation of **{corr:.2f}**  
    • ADF p-value: **{p_value_display}**  

    This indicates {'a statistically valid mean-reverting relationship' if p_value is not None and p_value < 0.05 else 'weak or no cointegration'}.

    • Current Z-score: **{z_score:.2f}**  
    • Resulting signal: **{signal}**
    """
)

st.markdown("---")
st.caption(
    "👨‍💻 Developed by Parth Sharma | "
    "Educational & research use only — not financial advice."
)