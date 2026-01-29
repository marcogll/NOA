from fastapi import FastAPI
from app.config import settings
from app.routes import webhooks

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.get("/")
async def root():
    return {"message": "Welcome to NOA API", "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(webhooks.router, prefix=settings.API_V1_STR, tags=["webhooks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
