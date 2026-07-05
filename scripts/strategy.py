from indicators import (
    calculate_rsi,
    calculate_ema,
    calculate_macd,
    calculate_atr
)


def analyze(df):

    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()

    price = close.iloc[-1]

    rsi = calculate_rsi(close)
    ema = calculate_ema(close)
    macd, signal = calculate_macd(close)
    atr = calculate_atr(high, low, close)

    trend = "BULLISH" if price > ema else "BEARISH"

    score_buy = 0
    score_sell = 0
    reasons = []

    # RSI
    if rsi < 30:
        score_buy += 25
        reasons.append("RSI sobrevendido")

    elif rsi > 70:
        score_sell += 25
        reasons.append("RSI sobrecomprado")

    # MACD
    if macd > signal:
        score_buy += 25
        reasons.append("MACD alcista")

    else:
        score_sell += 25
        reasons.append("MACD bajista")

    # EMA
    if price > ema:
        score_buy += 25
        reasons.append("Precio sobre EMA200")

    else:
        score_sell += 25
        reasons.append("Precio bajo EMA200")

    # Tendencia
    if trend == "BULLISH":
        score_buy += 25

    else:
        score_sell += 25

    if score_buy >= 75:

        trade = "BUY"
        confidence = score_buy

    elif score_sell >= 75:

        trade = "SELL"
        confidence = score_sell

    else:

        trade = "WAIT"
        confidence = max(score_buy, score_sell)

    return {

        "price": price,

        "rsi": round(rsi, 2),

        "ema": round(ema, 5),

        "atr": round(atr, 5),

        "trend": trend,

        "signal": trade,

        "confidence": confidence,

        "reasons": reasons

    }