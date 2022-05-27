FROM h.eefocus.tech/devops/dev-env/alpine3.10-node10-nginx:latest

COPY docker/m2j.eefocus.tech.conf /etc/nginx/conf.d/
COPY build /opt/vhosts/m2j.eefocus.tech/

WORKDIR /opt/vhosts/m2j.eefocus.tech/

EXPOSE 8080