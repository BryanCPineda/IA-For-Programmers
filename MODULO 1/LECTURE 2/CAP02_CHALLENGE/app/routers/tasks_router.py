"""
Task Router Module

This module defines the API endpoints for task management operations.
It provides CRUD operations for tasks including:
- Creating new tasks
- Retrieving tasks (individual or all)
- Updating existing tasks
- Deleting tasks (individual or all)

Each endpoint is mapped to a corresponding function in the database service.
"""

from fastapi import APIRouter, HTTPException
from app.models import Task, TaskList, UpdateTaskModel
from app.db import FakeDB

router = APIRouter()
db = FakeDB()  # Use a single instance

@router.post("/tasks", status_code=201, response_model=Task)
async def create_task(task: Task):
    """
    Create a new task.
    
    Args:
        task (Task): The task data to create
        
    Returns:
        Task: The created task with assigned ID
    """
    return db.add_task(task)

@router.get("/tasks", response_model=TaskList)
async def get_tasks():
    """
    Get all tasks.
    
    Returns:
        TaskList: A list containing all tasks
    """
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)

# Important: Place the "all" endpoint BEFORE the "{task_id}" endpoint
# to ensure FastAPI routes it correctly
@router.delete("/tasks/all", status_code=200)
async def delete_all_tasks():
    """
    Delete all tasks from the database.
    
    Returns:
        dict: A message confirming all tasks were deleted
    """
    db.delete_all_tasks()
    return {"message": "All tasks deleted successfully"}

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """
    Get a specific task by ID.
    
    Args:
        task_id (int): The ID of the task to retrieve
        
    Returns:
        Task: The requested task
        
    Raises:
        HTTPException: If task with specified ID is not found
    """
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    """
    Update an existing task.
    
    Args:
        task_id (int): The ID of the task to update
        task_update (UpdateTaskModel): The data to update
        
    Returns:
        Task: The updated task
        
    Raises:
        HTTPException: If task with specified ID is not found
    """
    # Validate task exists before updating
    if db.get_task(task_id) is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    updated_task = db.update_task(task_id, task_update)
    return updated_task

@router.delete("/tasks/{task_id}", status_code=200)
async def delete_task(task_id: int):
    """
    Delete a specific task by ID.
    
    Args:
        task_id (int): The ID of the task to delete
        
    Returns:
        dict: A message confirming the task was deleted
        
    Raises:
        HTTPException: If task with specified ID is not found
    """
    # Validate task exists before deleting
    if db.get_task(task_id) is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}
