from sqlalchemy.orm import Session
from app.modules.projects.models import Project
from app.modules.projects.schemas import ProjectCreate

def create_project(data: ProjectCreate, owner_id: int, db: Session) -> Project:
    project = Project(**data.model_dump(), owner_id=owner_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
