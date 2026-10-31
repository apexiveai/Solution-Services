from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app import models  # noqa: F401 - register SQLAlchemy models
from app.routers import health, identity, tenants, audit
from backend.app.init_phase2 import router as phase2_router
from app.modules.telecom import models as telecom_models  # noqa: F401
from app.modules.main import router as industry_modules_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.dev_create_tables and settings.app_env == "development":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="ApexiveAI modular enterprise operations and intelligence platform.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

app.include_router(health.router)
app.include_router(identity.router)
app.include_router(tenants.router)
app.include_router(audit.router)
app.include_router(phase2_router)
app.include_router(telecom_models)
app.include_router(industry_modules_router)

@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running",
    }
