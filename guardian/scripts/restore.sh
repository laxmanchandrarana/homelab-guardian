#!/bin/bash

set -e

BACKUP="$1"

echo "Restoring..."

tar -xzpf "$BACKUP" -C /

echo "Restore Finished"
