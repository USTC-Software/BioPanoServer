FROM smartentry/alpine:3.4-beta

ADD . /opt/biopano

ENV ASSETS_DIR=/opt/biopano/docker

RUN smartentry.sh build
