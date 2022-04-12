import argon2
from pydantic import SecretStr

from server.application.auth.passwords import PasswordEncoder


class Argon2PasswordEncoder(PasswordEncoder):
    def __init__(self) -> None:
        self._hasher = argon2.PasswordHasher()

    def hash(self, password: SecretStr) -> str:
        return self._hasher.hash(password.get_secret_value())

    def verify(self, password: SecretStr, hash: str) -> bool:
        try:
            return self._hasher.verify(hash, password.get_secret_value())
        except argon2.exceptions.VerificationError:
            return False
        except argon2.exceptions.InvalidHash:
            return False
