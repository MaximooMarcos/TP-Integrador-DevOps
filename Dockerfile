# ==========================================
# Etapa 1: Builder (Instalación de dependencias)
# ==========================================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar e instalar dependencias en el directorio del usuario local
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Etapa 2: Runner (Imagen final de ejecución minimalista)
# ==========================================
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Crear un usuario no privilegiado (Non-root) por seguridad
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copiar únicamente los paquetes instalados desde la etapa builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar el código fuente asignando la propiedad al usuario appuser
COPY --chown=appuser:appuser . .

# Cambiar al usuario sin privilegios
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]