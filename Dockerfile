# ---------- Aşama 1: bağımlılıkların derlenmesi ----------
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Aşama 2: minimal çalışma imajı ----------
FROM python:3.12-slim
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/devopsuser/.local/bin:$PATH

RUN adduser --disabled-password --gecos "" --uid 1000 devopsuser
WORKDIR /app
COPY --from=builder --chown=devopsuser:devopsuser /root/.local /home/devopsuser/.local
COPY --chown=devopsuser:devopsuser app/ ./app/

USER 1000
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
