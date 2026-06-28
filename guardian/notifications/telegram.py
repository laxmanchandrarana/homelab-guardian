import os
import requests


class TelegramNotifier:
    API_URL = "https://api.telegram.org/bot{token}/sendMessage"

    def send(self, title: str, message: str):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN not configured")

        if not chat_id:
            raise RuntimeError("TELEGRAM_CHAT_ID not configured")

        payload = {
            "chat_id": chat_id,
            "text": f"🚨 <b>{title}</b>\n\n{message}",
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        response = requests.post(
            self.API_URL.format(token=token),
            json=payload,
            timeout=15,
        )

        print("Telegram Status:", response.status_code)
        print("Telegram Response:", response.text)

        response.raise_for_status()

        return response.json()
