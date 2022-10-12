FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
ENV PYTHONUNBUFFERED 1

WORKDIR /app

FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

COPY pyproject.toml /app/
COPY pydnsapi /app/pydnsapi

# make the default logging dir
RUN  mkdir /app/logs

RUN poetry install --no-interaction --no-ansi -vvv

FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app

EXPOSE 8000

CMD ["uvicorn","pydnsapi:main:app","--host=0.0.0.0","--port=8000"]
