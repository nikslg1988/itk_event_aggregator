class TicketNotFoundError(Exception):
    pass


class SeatUnavailableError(Exception):
    def __init__(self, seat: str):
        super().__init__(f"Seat '{seat}' is unavailable")
