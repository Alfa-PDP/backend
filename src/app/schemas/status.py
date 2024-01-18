from pydantic import BaseModel


class StatusSchema(BaseModel):
    api: bool
    redis: bool
