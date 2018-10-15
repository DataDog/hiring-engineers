FROM alpine:latest
LABEL maintainer "Yuya Ushijima <github:ushijimay>"

### Environment variables
ENV LANG='en_US.UTF-8' \
    LANGUAGE='en_US.UTF-8' \
    TERM='xterm' \
    DOCKPGDB=$DOCKPGDB \
    DOCKPGHOST=$DOCKPGHOST \
    DOCKPGUSER=$DOCKPGUSER \
    DOCKPGPASSWD=$DOCKPGPASSWD \
    DD_AGENT_PORT_8126_TCP_ADDR=${DD_AGENT_PORT_8126_TCP_ADDR} \
    DD_AGENT_PORT_8126_TCP_PORT=${DD_AGENT_PORT_8126_TCP_PORT} \
    DD_HOST=${DD_HOST}

### Install Application
RUN apk --no-cache upgrade && \
    apk add --no-cache --virtual=build-deps \
      gcc \
      jpeg-dev \
      python3-dev \
      musl-dev \
      postgresql-dev \
      zlib-dev && \
    apk add --no-cache --virtual=run-deps \
      python3 \ 
      jpeg \
      ssmtp \
      postgresql-libs \
      su-exec && \
    pip3 --no-cache-dir install --upgrade setuptools pip && \
    pip3 --no-cache-dir install mezzanine==4.3.1 psycopg2-binary==2.7.5 gunicorn==19.9.0 ddtrace setproctitle && \
    apk del --no-cache --purge \
      build-deps  && \
    rm -rf /tmp/* \
           /var/cache/apk/*  \
           /var/tmp/*

### Add Original Django Project
RUN mkdir /project
COPY app /project

### Expose ports
EXPOSE 8000

### Running User: not used, managed by docker-entrypoint.sh
#USER mezzanine

### Start Mezzanine
COPY app/docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["mezzanine"]
