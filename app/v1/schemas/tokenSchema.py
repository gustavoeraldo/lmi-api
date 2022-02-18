from pydantic import BaseModel
from typing import Optional


class TokenSchema(BaseModel):
    access_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNjQ0MTkyODkwfQ.Fyc5AmyyxADRhmtD03miLkOruzayKiGvgJUeDsTj5w0"
    token_type: Optional[str] = "Bearer"


class TokenPayload(BaseModel):
    id: Optional[int]
