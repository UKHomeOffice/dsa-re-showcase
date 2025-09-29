ARG ALPINE_TAG=3.22.1
FROM alpine:${ALPINE_TAG}

RUN apk -U upgrade \
    && apk add --no-cache \
        bash \
        curl \
        jq \
        wget \
        busybox-extras \
        openjdk11 \
        openssl \
        aws-cli \
        postgresql-client \
    && rm -rf /var/cache/apk/*

# Download and install kafka
ARG KAFKA_VERSION=3.9.0
ARG SCALA_VERSION=2.13
RUN curl -L "https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" | tar -xz -C /opt/ \
&& mv /opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION} /opt/kafka

RUN adduser -D -u 1000 reliabilityenablement

USER 1000

RUN echo 'export PATH="/opt/kafka/bin:$PATH"' >> /home/reliabilityenablement/.profile

CMD ["/bin/bash", "--login"]
