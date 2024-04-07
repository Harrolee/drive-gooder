ARG WORKDIR="/app"

FROM halzinnia/drive-gooder-base:v0.0.6arm

ARG WORKDIR
WORKDIR ${WORKDIR}

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

EXPOSE 80
EXPOSE 443
EXPOSE 22
CMD ["./start.sh"]