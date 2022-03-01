import argon2

from server.application.auth.passwords import PasswordEncoder


class Argon2PasswordEncoder(PasswordEncoder):
    def __init__(self) -> None:
        self._hasher = argon2.PasswordHasher()

    def hash(self, value: str) -> str:
        return self._hasher.hash(value)

    def verify(self, password: str, hash: str) -> bool:
        try:
            return self._hasher.verify(hash, password)
        except (argon2.exceptions.VerificationError, argon2.exceptions.InvalidHash):
            return False
