from server.application.auth.passwords import generate_api_token
from server.infrastructure.auth.passwords import Argon2PasswordEncoder


def test_generate_api_token() -> None:
    api_token = generate_api_token()
    assert len(api_token) == 64
    assert api_token.isalnum()


def test_argon2_password_encoder() -> None:
    encoder = Argon2PasswordEncoder()
    hsh = encoder.hash("s3kr3t")
    assert encoder.verify("s3kr3t", hsh)
    assert not encoder.verify("other", hsh)
    assert not encoder.verify("s3kr3t", "invalidhash")
