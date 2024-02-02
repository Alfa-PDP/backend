from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.team import TeamSchema


class GetUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    family_name: str
    middle_name: str
    position: str
    avatar: str | None
    team_id: UUID


class GetUserWithProgressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    family_name: str
    middle_name: str
    position: str
    avatar: str | None
    team_id: UUID
    task_count: int
    task_progress: int


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    family_name: str
    middle_name: str
    position: str
    avatar: str | None


class UserFilterParams(BaseModel):
    team_id: UUID | None
    year: int = 2024


class UserOrderParams(BaseModel):
    sort_by: str
    order: str

    @property
    def is_desc(self) -> bool:
        return self.order == "desc"


class UserWithTasksSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    family_name: str
    middle_name: str
    position: str
    avatar: str | None
    team: TeamSchema | None
    # tasks: list[TaskWithStatusSchema]
