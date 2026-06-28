import asyncio

from guardian.notifications.telegram import TelegramNotifier
from guardian.notifications.discord import DiscordNotifier
from guardian.notifications.email import EmailNotifier
from guardian.notifications.slack import SlackNotifier
from guardian.api.events import publish


class NotificationService:

    def __init__(self):

        self.telegram = TelegramNotifier()
        self.discord = DiscordNotifier()
        self.email = EmailNotifier()
        self.slack = SlackNotifier()

    def _broadcast(self, payload: dict):
        """
        Broadcast an event to all connected WebSocket clients.

        If there is already an event loop running (FastAPI),
        schedule the task.
        Otherwise (CLI/tests), create a temporary loop.
        """

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(
                publish("notification", payload)
            )
        except RuntimeError:
            asyncio.run(
                publish("notification", payload)
            )

    def send(self, title: str, message: str):

        results = {}

        notifiers = {
            "telegram": self.telegram,
            "discord": self.discord,
            "email": self.email,
            "slack": self.slack,
        }

        for name, notifier in notifiers.items():

            try:

                notifier.send(title, message)

                results[name] = "SUCCESS"

                self._broadcast(
                    {
                        "channel": name,
                        "title": title,
                        "message": message,
                        "status": "success",
                    }
                )

            except Exception as exc:

                results[name] = str(exc)

                self._broadcast(
                    {
                        "channel": name,
                        "title": title,
                        "message": message,
                        "status": "failed",
                        "error": str(exc),
                    }
                )

        return results
