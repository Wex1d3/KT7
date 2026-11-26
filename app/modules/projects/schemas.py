from pydantic import BaseModel, ConfigDict, Field

class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = ""

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
