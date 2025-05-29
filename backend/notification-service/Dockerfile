FROM quay.io/ukhomeofficedigital/dsa-re-python:3.11.12-alpine3.21

WORKDIR /app

ARG USER=dynatrace
ARG UID=1000

USER root

COPY dsa-re-showcase/backend/notification-service .

ADD https://raw.githubusercontent.com/UKHomeOffice/acp-ca/master/ca.pem /app/acp_root_ca.crt

RUN chown -R "$USER":"$USER" /app
RUN chmod 755 /app

USER $UID

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]