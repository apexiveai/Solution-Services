import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from app.config import settings


def _cipher() -> Fernet:
    secret = settings.automation_credential_key
    if (
        len(secret) < 32
        or secret.lower() in {"change-me", "changethis", "development"}
        or "change_this" in secret.lower()
    ):
        raise RuntimeError(
            "AEOP_AUTOMATION_CREDENTIAL_KEY must be configured with at least 32 characters "
            "before the credential vault can be used."
        )
    key = base64.urlsafe_b64encode(hashlib.sha256(secret.encode("utf-8")).digest())
    return Fernet(key)


def encrypt_secret(secret: str) -> str:
    return _cipher().encrypt(secret.encode("utf-8")).decode("ascii")


def decrypt_secret(ciphertext: str) -> str:
    try:
        return _cipher().decrypt(ciphertext.encode("ascii")).decode("utf-8")
    except InvalidToken as exc:
        raise RuntimeError("Credential ciphertext could not be authenticated") from exc
