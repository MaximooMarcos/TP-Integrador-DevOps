import random
import time
import httpx

BASE_URL = "http://localhost:8000"

ENDPOINTS = [
    ("GET", "/health"),
    ("GET", "/projects"),
    ("GET", "/tasks"),
    ("GET", "/incidents"),
    ("GET", "/projects/1"),
    ("GET", "/tasks/1"),
    ("GET", "/incidents/1"),
    ("GET", "/projects/999"),  # Intencional: Genera HTTP 404 para medir tasa de errores
    ("GET", "/tasks/999"),     # Intencional: Genera HTTP 404
]


def run_traffic():
    print("🚀 Iniciando el generador de tráfico simulado para DevFlow...")
    print("Presioná Ctrl + C para detener el script.\n")

    total_requests = 0
    success_count = 0
    error_count = 0

    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        while True:
            method, path = random.choice(ENDPOINTS)
            try:
                response = client.request(method, path)
                total_requests += 1

                if response.status_code < 400:
                    success_count += 1
                    status_symbol = "✅"
                else:
                    error_count += 1
                    status_symbol = "⚠️"

                print(
                    f"{status_symbol} [{response.status_code}] {method} {path} - "
                    f"Éxitos: {success_count} | Errores: {error_count} | Total: {total_requests}"
                )
            except Exception as e:
                print(f"❌ Error al conectar con la API: {e}")

            time.sleep(random.uniform(0.2, 1.0))


if __name__ == "__main__":
    run_traffic()