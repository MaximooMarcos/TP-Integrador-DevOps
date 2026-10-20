from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# 1. Pruebas de Endpoints Generales
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "DevFlow API"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# 2. Pruebas del Módulo de Proyectos
def test_get_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_project_by_id_success():
    response = client.get("/projects/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_project_by_id_not_found():
    response = client.get("/projects/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Proyecto no encontrado"


def test_create_project():
    new_project = {
        "name": "Sistema de Logs",
        "description": "Integración con ELK / Grafana",
        "status": "active",
    }
    response = client.post("/projects", json=new_project)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sistema de Logs"
    assert "id" in data


def test_update_project():
    updated_project = {
        "name": "DevFlow Core v2",
        "description": "Plataforma actualizada",
        "status": "in_progress",
    }
    response = client.put("/projects/1", json=updated_project)
    assert response.status_code == 200
    assert response.json()["name"] == "DevFlow Core v2"


# 3. Pruebas del Módulo de Tareas
def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task():
    updated_task = {
        "project_id": 1,
        "title": "Implementar endpoints CRUD",
        "assigned_to": "Marcos",
        "status": "completed",
    }
    response = client.put("/tasks/1", json=updated_task)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


# 4. Pruebas del Módulo de Incidentes
def test_get_incidents():
    response = client.get("/incidents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_incident_not_found():
    response = client.get("/incidents/999")
    assert response.status_code == 404


def test_update_incident():
    updated_incident = {
        "project_id": 1,
        "title": "Fallo resuelto y verificado",
        "severity": "low",
        "status": "closed",
    }
    response = client.put("/incidents/1", json=updated_incident)
    assert response.status_code == 200
    assert response.json()["status"] == "closed"