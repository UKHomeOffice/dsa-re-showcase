import os
import logging
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.logs import LogEmitterProvider, LoggingHandler
from opentelemetry.sdk.logs.export import BatchLogProcessor
from opentelemetry.exporter.otlp.proto.http.log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.logs import LoggingHandler


# Set the CA certificate path via an environment variable
os.environ["REQUESTS_CA_BUNDLE"] = "/app/acp_root_ca.crt"

OTLP_ENDPOINT = os.getenv(
    "OTLP_ENDPOINT",
    "https://activegate-notprod.dynatrace-corecloud-notprod.dsa-notprod.homeoffice.gov.uk/e/ewo35763/api/v2/otlp/v1"
)

DYNATRACE_PAAS_TOKEN = os.getenv("DYNATRACE_PAAS_TOKEN")
DYNATRACE_LOGS_TOKEN = os.getenv("DYNATRACE_LOGS_TOKEN")

# Initialize OpenTelemetry Metric Exporter
metric_exporter = OTLPMetricExporter(
    endpoint=f"{OTLP_ENDPOINT}/metrics",
    headers={
        "Authorization": f"Api-Token {DYNATRACE_PAAS_TOKEN}",
        "Content-Type": "application/x-protobuf"
    },
)

# Set up the MeterProvider with the Metric Exporter
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Get a reusable meter instance
meter = metrics.get_meter("notification-service")

# Initialize OpenTelemetry Log Exporter
log_exporter = OTLPLogExporter(
    endpoint=f"{OTLP_ENDPOINT}/logs",
    headers={
        "Authorization": f"Api-Token {DYNATRACE_LOGS_TOKEN}",
        "Content-Type": "application/x-protobuf"
    },
)

# Set up the LogEmitterProvider with the Log Exporter
log_emitter_provider = LogEmitterProvider(
    resource=Resource.create({"service.name": "notification-service"})
)
# Attach OpenTelemetry LoggingHandler to Python's logging module
logging.basicConfig(
    level=logging.INFO,  # Set the log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        LoggingHandler(level=logging.INFO, log_emitter_provider=log_emitter_provider),
    ],
)

# Create a reusable logger instance
otel_logger = logging.getLogger("notification-service")