class InvalidMove(Exception):
    pass


class GameExpired(Exception):
    pass


class GameFinished(Exception):
    def __init__(self, status: str):
        super().__init__(f"Game already {status}")
        self.status = status
