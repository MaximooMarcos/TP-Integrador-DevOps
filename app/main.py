import json
import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import projects, tasks, incidents

# Configuración del Logger estructurado en JSON para Observabilidad
logger = logging.getLogger("devflow-logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()


class JSONFormatter(loggin.Formatter if "logging" in globals() else logging.Formatter):  # estándar
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_info"):
            log_data.update(record.extra_info)
        return json.dumps(log_data)


handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

app = FastAPI(
    title="DevFlow API",
    description="API REST de Gestión IT de Proyectos, Tareas e Incidentes",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para Logs Estructurados en JSON (Middleware de Observabilidad)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    log_extra = {
        "extra_info": {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "client_ip": (
                request.client.host if request.client else "unknown"
            ),
        }
    }
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code}",
        extra=log_extra,
    )
    return response


# Montar archivos estáticos del Frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir Routers
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(incidents.router)

# Instrumentación de Prometheus (expone automáticamente el endpoint /metrics)
Instrumentator().instrument(app).expose(app)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():
    return FileResponse("app/static/index.html")