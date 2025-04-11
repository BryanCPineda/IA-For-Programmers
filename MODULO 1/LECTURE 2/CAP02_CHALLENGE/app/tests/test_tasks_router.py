"""
Test module for the tasks router.
This module contains unit tests for all task-related endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app
from app.models import Task
from app.db import FakeDB

# Create a test client
client = TestClient(app)

# Setup test data
@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    """Setup test data before running tests"""
    # Clear existing data
    client.delete("/tasks/all")
    
    # Add test tasks
    task1 = {
        "title": "Test Task 1",
        "description": "Description 1",
        "completed": False
    }
    task2 = {
        "title": "Test Task 2",
        "description": "Description 2",
        "completed": True
    }
    
    client.post("/tasks", json=task1)
    client.post("/tasks", json=task2)
    
    yield
    
    # Cleanup after all tests
    client.delete("/tasks/all")

# Test cases for endpoints
def test_get_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API"}

def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "New Task",
        "description": "New Description",
        "completed": False
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    assert response.json()["title"] == "New Task"
    assert response.json()["description"] == "New Description"
    assert response.json()["completed"] == False
    assert "id" in response.json()

def test_get_all_tasks():
    """Test getting all tasks"""
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()["tasks"]
    # We should have at least 3 tasks (2 from setup + 1 from test_create_task)
    assert len(tasks) >= 3
    # Check if our test tasks are in the list
    titles = [task["title"] for task in tasks]
    assert "Test Task 1" in titles
    assert "Test Task 2" in titles

def test_get_task():
    """Test getting a specific task"""
    # First get all tasks to find a valid ID
    response = client.get("/tasks")
    tasks = response.json()["tasks"]
    task_id = tasks[0]["id"]
    
    # Get existing task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Get non-existent task
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task():
    """Test updating a task"""
    # First get all tasks to find a valid ID
    response = client.get("/tasks")
    tasks = response.json()["tasks"]
    task_id = tasks[0]["id"]
    
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    
    # Update existing task
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["completed"] == True
    
    # Update non-existent task
    response = client.put("/tasks/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task():
    """Test deleting a task"""
    # Create a task to delete
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "completed": False
    }
    response = client.post("/tasks", json=task_data)
    task_id = response.json()["id"]
    
    # Delete existing task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
    
    # Verify task was deleted
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    
    # Delete non-existent task
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_all_tasks():
    """Test deleting all tasks"""
    # First create some tasks to ensure we have data
    task_data = {
        "title": "Task for deletion test",
        "description": "This task will be deleted in bulk",
        "completed": False
    }
    client.post("/tasks", json=task_data)
    client.post("/tasks", json=task_data)
    
    # First verify we have tasks
    response = client.get("/tasks")
    assert len(response.json()["tasks"]) > 0
    
    # Delete all tasks
    response = client.delete("/tasks/all")
    assert response.status_code == 200
    assert response.json()["message"] == "All tasks deleted successfully"
    
    # Verify all tasks were deleted
    response = client.get("/tasks")
    assert len(response.json()["tasks"]) == 0
