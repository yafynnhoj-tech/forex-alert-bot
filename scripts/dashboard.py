import streamlit as st
import pandas as pd
import random
import time

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="FOREX AI DASHBOARD",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("🚀 FOREX AI DASHBOARD")

st.markdown("---")

# =========================
# FAKE REALTIME DATA
# =========================

pairs_data = [

    {
        "PAIR": "EURUSD",
        "PRICE": round(random.uniform(1.05, 1.20), 5),
        "RSI": round(random.uniform(20, 80), 2),
        "TREND": random.choice(["BULLISH", "BEARISH"]),
        "SIGNAL": random.choice(["BUY", "SELL", "WAIT"]),
        "SL": round(random.uniform(1.05, 1.15), 5),
        "TP": round(random.uniform(1.15, 1.25), 5),
        "WINRATE": f"{random.randint(60,90)}%"
    },

    {
        "PAIR": "GBPUSD",
        "PRICE": round(random.uniform(1.20, 1.40), 5),
        "RSI": round(random.uniform(20, 80), 2),
        "TREND": random.choice(["BULLISH", "BEARISH"]),
        "SIGNAL": random.choice(["BUY", "SELL", "WAIT"]),
        "SL": round(random.uniform(1.20, 1.30), 5),
        "TP": round(random.uniform(1.30, 1.40), 5),
        "WINRATE": f"{random.randint(60,90)}%"
    },

    {
        "PAIR": "USDJPY",
        "PRICE": round(random.uniform(140, 165), 3),
        "RSI": round(random.uniform(20, 80), 2),
        "TREND": random.choice(["BULLISH", "BEARISH"]),
        "SIGNAL": random.choice(["BUY", "SELL", "WAIT"]),
        "SL": round(random.uniform(140, 155), 3),
        "TP": round(random.uniform(155, 165), 3),
        "WINRATE": f"{random.randint(60,90)}%"
    },

    {
        "PAIR": "AUDUSD",
        "PRICE": round(random.uniform(0.60, 0.75), 5),
        "RSI": round(random.uniform(20, 80), 2),
        "TREND": random.choice(["BULLISH", "BEARISH"]),
        "SIGNAL": random.choice(["BUY", "SELL", "WAIT"]),
        "SL": round(random.uniform(0.60, 0.70), 5),
        "TP": round(random.uniform(0.70, 0.80), 5),
        "WINRATE": f"{random.randint(60,90)}%"
    }

]

# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(pairs_data)

# =========================
# METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("ACTIVE PAIRS", "4")
col2.metric("ONLINE STATUS", "RUNNING")
col3.metric("MARKET", "FOREX")
col4.metric("AI STATUS", "ACTIVE")

st.markdown("---")

# =========================
# TABLE
# =========================

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# =========================
# FOOTER
# =========================

st.success("✅ AI DASHBOARD ONLINE")

# =========================
# AUTO REFRESH
# =========================

time.sleep(5)
st.rerun()