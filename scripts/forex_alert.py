import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
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
    print("ANALIZANDO MERCADO")
    print("==============================\n")

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
            # EMA 200
            # =========================

            ema_200 = EMAIndicator(
                close=close_prices,
                window=200
            )

            df["EMA200"] = ema_200.ema_indicator()

            # =========================
            # LAST VALUES
            # =========================

            rsi = df["RSI"].iloc[-1]
            macd_value = df["MACD"].iloc[-1]
            signal = df["MACD_SIGNAL"].iloc[-1]
            ema200 = df["EMA200"].iloc[-1]
            price = close_prices.iloc[-1]

            # =========================
            # PRINT STATUS
            # =========================

            print(
                f"{pair} | "
                f"PRICE: {price:.4f} | "
                f"RSI: {rsi:.2f} | "
                f"MACD: {macd_value:.4f} | "
                f"EMA200: {ema200:.4f}"
            )

            # =========================
            # BUY SIGNAL
            # =========================

            if (
                rsi < RSI_BUY
                and macd_value > signal
                and price > ema200
            ):

                if last_signals.get(pair) != "BUY":

                    message = f"""
🟢 BUY SIGNAL

PAIR: {pair}

PRICE: {price:.4f}

RSI: {rsi:.2f}

EMA200 FILTER ✅

MACD CONFIRMED ✅
"""

                    print(message)

                    send_telegram(message)

                    last_signals[pair] = "BUY"

            # =========================
            # SELL SIGNAL
            # =========================

            elif (
                rsi > RSI_SELL
                and macd_value < signal
                and price < ema200
            ):

                if last_signals.get(pair) != "SELL":

                    message = f"""
🔴 SELL SIGNAL

PAIR: {pair}

PRICE: {price:.4f}

RSI: {rsi:.2f}

EMA200 FILTER ✅

MACD CONFIRMED ✅
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

print("BOT INICIADO")

analyze_market()

# =========================
# LOOP
# =========================

while True:

    schedule.run_pending()
    time.sleep(1)