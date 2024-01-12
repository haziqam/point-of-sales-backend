from fastapi import HTTPException, Request
from exceptions.auth_exception import ExpiredToken, InvalidToken
from infrastructure.adapters.rest.utils.jwt_utils import verify_jwt
from infrastructure.adapters.rest.controllers.cashier import PurchaseSchema


def member_auth_middleware(request: Request):
    token = request.cookies.get("member-jwt", None)
    if token is None:
        raise HTTPException(
            status_code=401, detail="Member token unavailable. Please log in"
        )
    try:
        payload = verify_jwt(token)
        id_from_token = payload.get("id", None)
        id_from_query = request.query_params.get("id", None)
        if id_from_token is None:
            raise HTTPException(
                status_code=401, detail="Member token invalid. Please log in."
            )

        if id_from_query is not None:
            if id_from_token != id_from_query:
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden: not allowed to manipulate other member data",
                )
    except ExpiredToken:
        raise HTTPException(
            status_code=401, detail="Member token expired. Please relog in"
        )
    except InvalidToken:
        raise HTTPException(
            status_code=401, detail="Member token invalid. Please relog in"
        )


def member_payment_auth_middleware(schema: PurchaseSchema, request: Request):
    id_from_request_body = schema.member_id
    # Payment without membership
    if id_from_request_body is None:
        return

    # Payment with membership
    try:
        token = request.cookies.get("member-jwt", None)
        if token is None:
            raise HTTPException(
                status_code=401, detail="Member token is missing. Please log in"
            )
        payload = verify_jwt(token)
        id_from_token = payload.get("id", None)
        if id_from_token != id_from_request_body:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: not allowed to manipulate other member data",
            )
    except ExpiredToken:
        raise HTTPException(
            status_code=401, detail="Member token expired. Please relog in"
        )
    except InvalidToken:
        raise HTTPException(
            status_code=401, detail="Member token invalid. Please relog in"
        )
