from api.routers.chat import router as chat_router
from fastapi import FastAPI
from api.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, 
              version=settings.PROJECT_VERSION)

app.include_router(chat_router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
# Run with: uvicorn api.main:app --reload