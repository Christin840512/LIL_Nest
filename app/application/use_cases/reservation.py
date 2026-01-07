from dataclasses import dataclass

from application.dtos.reservation import ReservationCreateCommand, ReservationResult
from domain.entities.reservation import Reservation
from domain.exceptions.reservation import ReservationValidationError
from domain.ports.reservation_repository import IReservationRepository

@dataclass
class DraftReservationUseCase:
    repo: IReservationRepository
    def execute(self, cmd: ReservationCreateCommand) -> Reservation:
        if cmd.court_name is None or cmd.court_name.strip() == "":
            raise ReservationValidationError("Court name cannot be empty.")
        if cmd.starts_at is None:
            raise ReservationValidationError("Start time is required.")

        # 交給 repo 做交易處理與 player upsert/關聯
        return ReservationResult




