import asyncio

from fastapi import APIRouter

from guardian.repositories.incident_repo import IncidentRepository
from guardian.healing.service import HealingService
from guardian.api.events import publish


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)

repo = IncidentRepository()
healer = HealingService()


def broadcast_incident(payload: dict):
    """
    Broadcast incident events to all connected WebSocket clients.
    Works from FastAPI, daemon threads and CLI.
    """

    try:
        loop = asyncio.get_running_loop()
        loop.create_task(
            publish("incident", payload)
        )

    except RuntimeError:
        asyncio.run(
            publish("incident", payload)
        )


@router.get("")
def incidents():

    rows = repo.list()

    return [
        {
            "id": i.id,
            "created": i.created,
            "severity": i.severity,
            "service": i.service,
            "message": i.message,
            "healed": i.healed,
        }
        for i in rows
    ]


@router.post("/{service}")
def create_incident(service: str):

    incident = {
        "severity": "CRITICAL",
        "service": service,
        "message": "Manual incident",
    }

    # Broadcast to live dashboard
    broadcast_incident(incident)

    # Trigger Guardian healing
    result = healer.heal(**incident)

    # Broadcast result
    broadcast_incident({
        **incident,
        "result": result,
    })

    return result
