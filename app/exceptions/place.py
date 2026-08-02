class PlaceAlreadyExistsError(Exception):
    def __init__(self, seat: str):
        super().__init__("Place already exsist")


class PlaceNotFoundError(Exception):
    def __init__(self, seat: str):
        super().__init__("Place not found")
