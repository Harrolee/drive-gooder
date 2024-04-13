
FROM python:3.10-slim-bullseye AS base

RUN apt clean \
    && apt -y update

RUN apt-get install -y --no-install-recommends nginx                  \
    && apt-get install -y --no-install-recommends python3-dev         \
    && apt-get install -y --no-install-recommends build-essential     \
    && apt-get install -y --no-install-recommends sudo 
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
    && sed -i '1s;^;source ./.venv/bin/activate\n;' /home/appUser/.bashrc       \
    && chown -R appUser /app

USER appUser
ENV PATH="${PATH}:/home/appUser/.local/bin"
RUN pip install --upgrade pip \
        && pip install poetry \
        && poetry config virtualenvs.in-project true
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-root 
USER root


# create ssl cert to encrypt requests between FE and BE
# too careful? maybe.
RUN mkdir /etc/nginx/certs \
    && cd /etc/nginx/certs \ 
    && openssl req -x509 -newkey \
    rsa:4096 -keyout key.pem -out cert.pem \
    -sha256 -days 365 -nodes -subj "/C=US/ST=IN/L=Indianapolis/O=BTYT/OU=clowns/CN=drive-gooder"

COPY ./cloud/nginx.conf /etc/nginx/nginx.conf

COPY --chown=1007:1010 backend backend
COPY --chown=1007:1010 /build frontend
COPY --chown=1007:1010 cloud/uwsgi.ini cloud/start.sh cloud/appUserStart.sh ./
RUN chmod +x start.sh appUserStart.sh

# add a dev ssh key
# RUN mkdir /home/appUser/.ssh
# RUN chmod 700 /home/appUser/.ssh
# COPY id_rsa.pub /appUser/.ssh/authorized_keys
# RUN chmod 600 /home/appUser/.ssh

# EXPOSE 80
# EXPOSE 443
EXPOSE 3000
CMD ["./start.sh"]