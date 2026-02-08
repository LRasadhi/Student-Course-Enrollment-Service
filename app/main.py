"""Student Course Enrollment Service - FastAPI application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import engine, Base
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Course Enrollment Service",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def root():
    """Health check."""
    return {"message": "Student Course Enrollment API"}
