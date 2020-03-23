FROM golang:1.14 AS builder

ENV SRV_NAME custom_dashboard
ENV CGO_ENABLED=0
ENV GO111MODULE=on
ENV GOOS=linux

# Copy the code from the host and compile it
WORKDIR /${SRV_NAME}
COPY . .
RUN make vendor && make
COPY config.yml ./bin/
ENTRYPOINT ["./bin/app"]