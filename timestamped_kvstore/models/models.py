from pydantic import BaseModel


class KeyTimestamp(BaseModel):
    key: str
    timestamp: int


class UpdateValue(KeyTimestamp):
    value: str
