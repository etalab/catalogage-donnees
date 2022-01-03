import argon2
from argon2.exceptions import InvalidHash, VerificationError

_hasher = argon2.PasswordHasher()


def hash(plain: str) -> str:
    return _hasher.hash(plain)


def verify(password: str, hashed: str) -> bool:
    try:
        _hasher.verify(hashed, password)
    except (InvalidHash, VerificationError):
        return False
    else:
        return True
