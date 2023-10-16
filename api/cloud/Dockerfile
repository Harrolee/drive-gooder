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
    && apt-get -y install espeak \
    && apt-get install sudo
    # need sudo to securely switch to appUser

FROM base AS builder

# Renewing WORKDIR
ARG WORKDIR
WORKDIR ${WORKDIR}

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY .venv ./

FROM builder as final

# Renewing WORKDIR
ARG WORKDIR
WORKDIR ${WORKDIR}

COPY backend ./backend
COPY cloud/start.sh cloud/uwsgi.ini ./
RUN chmod +x start.sh
COPY ./cloud/nginx.conf /etc/nginx

# configure appUser
COPY cloud/password cloud/appUser.sh cloud/appUserStart.sh ./ 
RUN chmod +x appUser.sh appUserStart.sh
RUN ./appUser.sh

EXPOSE 5003
CMD ["./start.sh"]