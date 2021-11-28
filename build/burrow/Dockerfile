# stage 1: builder
FROM golang:1.17.2-alpine as builder

RUN apk add --no-cache git curl
COPY ./build/burrow /usr/src/Burrow/
WORKDIR /usr/src/Burrow/

RUN go mod tidy && go build -o /tmp/burrow .

# stage 2: runner
FROM alpine:3.14

LABEL maintainer="LinkedIn Burrow https://github.com/linkedin/Burrow"

COPY --from=builder ./tmp/burrow /app/
COPY ./build/burrow/docker-config/burrow.toml /etc/burrow/

CMD ["/app/burrow", "--config-dir", "/etc/burrow"]
