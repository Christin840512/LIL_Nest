from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user import AdminUser


class IAdminUserRepository(ABC):
    """Port for persisting the single admin user."""

    @abstractmethod
    def get_admin(self) -> Optional[AdminUser]:
        """Return the (only) admin, or None if not initialized."""
        raise NotImplementedError

    @abstractmethod
    def save_admin(self, admin: AdminUser) -> AdminUser:
        """Create or update the admin user."""
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[AdminUser]:
        """Return the admin user by ID, or None if not found."""
        raise NotImplementedError
    