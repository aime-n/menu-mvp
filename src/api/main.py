"""
FastAPI app entrypoint.

- Creates FastAPI instance.
- Includes API routes.
- Runs with uvicorn in dev.
"""
from api.routers.plan import router as plan_router
from api.routers.recipes import router as recipes_router
from fastapi import FastAPI

app = FastAPI(title="Menu AI MVP Backend", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.include_router(plan_router, prefix="/plan")
app.include_router(recipes_router, prefix="/recipes")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="trace")
# Run with: uvicorn src.api.main:app --reload