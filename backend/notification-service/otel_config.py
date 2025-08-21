import os
import logging
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry._logs import set_logger_provider, get_logger
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

provider = LoggerProvider()
processor = BatchLogRecordProcessor(ConsoleLogExporter())
provider.add_log_record_processor(processor)
# Sets the global default logger provider
set_logger_provider(provider)

logger = get_logger(__name__)

handler = LoggingHandler(level=logging.INFO, logger_provider=provider)
logging.basicConfig(handlers=[handler], level=logging.INFO)

logging.info("This is an OpenTelemetry log record!")


# Set the CA certificate path via an environment variable
os.environ["REQUESTS_CA_BUNDLE"] = "/app/acp_root_ca.crt"

OTLP_ENDPOINT = os.getenv(
    "OTLP_ENDPOINT",
    "https://dynatrace-activegate-notprod-testing.dynatrace.svc.cluster.local/e/ewo35763/api/v2/otlp/v1"
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

# 2. Set up OpenTelemetry LoggerProvider
logger_provider = LoggerProvider(
    resource=Resource.create({"service.name": "notification-service"})
)
set_logger_provider(logger_provider)

# 3. Add a log processor with OTLP exporter
log_exporter = OTLPLogExporter(
    endpoint=f"{OTLP_ENDPOINT}/logs",
    headers={"Authorization": f"Api-Token {DYNATRACE_LOGS_TOKEN}"},
    insecure=True  
)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

# 4. Hook into Python's logging module
logging_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging_handler],
)

# 5. Create a reusable logger instance
otel_logger = get_logger("notification-service")