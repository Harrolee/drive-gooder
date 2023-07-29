FROM python:3.11-slim-bullseye

# install curl for health check purposes
RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get install -y curl \
    && apt-get -y install build-essential \
    && apt-get -y install libpq-dev

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
COPY ./cloud/nginx.conf /etc/nginx
RUN chmod +x ./cloud/start.sh

EXPOSE 5003

CMD ["./cloud/start.sh"]