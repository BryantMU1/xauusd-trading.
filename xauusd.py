import time
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import datetime

# 1. Web Page Configuration
st.set_page_config(page_title="XAUUSD Sentinel", page_icon="🥇", layout="wide")
st.title("🥇 XAUUSD (Gold) Market Sentinel")
st.markdown("Real-time technical analysis, volatility tracking, and actionable recommendations.")

# 2. Fetch Gold Data (Using Gold Futures GC=F as a proxy for XAUUSD)

def get_gold_data():
    gold = yf.download("GC=F", period="1d", interval="1m")
    return gold

data = get_gold_data()

 # 3. Calculate Simple RSI (Changed window from 14 to 7 for faster 1-minute reactions)
def calculate_rsi(data, window=7):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

data['RSI'] = calculate_rsi(data)
current_price = data['Close'].iloc[-1].item()
current_rsi = data['RSI'].iloc[-1].item()

# 4. Top Dashboard Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Current Gold Price (USD)", f"${current_price:.2f}")
# Updated label to reflect the 7-period RSI
col2.metric("RSI (7-Period)", f"{current_rsi:.2f}")

# 5. Recommendation Logic (Adjusted for high-frequency 1-minute volatility)
# Tightened the thresholds to 40 and 60 so it triggers more easily!
if current_rsi < 40:
    action = "🟢 BUY SIGNAL"
    reason = "Short-term RSI dropped below 40. Scalping opportunity for a quick rebound."
elif current_rsi > 60:
    action = "🔴 SELL SIGNAL"
    reason = "Short-term RSI spiked above 60. Momentum is exhausted, potential quick drop."
else:
    action = "⚪ HOLD / NEUTRAL"
    reason = "Price is chopping in a tight range. Waiting for a breakout."

# 6. Interactive Candlestick Chart with Plotly
st.subheader("Interactive Price Chart")
fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'].squeeze(),
                high=data['High'].squeeze(),
                low=data['Low'].squeeze(),
                close=data['Close'].squeeze(),
                name="XAUUSD")])

fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# 7. News Integration Placeholder
st.subheader("📰 Macro News Sentiment (Beta)")
st.warning("News API Integration pending. Market currently reacting to USD Inflation data.")
