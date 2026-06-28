from dataclasses import dataclass
from typing import Optional


@dataclass
class AutomationRule:
    id: Optional[int]
    name: str
    trigger: str
    target: str
    action: str
    cooldown: int
    retries: int
    timeout: int
    priority: int
    enabled: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class AutomationJob:
    id: Optional[int]
    rule_id: int
    service: str
    status: str
    progress: int = 0
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: float = 0
    exit_code: Optional[int] = None


@dataclass
class AutomationLog:
    id: Optional[int]
    job_id: int
    timestamp: str
    level: str
    message: str
