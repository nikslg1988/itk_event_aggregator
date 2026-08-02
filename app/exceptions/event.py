class EventNotFoundError(Exception):
    def __init__(self):
        super().__init__("Event not found")


class EventNotPublishedError(Exception):
    def __init__(self):
        super().__init__("Registration is not published")


class EventRegistrationClosedError(Exception):
    def __init__(self):
        super().__init__("Registration is closed")


class EventProviderError(Exception):
    def __init__(self):
        super().__init__("External events provider is unavailable")
