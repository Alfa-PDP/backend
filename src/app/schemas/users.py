from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    family_name: str
    middle_name: str
    position: str
    avatar: str | None


class UserSchema(BaseUserSchema):
    id: UUID


class UserWithTeamIdSchema(UserSchema):
    team_id: UUID


class UserWithTaskSchema(UserWithTeamIdSchema):
    task_count: int
    task_progress: int


class UserCreateSchema(BaseUserSchema):
    pass


class UserFilterParams(BaseModel):
    team_id: UUID | None


class UserOrderParams(BaseModel):
    field: str
    is_desc: bool = False
