from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = ROOT / "config"

LOG_DIR = ROOT / "logs"

BACKUP_DIR = Path("/mnt/storage/Backup/backups")

DATABASE = ROOT / "guardian.db"

VERSION = "0.1.0"

APP_NAME = "Homelab Guardian"

AUTHOR = "Laxman Chandra Rana"

