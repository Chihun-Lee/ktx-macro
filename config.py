"""Secret storage for Korail credentials and (optional) card info.

Backed by macOS Keychain via the `keyring` library
(`keyring.backends.macOS.Keyring`, Security.framework).

KTX uses korail2 for search/reserve. Payment goes through Playwright
browser automation against the Korail website, which needs the same
card fields as a manual checkout.
"""
from __future__ import annotations

import json
from typing import Optional

import keyring
from pydantic import BaseModel, Field

KEYRING_SERVICE = "ktx-macro"
KEYRING_USER = "config"


class Credentials(BaseModel):
    ktx_id: str = Field(min_length=1)
    ktx_password: str = Field(min_length=1)
    # card fields are optional — only required when pay_mode=auto
    card_number: str = Field(default="", max_length=19)
    card_password: str = Field(default="", max_length=2)
    card_validation: str = Field(default="", max_length=10)
    card_expire: str = Field(default="", max_length=4)
    card_installment: int = Field(default=0, ge=0, le=24)


def _read_blob() -> Optional[str]:
    return keyring.get_password(KEYRING_SERVICE, KEYRING_USER)


def exists() -> bool:
    return _read_blob() is not None


def load() -> Optional[Credentials]:
    blob = _read_blob()
    if not blob:
        return None
    try:
        return Credentials.model_validate_json(blob)
    except Exception:
        return None


def save(creds: Credentials) -> None:
    payload = creds.model_dump()
    payload["card_number"] = payload["card_number"].replace("-", "").replace(" ", "")
    keyring.set_password(KEYRING_SERVICE, KEYRING_USER, json.dumps(payload))


def clear() -> None:
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_USER)
    except keyring.errors.PasswordDeleteError:
        pass


def public_status() -> dict:
    creds = load()
    if not creds:
        return {"configured": False}
    has_card = bool(creds.card_number)
    out = {
        "configured": True,
        "ktx_id": creds.ktx_id,
        "has_card": has_card,
        "storage": "macOS Keychain",
    }
    if has_card:
        out["card_last4"] = creds.card_number[-4:]
        out["card_masked"] = "*" * (len(creds.card_number) - 4) + creds.card_number[-4:]
        out["card_installment"] = creds.card_installment
    return out
