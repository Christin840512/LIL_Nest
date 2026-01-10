from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.player import Player


class IPlayerRepository(ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Player]: ...

    @abstractmethod
    def get_by_id(self, player_id: int) -> Optional[Player]: ...

    @abstractmethod
    def create(self, name: str) -> Player: ...
