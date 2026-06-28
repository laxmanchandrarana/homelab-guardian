AUTO_HEAL_SERVICES = {
    "n8n",
    "nextcloud",
    "nextcloud-db",
    "prometheus",
    "grafana",
    "alertmanager",
    "cadvisor",
    "node-exporter",
    "blackbox-exporter",
    "smartctl-exporter",
    "watchtower",
    "portainer",
    "backup-api",
    "backup-ui",
}

from guardian.healing.config import AUTO_HEAL_SERVICES

service = incident["service"]

if service not in AUTO_HEAL_SERVICES:
    return {
        "success": False,
        "action": "ignored",
        "reason": "Auto-heal disabled",
    }


