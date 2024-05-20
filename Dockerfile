FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app/

# Copy requirements in case it doesn't exist in the repo
COPY ./requirements.lock /app/
COPY ./requirements-dev.lock /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r requirements-dev.lock ; else pip install -r requirements.lock ; fi"

ENV PYTHONPATH=/app

COPY ./scripts/ /app/

COPY ./alembic.ini /app/

COPY ./prestart.sh /app/

COPY ./tests-start.sh /app/

COPY ./app /app/app
