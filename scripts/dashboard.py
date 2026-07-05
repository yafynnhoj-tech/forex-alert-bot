from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import json

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Forex AI Dashboard",
    layout="wide"
    
)
st_autorefresh(interval=5000, key="refresh")
# =========================
# TITLE
# =========================

st.title("🚀 FOREX AI DASHBOARD PRO")

st.markdown("---")

# =========================
# LOAD REAL SIGNALS
# =========================

try:

    with open("signals.json", "r") as file:

        data = json.load(file)

except:

    data = []

# =========================
# METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 PARES ACTIVOS", len(data))
col2.metric("🟢 ESTADO", "RUNNING")
col3.metric("🌎 MERCADO", "FOREX")
col4.metric("🤖 AI STATUS", "ACTIVE")

st.markdown("---")

# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(data)

# =========================
# COLOR SIGNALS
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
# SHOW TABLE
# =========================

if not df.empty:

    styled_df = df.style.map(
        color_signal,
        subset=["SEÑAL"]
    )

    st.dataframe(
        styled_df,
        use_container_width=True
    )

else:

    st.warning("⚠️ NO HAY SEÑALES TODAVÍA")

# =========================
# FOOTER
# =========================

st.success("✅ AI DASHBOARD ONLINE")