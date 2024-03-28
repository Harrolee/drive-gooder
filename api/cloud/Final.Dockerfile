ARG WORKDIR="/app"

FROM halzinnia/drive-gooder-base:v0.0.2

ARG WORKDIR
WORKDIR ${WORKDIR}

COPY backend backend
COPY cloud/start.sh cloud/uwsgi.ini ./
RUN chmod +x start.sh
COPY ./cloud/nginx.conf /etc/nginx

# copy built static FE to docker image
COPY /build frontend

# copy the cert in 
COPY /sslCert /etc/nginx/certs

# configure appUser
COPY cloud/password cloud/appUser.sh cloud/appUserStart.sh ./ 
RUN chmod +x appUser.sh appUserStart.sh
RUN ./appUser.sh

# add a dev ssh key
# RUN mkdir /home/appUser/.ssh
# RUN chmod 700 /home/appUser/.ssh
# COPY id_rsa.pub /appUser/.ssh/authorized_keys
# RUN chmod 600 /home/appUser/.ssh

EXPOSE 80
EXPOSE 443
EXPOSE 22
CMD ["./start.sh"]