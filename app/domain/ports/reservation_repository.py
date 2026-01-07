from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.reservation import Reservation

@abstractmethod
class IReservationRepository(ABC):
    """Port for persisting reservations."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Reservation]:
        """Return the reservation by ID, or None if not found."""
        raise NotImplementedError

    @abstractmethod
    def save(self, reservation: Reservation) -> None:
        """Create or update the reservation."""
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, reservation: Reservation) -> None:
        """Delete the reservation."""
        raise NotImplementedError
    
    @abstractmethod
    def list_all(self) -> list[Reservation]:
        """Return a list of all reservations."""
        raise NotImplementedError

