from security.hasher import IPasswordHasher


class SecurityContainer:
    def __init__(self, hasher: IPasswordHasher) -> None:
        self.hasher = hasher
