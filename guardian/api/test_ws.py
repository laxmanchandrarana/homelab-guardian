from guardian.api.events import broadcast


def send_test():
    broadcast(
        {
            "type": "test",
            "message": "Guardian websocket working",
        }
    )

