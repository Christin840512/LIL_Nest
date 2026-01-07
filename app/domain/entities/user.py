from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class AdminUser:
    id: int
    username: str
    password_hash: str
    last_login_at: Optional[datetime] = None

    def record_login(self, when: Optional[datetime] = None) -> None:
        self.last_login_at = when or datetime.now()