FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY . .

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
