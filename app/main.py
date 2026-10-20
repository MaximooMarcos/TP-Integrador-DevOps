from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.logger import JSONLogMiddleware
from app.routers import incidents, projects, tasks

app = FastAPI(
    title="DevFlow API",
    description="Plataforma de gestión de Proyectos, Tareas e Incidentes IT (DevOps TP Integrador)",
    version="1.0.0",
)

# Registrar Middleware de Logging JSON
app.add_middleware(JSONLogMiddleware)

# Montar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registrar Routers de la API
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(incidents.router)


@app.get("/", tags=["UI"])
def read_dashboard():
    return FileResponse("app/static/index.html")


@app.get("/health", tags=["General"])
def health_check():
    return {"status": "healthy", "database": "connected_in_memory"}