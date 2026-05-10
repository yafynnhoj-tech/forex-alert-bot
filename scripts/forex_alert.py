import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
import requests
import schedule
import time

# =========================
# TELEGRAM
# =========================

import os

TOKEN = os.getenv("8527015467:AAGzCSMGAegfjgMtV7Alrf3-XkyBUIGs_gE")
CHAT_ID = os.getenv("1360272040")

# =========================
# CONFIG
# =========================

PAIRS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X"
]

RSI_BUY = 20
RSI_SELL = 85

# =========================
# MEMORY
# =========================

last_signals = {}

# =========================
# TELEGRAM ALERT
# =========================

def send_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# =========================
# ANALYSIS
# =========================

def analyze_market():

    print("\n===================================")
    print("ANALIZANDO MERCADO...")
    print("===================================\n")

    for pair in PAIRS:

        try:

            # =========================
            # DOWNLOAD DATA
            # =========================

            df = yf.download(
                pair,
                period="5d",
                interval="15m"
            )

            close_prices = df["Close"].squeeze()

            # =========================
            # RSI
            # =========================

            df["RSI"] = RSIIndicator(
                close=close_prices,
                window=14
            ).rsi()

            # =========================
            # MACD
            # =========================

            macd = MACD(close=close_prices)

            df["MACD"] = macd.macd()
            df["MACD_SIGNAL"] = macd.macd_signal()

            # =========================
            # LAST VALUES
            # =========================

            last_rsi = df["RSI"].iloc[-1]
            last_macd = df["MACD"].iloc[-1]
            last_signal = df["MACD_SIGNAL"].iloc[-1]

            # =========================
            # PRINT STATUS
            # =========================

            print(
                f"{pair} | RSI: {last_rsi:.2f} | "
                f"MACD: {last_macd:.4f}"
            )

            # =========================
            # BUY SIGNAL
            # =========================

            if (
                last_rsi <= RSI_BUY
                and last_macd > last_signal
            ):

                # evitar spam
                if last_signals.get(pair) != "BUY":

                    message = f"""
🟢 POSIBLE COMPRA

Par: {pair}

RSI: {last_rsi:.2f}

MACD CONFIRMADO ✅
"""

                    print(message)

                    send_telegram(message)

                    last_signals[pair] = "BUY"

            # =========================
            # SELL SIGNAL
            # =========================

            elif (
                last_rsi >= RSI_SELL
                and last_macd < last_signal
            ):

                # evitar spam
                if last_signals.get(pair) != "SELL":

                    message = f"""
🔴 POSIBLE VENTA

Par: {pair}

RSI: {last_rsi:.2f}

MACD CONFIRMADO ✅
"""

                    print(message)

                    send_telegram(message)

                    last_signals[pair] = "SELL"

            # =========================
            # NO SIGNAL
            # =========================

            else:

                last_signals[pair] = "NONE"

        except Exception as e:

            print(f"ERROR EN {pair}: {e}")

# =========================
# SCHEDULE
# =========================

schedule.every(15).minutes.do(analyze_market)

# =========================
# FIRST RUN
# =========================

analyze_market()

# =========================
# INFINITE LOOP
# =========================

while True:

    schedule.run_pending()
    time.sleep(1)