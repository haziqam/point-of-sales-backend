class UserNotFound(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidToken(Exception):
    pass


class ExpiredToken(Exception):
    pass
