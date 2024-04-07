
FROM python:3.10-slim-bullseye AS base

RUN apt clean \
    && apt -y update

RUN apt install -y --no-install-recommends nginx                  \
    && apt install -y --no-install-recommends python3-dev         \
    && apt install -y --no-install-recommends build-essential     \
    && apt install -y --no-install-recommends sudo 
    # need sudo to securely switch to appUser

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR "/app"

RUN groupadd --gid 1010 socketWriters                                           \
    && usermod -a -G socketWriters www-data                                     \
    && pwd=$(cat /proc/sys/kernel/random/uuid)                                  \
    && echo "$pwd" > password                                                   \
# create appUser
# gid 1010 is socketWriters
# uid 1007 will own the /app dir
# Coqui saves models to the user's home dir, so we need to create a user with a home dir
    && useradd -u 1007 -g 1010 -m -p "$(cat password)" appUser                  \ 
    && shred -u password                                                        \
# set HOME on non-login user changes for appUser:
    && sed -i '1s;^;export HOME="/home/appUser"\n;' /home/appUser/.bashrc       \
    && sed -i '1s;^;echo "running bashrc for appUser"\n;' /home/appUser/.bashrc \
    && sed -i '1s;^;source ./.venv/bin/activate\n;' /home/appUser/.bashrc     &&\
# Create the .local and share directories if useradd does not make them 
    if [ ! -d "/home/appUser/.local" ]; then                                    \
        mkdir -p "/home/appUser/.local/share/tts"                               \
# coqui seems to use both tts and tts-caches
        && mkdir -p "/home/appUser/.local/share/tts-cache"                      \
        && chown -R appUser "/home/appUser/";                                   \
    fi                                                                          \
    && chown -R appUser /app

USER appUser
ENV PATH="${PATH}:/home/appUser/.local/bin"
RUN pip install --upgrade pip \
        && pip install poetry \
        && poetry config virtualenvs.in-project true
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-root 
USER root