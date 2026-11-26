from celery import Celery
from app.core.config import settings

celery_app = Celery("kt6_tasks", broker=settings.redis_url, backend=settings.redis_url)

@celery_app.task(name="send_task_created_notification")
def send_task_created_notification(task_id: int, title: str):
    # Demo background action: worker logs the notification event.
    print(f"[NOTIFICATION] Task #{task_id} created: {title}")
    return {"task_id": task_id, "sent": True}
