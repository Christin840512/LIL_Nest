from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from domain.entities.player import Player as PlayerEntity
from domain.enums.payment import PaymentStatus
from domain.ports.player_repository import IPlayerRepository
from infrastructure.database.models.player import Player as PlayerModel


def _to_entity(m: PlayerModel) -> PlayerEntity:
    return PlayerEntity(
        id=m.id,
        name=m.name,
        created_at=m.created_at,
    )

def _apply_model(m: PlayerModel, e: PlayerEntity) -> None:
    m.id = e.id
    m.name = e.name
    m.created_at = e.created_at
    

class PlayerRepository(IPlayerRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, player: PlayerEntity) -> None:
        m = PlayerModel(id=player.id)
        if not self.get_by_id(player.id):
            _apply_model(m, player)
            self.db.add(m)
            self.db.commit()

    def get_by_id(self, player_id: int) -> Optional[PlayerEntity]:
        m = self.db.get(PlayerModel, player_id)
        return _to_entity(m) if m else None
    
    def get_by_name(self, name: str) -> Optional[PlayerEntity]:
        m = self.db.query(PlayerModel).filter(PlayerModel.name == name).first()
        return _to_entity(m) if m else None
