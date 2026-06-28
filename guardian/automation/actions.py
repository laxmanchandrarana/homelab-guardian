import subprocess
import shlex
import requests


class AutomationError(Exception):
    pass


def run_command(command: str):
    process = subprocess.run(
        shlex.split(command),
        capture_output=True,
        text=True,
    )

    return {
        "success": process.returncode == 0,
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
        "returncode": process.returncode,
    }


def restart_container(container: str):
    return run_command(f"docker restart {container}")


def stop_container(container: str):
    return run_command(f"docker stop {container}")


def start_container(container: str):
    return run_command(f"docker start {container}")


def restart_compose_stack(path: str):
    return run_command(f"docker compose -f {path} restart")


def restart_service(service: str):
    return run_command(f"sudo systemctl restart {service}")


def run_shell_script(script: str):
    return run_command(script)


def webhook(url: str, payload: dict):
    response = requests.post(url, json=payload, timeout=20)

    return {
        "success": response.ok,
        "status": response.status_code,
        "body": response.text,
    }
