FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml /app/pyproject.toml
COPY app /app/app

RUN pip install --upgrade pip && pip install --no-cache-dir .

COPY . /app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD \
  python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
