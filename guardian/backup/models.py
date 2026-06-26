from dataclasses import dataclass
from datetime import datetime


@dataclass
class BackupJob:
    name: str
    backup_type: str
    destination: str
    created: datetime
    status: str
    size: int = 0
