
FROM python:3.11-slim
WORKDIR /backend

COPY ./backend/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /backend/requirements.txt

COPY ./backend/app /backend/app

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
