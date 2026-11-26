from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    project_id: int

class TaskOut(BaseModel):
    id: int
    title: str
    is_done: bool
    project_id: int
    model_config = ConfigDict(from_attributes=True)
