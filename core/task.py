from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Task:
    task_type: str
    data: dict

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"

    created: str = field(default_factory=lambda: datetime.now().isoformat())

    assigned_agent: str = ""

    result: dict = field(default_factory=dict)

    error: str = ""
