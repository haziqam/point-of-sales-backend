from fastapi import HTTPException, Request
from exceptions.auth_exception import ExpiredToken, InvalidToken
from infrastructure.adapters.rest.utils.jwt_utils import verify_jwt


def cashier_or_manager_auth_middleware(request: Request):
    token = request.cookies.get("user-jwt", None)
    if token is None:
        raise HTTPException(
            status_code=401, detail="Manager token unavailable. Please log in"
        )
    try:
        payload = verify_jwt(token)
        role = payload["role"]
        if role != "MANAGER" and role != "CASHIER":
            raise HTTPException(
                status_code=403,
                detail="Request unauthorized for roles other than MANAGER or CASHIER",
            )
    except ExpiredToken:
        raise HTTPException(
            status_code=401, detail="Manager token expired. Please relog in"
        )
    except InvalidToken:
        raise HTTPException(
            status_code=401, detail="Manager token invalid. Please relog in"
        )
