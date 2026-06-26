from fastapi import FastAPI

from guardian.api.routes import router
from guardian.api.monitoring import router as monitoring_router
from guardian.api.backup import router as backup_router
from guardian.api.restore import router as restore_router

app = FastAPI(
    title="Homelab Guardian",
    description="Self Healing Homelab",
    version="0.1.0"
)

app.include_router(router)
app.include_router(monitoring_router)
app.include_router(backup_router)
app.include_router(restore_router)

