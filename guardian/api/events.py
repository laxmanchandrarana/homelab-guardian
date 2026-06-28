from guardian.api.websocket_manager import manager


async def publish(event_type: str, data: dict):
    await manager.broadcast(
        {
            "type": event_type,
            "data": data,
        }
    )

