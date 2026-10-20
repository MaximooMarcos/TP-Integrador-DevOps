from fastapi import FastAPI
from app.logger import JSONLogMiddleware
from app.routers import incidents, projects, tasks

app = FastAPI(
    title="DevFlow API",
    description="Plataforma de gestión de Proyectos, Tareas e Incidentes IT (DevOps TP Integrador)",
    version="1.0.0",
)

# Registrar Middleware de Logging JSON
app.add_middleware(JSONLogMiddleware)

# Registrar Routers
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(incidents.router)


@app.get("/", tags=["General"])
def read_root():
    return {
        "app": "DevFlow API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["General"])
def health_check():
    return {"status": "healthy", "database": "connected_in_memory"}