from typing import Optional
from fastapi import APIRouter, HTTPException, status
from app.database import tasks_db
from app.models import Task

router = APIRouter(prefix="/tasks", tags=["Tareas"])


@router.get("", status_code=status.HTTP_200_OK)
def get_tasks(project_id: Optional[int] = None):
    if project_id is not None:
        return [t for t in tasks_db if t.get("project_id") == project_id]
    return tasks_db


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada"
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    new_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = task.model_dump()
    new_task["id"] = new_id
    tasks_db.append(new_task)
    return new_task


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, updated_task: Task):
    for idx, task in enumerate(tasks_db):
        if task["id"] == task_id:
            updated_data = updated_task.model_dump()
            updated_data["id"] = task_id
            tasks_db[idx] = updated_data
            return updated_data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada"
    )


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    for idx, task in enumerate(tasks_db):
        if task["id"] == task_id:
            removed = tasks_db.pop(idx)
            return {"message": f"Tarea {task_id} eliminada", "task": removed}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada"
    )