FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 10002 --shell /usr/sbin/nologin appuser

WORKDIR /app
COPY --chown=appuser:appuser app.py ./app.py

USER appuser
EXPOSE 8788

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8788/healthz', timeout=3).read()"]

CMD ["python", "app.py"]
