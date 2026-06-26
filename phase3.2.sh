# Ensure you are in your project root directory
cd ~/projects/homelab-guardian

# Step 1 — Install required packages inside the virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    pip install requests psutil
    pip freeze > requirements.txt
else
    echo "⚠️ .venv not found! Installing in current environment context."
    pip install requests psutil
fi

# Step 2 — Create Prometheus service
cat << 'EOF' > guardian/services/prometheus_service.py
import requests


class PrometheusService:

    def __init__(self):
        self.url = "http://localhost:9090"

    def targets(self):
        return requests.get(
            f"{self.url}/api/v1/targets"
        ).json()

    def alerts(self):
        return requests.get(
            f"{self.url}/api/v1/alerts"
        ).json()

    def rules(self):
        return requests.get(
            f"{self.url}/api/v1/rules"
        ).json()

    def query(self, expression):
        return requests.get(
            f"{self.url}/api/v1/query",
            params={"query": expression},
        ).json()
EOF

# Step 3 — Create Alertmanager service
cat << 'EOF' > guardian/services/alertmanager_service.py
import requests


class AlertmanagerService:

    def __init__(self):
        self.url = "http://localhost:9093"

    def alerts(self):
        return requests.get(
            f"{self.url}/api/v2/alerts"
        ).json()

    def silences(self):
        return requests.get(
            f"{self.url}/api/v2/silences"
        ).json()
EOF

# Step 4 — Create Monitoring API routes
cat << 'EOF' > guardian/api/monitoring.py
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
EOF

# Step 5 — Register the router inside guardian/api/app.py safely
cat << 'EOF' > guardian/api/app.py
from fastapi import FastAPI

from guardian.api.routes import router
from guardian.api.monitoring import router as monitoring_router

app = FastAPI(
    title="Homelab Guardian",
    description="Self Healing Homelab",
    version="0.1.0"
)

app.include_router(router)
app.include_router(monitoring_router)
EOF

# Step 6 — Restart and check the systemd API service
sudo systemctl restart homelab-guardian

echo "--------------------------------------------------------"
echo "✅ Phase 3.2 Monitoring API added and service restarted!"
echo "📡 Open http://YOUR_SERVER_IP:8008/docs to see the new /monitoring endpoints."
echo "--------------------------------------------------------"
sudo systemctl status homelab-guardian --no-pager
