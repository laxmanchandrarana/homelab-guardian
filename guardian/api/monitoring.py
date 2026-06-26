from fastapi import APIRouter

from guardian.services.prometheus_service import PrometheusService
from guardian.services.alertmanager_service import AlertmanagerService

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

prom = PrometheusService()
alert = AlertmanagerService()


@router.get("/targets")
def targets():
    return prom.targets()


@router.get("/rules")
def rules():
    return prom.rules()


@router.get("/alerts")
def alerts():
    return prom.alerts()


@router.get("/alertmanager")
def alertmanager():
    return alert.alerts()


@router.get("/silences")
def silences():
    return alert.silences()


@router.get("/query")
def query(expr: str):
    return prom.query(expr)
