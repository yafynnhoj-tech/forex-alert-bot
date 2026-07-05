import os
from dotenv import load_dotenv

# ===========================
# CARGAR VARIABLES
# ===========================

load_dotenv()

# ===========================
# TELEGRAM
# ===========================

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ===========================
# FOREX
# ===========================

PAIRS = [

    # MAJORS
    "EURUSD=X",
    "USDJPY=X",
    "GBPUSD=X",
    "AUDUSD=X",
    "USDCAD=X",
    "USDCHF=X",
    "NZDUSD=X",

    # CROSSES
    "EURJPY=X",
    "GBPJPY=X",
    "EURGBP=X",
    "EURAUD=X",
    "GBPAUD=X",

    # METALES
    "GC=F",

]

# ===========================
# PARAMETROS
# ===========================

RSI_BUY = 30
RSI_SELL = 70

EMA_PERIOD = 200

ATR_PERIOD = 14

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

RISK_REWARD = 2

ATR_MULTIPLIER = 1.5