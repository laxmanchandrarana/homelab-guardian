from threading import Thread

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from guardian.api.websocket_manager import manager
from guardian.api.routes import router
from guardian.api.monitoring import router as monitoring_router
from guardian.api.backup import router as backup_router
from guardian.api.restore import router as restore_router
from guardian.api.incidents import router as incident_router
from guardian.api.alerts import router as alerts_router
from guardian.api.ai import router as ai_router
from guardian.api.prediction import router as prediction_router
from guardian.api.automation import router as automation_router
from guardian.api.automation_ai import router as automation_ai_router

from guardian.monitoring.daemon import GuardianDaemon


app = FastAPI(
    title="Homelab Guardian",
    description="Self Healing Homelab",
    version="0.1.0",
)

# -------------------------------------------------------
# CORS Configuration
# -------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://guardian.atmakriti.com",
        "https://api-guardian.atmakriti.com",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_origin_regex=r"https://.*\.lovable\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Startup
# -------------------------------------------------------

@app.on_event("startup")
def start_guardian_daemon():
    daemon = GuardianDaemon()

    Thread(
        target=daemon.run,
        daemon=True,
    ).start()


# -------------------------------------------------------
# WebSocket
# -------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket)


# -------------------------------------------------------
# API Routers
# -------------------------------------------------------

app.include_router(router)
app.include_router(monitoring_router)
app.include_router(backup_router)
app.include_router(restore_router)
app.include_router(incident_router)
app.include_router(alerts_router)
app.include_router(ai_router)
app.include_router(prediction_router)
app.include_router(automation_router)
app.include_router(automation_ai_router)

