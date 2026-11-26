from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.projects.schemas import ProjectCreate, ProjectOut
from app.modules.projects.service import create_project
from app.modules.projects.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectOut, status_code=201)
def add_project(data: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_project(data, user.id, db)

@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Project).filter(Project.owner_id == user.id).all()
