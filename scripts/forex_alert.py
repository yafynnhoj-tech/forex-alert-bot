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

RSI_BUY = 30
RSI_SELL = 70

last_signals = {}

# =========================
# TELEGRAM FUNCTION
# =========================

def send_telegram(message):

    if not TOKEN or not CHAT_ID:
        print("ERROR: TOKEN o CHAT_ID faltan")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        response = requests.post(
            url,
            data=data
        )

        print("TELEGRAM:", response.text)

    except Exception as e:

        print("ERROR TELEGRAM:", e)

# =========================
# ANALYSIS
# =========================

def analyze_market():

    print("\n=============================")
    print("first run")
    print("==============================\n")

    
    send_telegram("🚀 BOT ONLINE Y FUNCIONANDO")

    analyze_market()

    for pair in PAIRS:

        try:

            df = yf.download(
                pair,
                period="5d",
                interval="15m"
            )

            close_prices = df["Close"].squeeze()

            df["RSI"] = RSIIndicator(
                close=close_prices,
                window=14
            ).rsi()

            macd = MACD(close=close_prices)

            df["MACD"] = macd.macd()
            df["MACD_SIGNAL"] = macd.macd_signal()

            rsi = df["RSI"].iloc[-1]
            macd_value = df["MACD"].iloc[-1]
            signal = df["MACD_SIGNAL"].iloc[-1]

            print(
                f"{pair} | RSI: {rsi:.2f} | MACD: {macd_value:.4f}"
            )

            # BUY
            if rsi < RSI_BUY and macd_value > signal:

                if last_signals.get(pair) != "BUY":

                    message = f"""
🟢 BUY SIGNAL

PAIR: {pair}

RSI: {rsi:.2f}

MACD CONFIRMED ✅
"""

                    print(message)

                    send_telegram(message)

                    last_signals[pair] = "BUY"

            # SELL
            elif rsi > RSI_SELL and macd_value < signal:

                if last_signals.get(pair) != "SELL":

                    message = f"""
🔴 SELL SIGNAL

PAIR: {pair}

RSI: {rsi:.2f}

MACD CONFIRMED ✅
"""

                    print(message)

                    send_telegram(message)

                    last_signals[pair] = "SELL"

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
# LOOP
# =========================

while True:

    schedule.run_pending()
    time.sleep(1)

