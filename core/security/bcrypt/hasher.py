from core.security.hasher import PasswordHasher

import bcrypt

class BCryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def verify_password(self, entered_password: str, stored_password: str) -> bool:
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))