import json
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import AverageTrueRange
import requests
import schedule
import time
import os
import json
# =========================
# TELEGRAM
# =========================

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# CONFIG
# =========================

PAIRS = [

    # MAJORS
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X",
    "USDCAD=X",
    "USDCHF=X",
    "NZDUSD=X",

    # CROSSES
    "EURGBP=X",
    "EURJPY=X",
    "GBPJPY=X",
    "EURAUD=X",
    "GBPAUD=X",

    # GOLD
    "GC=F"
]

RSI_BUY = 30
RSI_SELL = 70

last_signals = {}

total_trades = 0

# =========================
# TELEGRAM FUNCTION
# =========================

def send_telegram(message):
    signal_data = {

    "PAR": pair,

    "PRECIO": round(price, 5),

    "RSI": round(rsi, 2),

    "TENDENCIA": trend,

    "SEÑAL": "BUY",

    "SL": round(stop_loss, 5),

    "TP": round(take_profit, 5),

    "WINRATE": f"{winrate}%"

}

try:

    with open("signals.json", "r") as file:

        signals = json.load(file)

except:

    signals = []

signals.append(signal_data)

with open("signals.json", "w") as file:

    json.dump(signals, file, indent=4)  
    signal_data = {
    "PAR": pair,
    "SEÑAL": "SELL",
    "RSI": round(rsi, 2),
    "PRECIO": round(price, 5),
    "SL": round(stop_loss, 5),
    "TP": round(take_profit, 5)
}

try:

    with open("signals.json", "r") as file:
        signals = json.load(file)

except:
    signals = []

signals.append(signal_data)

with open("signals.json", "w") as file:
    json.dump(signals, file, indent=4)

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
# EMA FUNCTION
# =========================

def get_ema(df):

    close_prices = df["Close"].squeeze()

    ema = EMAIndicator(
        close=close_prices,
        window=200
    )

    return ema.ema_indicator().iloc[-1]

# =========================
# ANALYSIS
# =========================

def analyze_market():

    global total_trades

    print("\n===================================")
    print("MULTI TIMEFRAME ANALYSIS")
    print("===================================\n")

    for pair in PAIRS:

        try:

            # =========================
            # M15 DATA
            # =========================

            df_m15 = yf.download(
                pair,
                period="5d",
                interval="15m"
            )

            # =========================
            # H1 DATA
            # =========================

            df_h1 = yf.download(
                pair,
                period="1mo",
                interval="1h"
            )

            # =========================
            # H4 DATA
            # =========================

            df_h4 = yf.download(
                pair,
                period="3mo",
                interval="4h"
            )

            # =========================
            # CLOSE PRICES
            # =========================

            close_m15 = df_m15["Close"].squeeze()
            close_h1 = df_h1["Close"].squeeze()
            close_h4 = df_h4["Close"].squeeze()

            # =========================
            # RSI
            # =========================

            df_m15["RSI"] = RSIIndicator(
                close=close_m15,
                window=14
            ).rsi()

            # =========================
            # MACD
            # =========================

            macd = MACD(close=close_m15)

            df_m15["MACD"] = macd.macd()
            df_m15["MACD_SIGNAL"] = macd.macd_signal()

            # =========================
            # EMA200
            # =========================

            ema_m15 = get_ema(df_m15)
            ema_h1 = get_ema(df_h1)
            ema_h4 = get_ema(df_h4)

            # =========================
            # ATR
            # =========================

                        # =========================
            # ATR
            # =========================

            high_prices = df_m15["High"].squeeze()
            low_prices = df_m15["Low"].squeeze()

            atr_indicator = AverageTrueRange(
                high=high_prices,
                low=low_prices,
                close=close_m15,
                window=14
            )

        

            df_m15["ATR"] = atr_indicator.average_true_range()

            # =========================
            # LAST VALUES
            # =========================

            rsi = df_m15["RSI"].iloc[-1]
            macd_value = df_m15["MACD"].iloc[-1]
            signal = df_m15["MACD_SIGNAL"].iloc[-1]
            atr = df_m15["ATR"].iloc[-1]

            price_m15 = close_m15.iloc[-1]
            price_h1 = close_h1.iloc[-1]
            price_h4 = close_h4.iloc[-1]

            # =========================
            # TREND FILTERS
            # =========================

            bullish_h1 = price_h1 > ema_h1
            bullish_h4 = price_h4 > ema_h4

            bearish_h1 = price_h1 < ema_h1
            bearish_h4 = price_h4 < ema_h4

            # =========================
            # PRINT STATUS
            # =========================

            print(
                f"{pair} | "
                f"PRICE: {price_m15:.4f} | "
                f"RSI: {rsi:.2f} | "
                f"MACD: {macd_value:.4f}"
            )

            # =========================
            # BUY SIGNAL
            # =========================

            if (
                rsi < RSI_BUY
                and macd_value > signal
                and bullish_h1
                and bullish_h4
            ):

                if last_signals.get(pair) != "BUY":

                    entry = price_m15
                    sl = entry - (atr * 1.5)
                    tp = entry + ((entry - sl) * 2)

                    message = f"""
🟢 BUY SIGNAL

PAIR: {pair}

ENTRY: {entry:.4f}

STOP LOSS: {sl:.4f}

TAKE PROFIT: {tp:.4f}

RISK REWARD: 2:1

RSI: {rsi:.2f}

M15 TREND ✅
H1 TREND ✅
H4 TREND ✅

MACD CONFIRMED ✅
"""

                    print(message)

                    send_telegram(message)

                    total_trades += 1

                    print(f"TOTAL TRADES: {total_trades}")

                    last_signals[pair] = "BUY"

            # =========================
            # SELL SIGNAL
            # =========================

            elif (
                rsi > RSI_SELL
                and macd_value < signal
                and bearish_h1
                and bearish_h4
            ):

                if last_signals.get(pair) != "SELL":

                    entry = price_m15
                    sl = entry + (atr * 1.5)
                    tp = entry - ((sl - entry) * 2)

                    message = f"""
🔴 SELL SIGNAL

PAIR: {pair}

ENTRY: {entry:.4f}

STOP LOSS: {sl:.4f}

TAKE PROFIT: {tp:.4f}

RISK REWARD: 2:1

RSI: {rsi:.2f}

M15 TREND ✅
H1 TREND ✅
H4 TREND ✅

MACD CONFIRMED ✅
"""

                    print(message)

                    send_telegram(message)

                    total_trades += 1

                    print(f"TOTAL TRADES: {total_trades}")

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

print("BOT INICIADO")

analyze_market()

# =========================
# LOOP
# =========================

while True:

    schedule.run_pending()
    time.sleep(1)