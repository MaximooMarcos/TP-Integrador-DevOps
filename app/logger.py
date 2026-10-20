import json
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class JSONLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000, 2)

        log_payload = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": (
                "INFO"
                if response.status_code < 400
                else "WARNING"
                if response.status_code < 500
                else "ERROR"
            ),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "message": (
                "Request procesada exitosamente"
                if response.status_code < 400
                else "Error en la solicitud"
            ),
        }

        print(json.dumps(log_payload), flush=True)
        return response