from typing import Optional
from pydantic import BaseModel, Field


class Project(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., example="Plataforma E-commerce")
    description: str = Field(..., example="Rediseño del backend de pagos")
    status: str = Field("active", example="active")


class Task(BaseModel):
    id: Optional[int] = None
    project_id: int = Field(..., example=1)
    title: str = Field(..., example="Configurar CI/CD Pipeline")
    assigned_to: str = Field(..., example="DevOps Engineer")
    status: str = Field("todo", example="in_progress")


class Incident(BaseModel):
    id: Optional[int] = None
    project_id: int = Field(..., example=1)
    title: str = Field(..., example="Elevada latencia en API de usuarios")
    severity: str = Field("high", example="high")
    status: str = Field("open", example="open")