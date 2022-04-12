from pydantic import SecretStr

from server.application.auth.passwords import generate_api_token
from server.infrastructure.auth.passwords import Argon2PasswordEncoder


def test_generate_api_token() -> None:
    api_token = generate_api_token()
    assert len(api_token) == 64
    assert api_token.isalnum()


def test_argon2_password_encoder() -> None:
    password = SecretStr("s3kr3t")
    encoder = Argon2PasswordEncoder()
    hash_ = encoder.hash(password)
    assert encoder.verify(password, hash_)
    assert not encoder.verify(SecretStr("other"), hash_)
    assert not encoder.verify(password, "invalidhash")
