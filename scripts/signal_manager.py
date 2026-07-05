from pathlib import Path
import json
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SIGNALS_FILE = BASE_DIR / "data" / "signals.json"

print("BASE_DIR:", BASE_DIR)
print("SIGNALS_FILE:", SIGNALS_FILE)

def load_signals():
    """
    Carga todas las señales guardadas.
    """

    if not os.path.exists(SIGNALS_FILE):
        return []

    try:

        with open(SIGNALS_FILE, "r", encoding="utf-8") as file:

            return json.load(file)

    except:

        return []


def save_signal(signal):

    signals = load_signals()

    signals.insert(0, signal)

    # Mantener solamente las últimas 200 señales
    signals = signals[:200]

    with open(SIGNALS_FILE, "w", encoding="utf-8") as file:

        json.dump(
            signals,
            file,
            indent=4,
            ensure_ascii=False
        )


def last_signal(pair):

    signals = load_signals()

    for signal in signals:

        if signal["PAR"] == pair:

            return signal["SEÑAL"]

    return None