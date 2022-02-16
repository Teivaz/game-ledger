FROM python:3.8 as base
WORKDIR /usr/app
ENV PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=on


FROM base as requirements
ENV POETRY_VERSION="1.1.12" \
	POETRY_NO_INTERACTION="1" \
	POETRY_HOME="/opt/poetry"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="$PATH:$POETRY_HOME/bin"
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt


FROM base as app
ENV APP_NUM_WORKERS="4" \
	APP_HOST="0.0.0.0" \
	APP_PORT="8000"
COPY game_ledger ./game_ledger
COPY app.py ./
COPY --from=requirements /usr/app/requirements.txt ./
RUN pip install --no-deps -r requirements.txt

CMD gunicorn -w ${APP_NUM_WORKERS} app:app -b ${APP_HOST}:${APP_PORT}
