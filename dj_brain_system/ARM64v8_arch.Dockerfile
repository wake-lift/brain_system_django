FROM arm64v8/python:3.12-bookworm

WORKDIR /app

COPY requirements_backend.txt .

RUN pip install -r requirements_backend.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dj_brain_system.wsgi", "--access-logfile", "-"]
