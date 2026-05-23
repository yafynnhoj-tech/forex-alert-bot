import streamlit as st
import pandas as pd
import random
import time

# =========================
# CONFIG PAGE
# =========================

st.set_page_config(
    page_title="Forex AI Dashboard",
    layout="wide"
)

# =========================
# TITULO
# =========================

st.title("🚀 FOREX AI DASHBOARD PRO")

st.markdown("---")

# =========================
# PARES FOREX
# =========================

pairs = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF",
    "NZDUSD",
    "EURJPY",
    "GBPJPY",
    "EURGBP",
    "XAUUSD",
    "BTCUSD"
]

# =========================
# METRICAS SUPERIORES
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 PARES ACTIVOS", len(pairs))

with col2:
    st.metric("🟢 ESTADO BOT", "ONLINE")

with col3:
    st.metric("🌎 MERCADO", "FOREX")

with col4:
    st.metric("🤖 IA", "ACTIVA")

st.markdown("---")

# =========================
# DATA
# =========================

data = []

for pair in pairs:

    signal = random.choice(["BUY", "SELL", "WAIT"])

    if signal == "BUY":
        trend = "ALCISTA"

    elif signal == "SELL":
        trend = "BAJISTA"

    else:
        trend = "LATERAL"

    data.append({

        "PAR": pair,

        "PRECIO": round(random.uniform(1, 200), 4),

        "RSI": round(random.uniform(20, 80), 2),

        "TENDENCIA": trend,

        "SEÑAL": signal,

        "SL": round(random.uniform(1, 200), 4),

        "TP": round(random.uniform(1, 200), 4),

        "WINRATE": f"{random.randint(65,95)}%"

    })

# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(data)

# =========================
# COLOR HEATMAP
# =========================

def color_signal(val):

    if val == "BUY":
        return "background-color: green; color: white"

    elif val == "SELL":
        return "background-color: red; color: white"

    elif val == "WAIT":
        return "background-color: orange; color: black"

    return ""

# =========================
# TABLA PROFESIONAL
# =========================

styled_df = df.style.map(
    color_signal,
    subset=["SEÑAL"]
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=500
)

# =========================
# STATUS
# =========================

st.success("✅ DASHBOARD IA ONLINE")

# =========================
# AUTO REFRESH
# =========================

time.sleep(5)

st.rerun()