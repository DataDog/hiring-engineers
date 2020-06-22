FROM alpine:3

RUN apk add --no-cache ca-certificates

WORKDIR /app

COPY ./twitter_collector_linux .
COPY ./entrypoint.sh .

RUN set -eux \
    && chmod +x ./entrypoint.sh ./twitter_collector_linux

EXPOSE 8080

ENTRYPOINT [ "./entrypoint.sh" ]
