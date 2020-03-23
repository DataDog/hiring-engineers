FROM golang:1.14 AS builder

ENV SRV_NAME server
ENV CGO_ENABLED=0
ENV GO111MODULE=on
ENV GOOS=linux

# Copy the code from the host and compile it
WORKDIR /${SRV_NAME}
COPY go.mod .
COPY go.sum .
COPY Makefile .
RUN go mod tidy
RUN go mod download
COPY . .

RUN make vendor
RUN make
RUN cp ./bin/app /app

FROM scratch
COPY --from=builder /app /go/bin/app
ENTRYPOINT ["/go/bin/app"]
