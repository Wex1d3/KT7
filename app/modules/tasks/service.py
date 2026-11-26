from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.tasks.models import Task
from app.modules.projects.models import Project
from app.modules.tasks.schemas import TaskCreate
from app.tasks import send_task_created_notification

def create_task(data: TaskCreate, user_id: int, db: Session) -> Task:
    project = db.query(Project).filter(Project.id == data.project_id, Project.owner_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task(title=data.title, project_id=data.project_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    try:
        send_task_created_notification.delay(task.id, task.title)
    except Exception:
        # API remains usable if the worker is temporarily unavailable.
        pass
    return task
