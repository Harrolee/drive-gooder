
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
    && apt-get -y install -y openssh-server \
    && apt-get install sudo 
    # need sudo to securely switch to appUser

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR "/app"
RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.in-project true
COPY poetry.lock pyproject.toml ./
# below line to sate coqui tts
# RUN pip wheel --no-cache-dir --use-pep517 "sudachipy (==0.6.8)"

RUN poetry install
