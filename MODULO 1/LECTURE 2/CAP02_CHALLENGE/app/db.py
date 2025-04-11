from typing import List, Optional
from app.models import Task

class FakeDB:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FakeDB, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.tasks = []
            self._initialized = True
            
    def add_task(self, task: Task):
        task_dict = task.dict()
        task_dict["id"] = len(self.tasks) + 1
        task_obj = Task(**task_dict)
        self.tasks.append(task_obj)
        return task_obj

    def get_task(self, task_id: int):
        task = next((task for task in self.tasks if task.id == task_id), None)
        return task

    def get_tasks(self):
        return self.tasks

    def update_task(self, task_id: int, task_update):
        for task in self.tasks:
            if task.id == task_id:
                if task_update.title is not None:
                    task.title = task_update.title
                if task_update.description is not None:
                    task.description = task_update.description
                if task_update.completed is not None:
                    task.completed = task_update.completed
                return task
        return None

    def delete_task(self, task_id: int):
        task = self.get_task(task_id)
        if task:
            self.tasks = [t for t in self.tasks if t.id != task_id]
            return True
        return False
        
    def delete_all_tasks(self):
        self.tasks = []
        return True