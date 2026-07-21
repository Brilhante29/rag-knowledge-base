FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir . \
    && addgroup --system app \
    && adduser --system --ingroup app app

COPY --chown=app:app data ./data
COPY --chown=app:app benchmarks ./benchmarks

USER app

EXPOSE 8000
ENTRYPOINT ["python", "-m", "rag_knowledge_base"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8000"]
