class EventNotFoundError(Exception):
    def __init__(self, message: str = "Event not found"):
        super().__init__(message)


class EventNotPublishedError(Exception):
    pass


class EventRegistrationClosedError(Exception):
    pass
