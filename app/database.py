# Base de datos en memoria para DevFlow
projects_db = [
    {
        "id": 1,
        "name": "DevFlow Core",
        "description": "Gestor de proyectos e incidentes IT",
        "status": "active",
    },
    {
        "id": 2,
        "name": "Migración Cloud",
        "description": "Migración de infraestructura a AWS",
        "status": "planning",
    },
]

tasks_db = [
    {
        "id": 1,
        "project_id": 1,
        "title": "Implementar endpoints REST",
        "assigned_to": "Marcos",
        "status": "completed",
    },
    {
        "id": 2,
        "project_id": 1,
        "title": "Dockerizar aplicación",
        "assigned_to": "Marcos",
        "status": "in_progress",
    },
]

incidents_db = [
    {
        "id": 1,
        "project_id": 1,
        "title": "Fallo de conexión a base de datos",
        "severity": "critical",
        "status": "resolved",
    }
]