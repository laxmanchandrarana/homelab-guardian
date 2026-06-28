from fastapi import APIRouter, Request, HTTPException
import json

from guardian.alerts.service import AlertService

router = APIRouter(tags=["Alerts"])

service = AlertService()


@router.post("/alerts/webhook")
async def alertmanager_webhook(request: Request):

    body = await request.body()

    print("\n========== ALERTMANAGER ==========")
    print("Headers:")
    print(dict(request.headers))
    print("\nRaw Body:")
    print(body.decode(errors="ignore"))
    print("=================================\n")

    if not body:
        raise HTTPException(
            status_code=400,
            detail="Empty request body",
        )

    try:
        payload = json.loads(body)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON: {exc}",
        )

    return {
        "received": True,
        "results": service.process(payload),
    }
