import secrets

API_TOKEN_LENGTH = 64


class PasswordEncoder:
    def hash(self, value: str) -> str:
        raise NotImplementedError  # pragma: no cover

    def verify(self, password: str, hash: str) -> bool:
        raise NotADirectoryError  # pragma: no cover


def generate_api_token() -> str:
    assert API_TOKEN_LENGTH % 2 == 0
    nbytes = API_TOKEN_LENGTH // 2
    return secrets.token_hex(nbytes)
