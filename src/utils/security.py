from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_pw(self, plain_pw: str) -> str:
        return self._pwd_context.hash(plain_pw)

    def verify(self, plain_pw: str, hash_pw: str) -> bool:
        return self._pwd_context.verify(plain_pw, hash_pw)
