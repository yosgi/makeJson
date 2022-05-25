FROM h.eefocus.tech/devops/dev-env/alpine3.10-node10-nginx:latest

COPY docker/adssys.eefocus.tech.conf /etc/nginx/conf.d/
COPY dist /opt/vhosts/adssys.eefocus.tech/

WORKDIR /opt/vhosts/adssys.eefocus.tech/

EXPOSE 8080