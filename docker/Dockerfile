from python:3.9

WORKDIR /app

COPY ../pyproject.toml /app/
COPY ../pydnsapi /app/pydnsapi

# make the default logging dir

RUN  mkdir /app/logs

RUN pip install poetry && poetry config virtualenvs.create false

RUN poetry install --no-dev

EXPOSE 8000
CMD ["uvicorn","pydnsapi:app","--host=0.0.0.0","--port=8000"]

