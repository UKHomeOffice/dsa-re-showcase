ARG ALPINE_TAG=latest
FROM alpine:${ALPINE_TAG}

RUN apk -U upgrade \
    && apk add --no-cache \
        bash \
        curl \
        jq \
        wget \
        busybox-extras \
    && rm -rf /var/cache/apk/*

RUN adduser -D -u 1000 reliabilityenablement

USER 1000

CMD ["/bin/bash", "--login"]
