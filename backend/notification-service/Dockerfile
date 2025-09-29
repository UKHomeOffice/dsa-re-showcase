FROM quay.io/ukhomeofficedigital/dsa-re-python:3.11.13-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD https://raw.githubusercontent.com/UKHomeOffice/acp-ca/master/ca.pem /app/acp_root_ca.crt

# Change permissions for the CA certificate
RUN chmod 644 /app/acp_root_ca.crt

# Copy the application code
COPY . .

# Change permissions for the /app directory
RUN chmod -R 755 /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
