#!/bin/bash

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$ROOT/scripts/lib/colors.sh"
source "$ROOT/scripts/lib/logger.sh"
source "$ROOT/scripts/lib/banner.sh"

source "$ROOT/scripts/modules/system.sh"
source "$ROOT/scripts/modules/docker.sh"
source "$ROOT/scripts/modules/network.sh"
source "$ROOT/scripts/modules/prometheus.sh"
source "$ROOT/scripts/modules/alertmanager.sh"
source "$ROOT/scripts/modules/blackbox.sh"
source "$ROOT/scripts/modules/backup.sh"
source "$ROOT/scripts/modules/telegram.sh"

banner

echo
info "Running Homelab Guardian Doctor..."
echo

score=100

check () {

    if "$1"; then
        ok "$2"
    else
        fail "$2"
        score=$((score-10))
    fi

}

check docker_status "Docker Engine"
check internet "Internet Connectivity"
check dns "DNS Resolution"
check prometheus "Prometheus"
check alertmanager "Alertmanager"
check blackbox "Blackbox Exporter"

echo

info "System Information"

echo
check_cpu
echo
check_ram
echo
check_disk
echo
check_uptime

echo

info "Running Containers"

running_containers

echo

info "Stopped Containers"

stopped_containers

echo

backup=$(latest_backup)

if [ -n "$backup" ]; then
    ok "Latest Backup"
    echo "$backup"
else
    warn "No Backup Found"
    score=$((score-10))
fi

echo

echo "Health Score : $score / 100"

if [ "$score" -ge 90 ]; then
    ok "System Healthy"
elif [ "$score" -ge 70 ]; then
    warn "System Needs Attention"
else
    fail "System Critical"
fi

log "Doctor completed with score $score"
