from pydantic import BaseModel


class APIStatusSchema(BaseModel):
    api: bool
    redis: bool
