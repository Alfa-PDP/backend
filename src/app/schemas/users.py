from uuid import UUID

from pydantic import Base64Bytes, BaseModel, ConfigDict  # noqa


class BaseUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    family_name: str
    middle_name: str
    position: str
    avatar: Base64Bytes | None


class UserSchema(BaseUserSchema):
    id: UUID
    team_id: UUID
    avatar: Base64Bytes | None


class UserWithTaskSchema(UserSchema):
    task_count: int
    task_progress: int


class UserCreateSchema(BaseUserSchema):
    pass


class UserFilterParams(BaseModel):
    team_id: UUID | None


class UserOrderParams(BaseModel):
    field: str
    is_desc: bool = False
