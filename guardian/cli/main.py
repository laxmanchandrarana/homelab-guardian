import typer

from guardian.services.docker_service import DockerService
from guardian.version import VERSION, BUILD, CODENAME

app = typer.Typer()
docker = DockerService()


@app.command()
def version():
    print(f"""
Homelab Guardian

Version : {VERSION}
Build    : {BUILD}
Codename : {CODENAME}
""")


@app.command()
def ps():
    for container in docker.containers():
        print(f"{container.name:25} {container.status}")


@app.command()
def restart(service: str):
    docker.restart(service)
    print(f"Restarted {service}")


@app.command()
def logs(service: str):
    print(docker.logs(service))


@app.command()
def doctor():
    print("Guardian Doctor is ready.")


if __name__ == "__main__":
    app()
