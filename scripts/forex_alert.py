import time
import schedule
import yfinance as yf

from config import PAIRS
from strategy import analyze
from signal_manager import save_signal, last_signal
from telegram_bot import send_telegram


def analyze_pair(pair):

    print(f"\nAnalizando {pair}...")

    try:

        df = yf.download(
            pair,
            period="5d",
            interval="15m",
            progress=False,
            auto_adjust=True
        )

        if df.empty:
            print("Sin datos")
            return

        result = analyze(df)

        signal = result["signal"]

        if signal == "WAIT":
            print("WAIT")
            return

        previous = last_signal(pair)

        if previous == signal:
            print("Señal repetida")
            return

        signal_data = {
            "PAR": pair,
            "SEÑAL": signal,
            "PRECIO": result["price"],
            "RSI": result["rsi"],
            "EMA": result["ema"],
            "ATR": result["atr"],
            "TENDENCIA": result["trend"],
            "CONFIANZA": result["confidence"],
            "MOTIVOS": result["reasons"]
        }

        save_signal(signal_data)

        message = f"""
🚀 FOREX AI PRO

━━━━━━━━━━━━━━━━━━

📊 PAR: {pair}

🎯 SEÑAL: {signal}

📈 CONFIANZA: {result['confidence']}%

💰 PRECIO: {result['price']:.5f}

📉 RSI: {result['rsi']}

📐 EMA200: {result['ema']}

📏 ATR: {result['atr']}

📊 TENDENCIA:
{result['trend']}

━━━━━━━━━━━━━━━━━━

🧠 MOTIVOS

{chr(10).join("✅ " + r for r in result["reasons"])}
"""

        send_telegram(message)

        print("✅ Señal enviada")

    except Exception as e:

        print(f"ERROR {pair}: {e}")


def run_bot():

    print("\n==============================")
    print("FOREX AI BOT INICIADO")
    print("==============================")

    for pair in PAIRS:
        analyze_pair(pair)


schedule.every(15).minutes.do(run_bot)

run_bot()

while True:
    schedule.run_pending()
    time.sleep(1)