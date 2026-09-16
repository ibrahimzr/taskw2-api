from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import setup_db
from app.routers.auth import auth_router
from app.routers.tasks import task_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    setup_db()
    yield

app=FastAPI(
    title="TaskFlow API",
    description="Task management API with authentication and role-based access",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(task_router)

@app.get("/",tags=["System"])
def home():
    return {"message":"TaskFlow API is running"}