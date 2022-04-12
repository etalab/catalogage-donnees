import secrets

from pydantic import SecretStr


class PasswordEncoder:
    def hash(self, password: SecretStr) -> str:
        raise NotImplementedError  # pragma: no cover

    def verify(self, password: SecretStr, hash: str) -> bool:
        raise NotImplementedError  # pragma: no cover


API_TOKEN_LENGTH = 64


def generate_api_token() -> str:
    nbytes = API_TOKEN_LENGTH // 2
    return secrets.token_hex(nbytes)
