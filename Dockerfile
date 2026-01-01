FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy all files first
COPY . /app

# Install in editable mode so it uses the local files directly
RUN pip install --upgrade pip && pip install --no-cache-dir -e .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD \
  python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
