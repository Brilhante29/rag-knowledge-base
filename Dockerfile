FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data
COPY benchmarks ./benchmarks

RUN pip install --no-cache-dir .

EXPOSE 8000
ENTRYPOINT ["python", "-m", "rag_knowledge_base"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8000"]
