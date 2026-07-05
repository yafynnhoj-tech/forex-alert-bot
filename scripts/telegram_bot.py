import requests
from config import TOKEN, CHAT_ID


def send_telegram(message):

    if not TOKEN:
        print("❌ TOKEN no encontrado")
        return

    if not CHAT_ID:
        print("❌ CHAT_ID no encontrado")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        response = requests.post(url, data=data)

        print("Telegram:", response.text)

    except Exception as e:

        print(e)