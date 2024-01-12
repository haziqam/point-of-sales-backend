from datetime import datetime, timezone, timedelta
from typing import Any, Dict
import jwt
from exceptions.auth_exception import ExpiredToken, InvalidToken

with open(".key", "r") as key_file:
    key = key_file.read().strip()


def encode_jwt(payload: Dict[str, Any], expires_in: timedelta) -> str:
    encoded = jwt.encode(
        payload={
            "exp": datetime.now(tz=timezone.utc) + expires_in,
            **payload,
        },
        key=key,
        algorithm="HS256",
    )
    return encoded


def verify_jwt(token: str) -> Dict[str, Any]:
    """
    Returns:
        Dictionary of payload

    Raises:
    * ExpiredToken
    * InvalidToken
    """
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpiredToken("Token is expired. Please relog in")
    except jwt.InvalidTokenError:
        raise InvalidToken("Token is invalid.")
