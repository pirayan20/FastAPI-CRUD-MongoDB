from pydantic import BaseModel


class Vote(BaseModel):
    name: str
    count: int
