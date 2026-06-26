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
