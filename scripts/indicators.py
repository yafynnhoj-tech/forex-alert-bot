from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange


def calculate_rsi(close):

    return RSIIndicator(
        close=close,
        window=14
    ).rsi().iloc[-1]


def calculate_ema(close):

    return EMAIndicator(
        close=close,
        window=200
    ).ema_indicator().iloc[-1]


def calculate_macd(close):

    macd = MACD(close=close)

    return (
        macd.macd().iloc[-1],
        macd.macd_signal().iloc[-1]
    )


def calculate_atr(high, low, close):

    atr = AverageTrueRange(
        high=high,
        low=low,
        close=close,
        window=14
    )

    return atr.average_true_range().iloc[-1]