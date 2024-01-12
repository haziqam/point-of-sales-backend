from pydantic import BaseModel


class ResponseMessageSchema(BaseModel):
    message: str
