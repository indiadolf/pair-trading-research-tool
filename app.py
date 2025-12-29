import matplotlib
matplotlib.use("Agg")

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from pair_selection import compute_correlation, adf_test
from signal_engine import generate_signal
from backtester import backtest_pair
from data_loader import fetch_pair_data



st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}
.card h3 {
    color: #38bdf8;
}
.confidence-bar {
    height: 18px;
    border-radius: 10px;
    background: linear-gradient(90deg, #ef4444, #facc15, #22c55e);
}
</style>
""", unsafe_allow_html=True)



def map_lookback(lb):
    return {"1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}[lb]



st.set_page_config(page_title="Pair Trading Research Tool", layout="wide")

st.title("📈 Pair Trading Research Tool")
st.markdown("""
**Developed by Parth Sharma**  
**Co-Developed by Priyanshu Kindo & Ashutosh Rathore**  
_Pair Trading Research & Decision Support Tool_
""")
st.markdown("---")



st.header("🔍 Analyze a Stock Pair")

c1, c2 = st.columns(2)
with c1:
    stock_a = st.text_input("Stock A (Yahoo symbol)", "HDFCBANK.NS")
with c2:
    stock_b = st.text_input("Stock B (Yahoo symbol)", "ICICIBANK.NS")

c3, c4 = st.columns(2)
with c3:
    lookback = st.selectbox("Lookback Period", ["1 Year", "2 Years", "5 Years"], index=1)
with c4:
    advanced_mode = st.checkbox("Advanced Mode (Experimental)")

capital = st.number_input("Investment Amount (₹)", min_value=10000, step=5000, value=50000)

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

  
    confidence_score = 0
    if corr > 0.7: confidence_score += 40
    if p_value is not None and p_value < 0.05: confidence_score += 40
    if abs(z_score) > 1.5: confidence_score += 20

    confidence_pct = min(confidence_score, 100)

  
    should_trade = confidence_pct >= 70 and signal in ["BUY", "SELL"]

    st.markdown("## 💡 Decision Summary")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if should_trade:
        st.success("✅ Trade MAY be considered (statistical edge detected)")
    elif advanced_mode:
        st.warning("⚠ Weak edge — exploratory only")
    else:
        st.error("❌ No reliable edge — avoid trade")

    st.markdown("### Model Confidence")
    st.progress(confidence_pct / 100)

    st.markdown("</div>", unsafe_allow_html=True)

   
    beta = prices[stock_a].cov(prices[stock_b]) / prices[stock_b].var()
    alloc_a = capital / (1 + abs(beta))
    alloc_b = alloc_a * abs(beta)

    volatility = prices[stock_a].pct_change().std()
    est_return = capital * volatility * min(abs(z_score), 2)

    st.markdown("## 💰 Capital Allocation & Estimated Return")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write(f"• Allocate **₹{alloc_a:,.0f}** in **{stock_a}**")
    st.write(f"• Allocate **₹{alloc_b:,.0f}** in **{stock_b}**")
    st.info(f"📊 Estimated short-term P&L range: **±₹{est_return:,.0f}**")
    st.caption("Estimate based on historical volatility & deviation magnitude.")
    st.markdown("</div>", unsafe_allow_html=True)

   
    st.markdown("## 📊 Visual Analysis")

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(prices.index, prices[stock_a], label=stock_a)
    ax.plot(prices.index, prices[stock_b], label=stock_b)
    ax.legend()
    ax.set_title("Price Movement")
    st.pyplot(fig)

    spread = prices[stock_a] - beta * prices[stock_b]
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(spread.index, spread)
    ax.axhline(spread.mean(), linestyle="--")
    ax.set_title("Spread (Mean Reversion)")
    st.pyplot(fig)

    rolling_mean = spread.rolling(30).mean()
    rolling_std = spread.rolling(30).std()
    z_series = (spread - rolling_mean) / rolling_std

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(z_series.index, z_series)
    ax.axhline(2, color="red", linestyle="--")
    ax.axhline(-2, color="green", linestyle="--")
    ax.axhline(0, color="black")
    ax.set_title("Z-Score")
    st.pyplot(fig)

    
    st.markdown("## 📊 Key Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Correlation", f"{corr:.2f}")
    m2.metric("ADF p-value", f"{p_value:.4f}" if p_value else "N/A")
    m3.metric("Z-Score", f"{z_score:.2f}")

    st.markdown("### 🚦 Trading Signal")
    st.success(signal)

    st.markdown("### 💼 Backtest Summary")
    st.write(f"Total Trades: {trades}")
    st.write(f"Total P&L (spread units): {pnl:.2f}")

    st.markdown("### 📝 Explanation")
    st.info(
        f"""
        • Correlation: **{corr:.2f}**  
        • ADF p-value: **{p_value:.4f if p_value else 'N/A'}**  
        • Z-score: **{z_score:.2f}**

        Signal **{signal}** generated based on deviation from equilibrium.
        """
    )

st.markdown("---")
st.caption(
    "👨‍💻 Parth Sharma ·\n"
    "Educational & research use only — not financial advice."
)