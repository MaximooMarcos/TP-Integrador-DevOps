from fastapi import APIRouter, HTTPException, status
from app.database import projects_db
from app.models import Project

router = APIRouter(prefix="/projects", tags=["Proyectos"])


@router.get("", status_code=status.HTTP_200_OK)
def get_projects():
    return projects_db


@router.get("/{project_id}", status_code=status.HTTP_200_OK)
def get_project(project_id: int):
    for project in projects_db:
        if project["id"] == project_id:
            return project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(project: Project):
    new_id = max([p["id"] for p in projects_db], default=0) + 1
    new_project = project.model_dump()
    new_project["id"] = new_id
    projects_db.append(new_project)
    return new_project

@router.put("/{project_id}", status_code=status.HTTP_200_OK)
def update_project(project_id: int, updated_project: Project):
    for idx, project in enumerate(projects_db):
        if project["id"] == project_id:
            updated_data = updated_project.model_dump()
            updated_data["id"] = project_id
            projects_db[idx] = updated_data
            return updated_data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
    )


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(project_id: int):
    for idx, project in enumerate(projects_db):
        if project["id"] == project_id:
            removed = projects_db.pop(idx)
            return {
                "message": f"Proyecto {project_id} eliminado",
                "project": removed,
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
    )