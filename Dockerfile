FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY webhook_inspector webhook_inspector
COPY inspector_app inspector_app
COPY manage.py .
RUN pip install --no-cache-dir -e .
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "-m", "django", "runserver", "0.0.0.0:8000"]
