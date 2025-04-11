from fastapi import FastAPI
from app.routers.tasks_router import router as tasks_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Task Manager API"}

# Include the tasks router
app.include_router(tasks_router)
