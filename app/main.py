from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.modules.auth.router import router as auth_router
from app.modules.tasks.router import router as tasks_router
from app.modules.projects.router import router as projects_router
from app.main_limiter import limiter
from app.modules.auth import models as auth_models
from app.modules.projects import models as project_models
from app.modules.tasks import models as task_models

# For a first local launch. In production, use: alembic upgrade head
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KT6 Fullstack API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)

@app.get("/", tags=["health"])
def root():
    return {"message": "KT6 Fullstack API is running"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
