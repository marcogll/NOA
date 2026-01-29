from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import webhooks
from app.db.async_session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown - clean up resources
    pass


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Welcome to NOA API", "version": settings.VERSION}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "database": "initialized",
        "webhooks": "configured",
    }


app.include_router(webhooks.router, prefix=settings.API_V1_STR, tags=["webhooks"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=2311)
