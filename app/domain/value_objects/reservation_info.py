from dataclasses import dataclass

@dataclass
class ReservationInfo:
    id: str
    players: list[str]