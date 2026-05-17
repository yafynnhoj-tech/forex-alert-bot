python
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
import requests
import schedule
import time
import os

# =========================
# TELEGRAM
# =========================

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# CONFIG
# =========================

PAIRS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X"
]

# Señales más realistas
RSI_BUY = 30
RSI_SELL = 70

# =========================
# MEMORY
# =========================

last_signals = {}

# =========================
# TELEGRAM ALERT
# =========================

def send_telegram(message):

    if not TOKEN or not CHAT_ID:
        print("ERROR: TOKEN o CHAT_ID no configurados")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url,
