#!/bin/bash

set -e

BACKUP_ROOT="/mnt/storage/Backup/backups"
DATE=$(date +"%Y%m%d-%H%M%S")

mkdir -p "$BACKUP_ROOT"

echo "Backing up server-services..."

tar \
    --warning=no-file-changed \
    --ignore-failed-read \
    -czpf \
"$BACKUP_ROOT/server-services-$DATE.tar.gz" \
/home/sonjoy/server-services

echo "Backup completed."
