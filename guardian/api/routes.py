from fastapi import APIRouter

from guardian.services.docker_service import DockerService
from guardian.core.health import Health

router = APIRouter()

docker = DockerService()
health = Health()


@router.get("/")
def root():
    return {
        "project": "Homelab Guardian",
        "status": "running"
    }


@router.get("/health")
def health_api():
    return {
        "cpu": health.cpu(),
        "memory": health.memory(),
        "disk": health.disk()
    }


@router.get("/containers")
def containers():
    result = []

    for c in docker.containers():
        result.append({
            "name": c.name,
            "status": c.status,
            "image": c.image.tags,
            "id": c.short_id
        })

    return result


@router.post("/restart/{container}")
def restart(container: str):

    docker.restart(container)

    return {
        "status": "restarted",
        "container": container
    }


@router.get("/logs/{container}")
def logs(container: str):

    return {
        "logs": docker.logs(container)
    }

@router.get("/containers/{name}")
def container(name: str):
    c = docker.get(name)

    return {
        "id": c.short_id,
        "name": c.name,
        "status": c.status,
        "image": c.image.tags,
        "created": c.attrs["Created"]
    }


@router.get("/stats/{name}")
def stats(name: str):
    return docker.stats(name)


@router.get("/inspect/{name}")
def inspect(name: str):
    return docker.inspect(name)


@router.post("/start/{name}")
def start(name: str):
    docker.start(name)
    return {"status": "started", "container": name}


@router.post("/stop/{name}")
def stop(name: str):
    docker.stop(name)
    return {"status": "stopped", "container": name}


@router.post("/restart/{name}")
def restart(name: str):
    docker.restart(name)
    return {"status": "restarted", "container": name}


@router.delete("/remove/{name}")
def remove(name: str):
    docker.remove(name)
    return {"status": "removed", "container": name}


@router.get("/logs/{name}")
def logs(name: str):
    return {"logs": docker.logs(name)}
