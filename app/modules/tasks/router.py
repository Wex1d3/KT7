from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.tasks.schemas import TaskCreate, TaskOut
from app.modules.tasks.service import create_task
from app.modules.tasks.models import Task
from app.modules.projects.models import Project

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut, status_code=201)
def add_task(data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_task(data, user.id, db)

@router.get("", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Task).join(Project).filter(Project.owner_id == user.id).all()
