# from https://github.com/python-poetry/poetry/issues/1178#issuecomment-1238475183

# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"

FROM python:3.10-slim-bullseye AS base

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get install -y curl \
    && apt-get -y install build-essential \
    && apt-get -y install libpq-dev \
    && apt-get -y install ffmpeg \
    && apt-get -y install espeak

FROM base AS builder

# Renew (https://stackoverflow.com/a/53682110):
ARG WORKDIR

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ${WORKDIR}

RUN pip install poetry && poetry config virtualenvs.in-project true > pipInstallPoetryOut 2>&1

RUN echo $(pwd)  

COPY poetry.lock pyproject.toml ./

RUN poetry install >poetryInstallOut 2>&1

COPY cloud/start.sh cloud/uwsgi.ini .venv ./
COPY backend ./backend

FROM builder as final

# Renew (https://stackoverflow.com/a/53682110):
ARG WORKDIR

WORKDIR ${WORKDIR}

COPY ./cloud/nginx.conf /etc/nginx
RUN chmod +x start.sh

# RUN adduser app -u 1000
# RUN usermod -aG sudo app
# RUN chmod -R app /

# App-specific settings:

EXPOSE 5003
CMD ["./start.sh"]