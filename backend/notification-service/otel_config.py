import os
import json
import logging

from opentelemetry.sdk.resources import Resource

# Exporters
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

# Traces
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider

# Metrics
from opentelemetry.sdk.metrics import MeterProvider, Counter, UpDownCounter, Histogram, ObservableCounter, ObservableUpDownCounter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, AggregationTemporality
from opentelemetry.metrics import set_meter_provider, get_meter

# Logs
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider


# -------------------------------------------------------------------------
# GLOBAL INITIALIZATION BLOCK (Executed immediately on import by db.py)
# This ensures 'meter' is a valid object when other modules import it.
# -------------------------------------------------------------------------

# Environment variables
DT_API_URL = os.getenv("OTLP_ENDPOINT")      
DT_API_TOKEN = os.getenv("DYNATRACE_LOGS_TOKEN")
DYNATRACE_PAAS_TOKEN = os.getenv("DYNATRACE_PAAS_TOKEN")
os.environ["REQUESTS_CA_BUNDLE"] = "/app/acp_root_ca.crt"

# Resource metadata
merged = {}
for name in [
    "/var/lib/dynatrace/enrichment/dt_metadata.json",
    "/var/lib/dynatrace/enrichment/dt_host_metadata.json",
]:
    try:
        with open(name) as f:
            merged.update(json.load(f))
    except:
        pass
merged.update({
    "service.name": "notification-service",
    "service.version": "1.0.0",
    "service.namespace": "dsa-re-dev"
})
resource = Resource.create(merged)

# Metrics Provider Setup
metric_exporter = OTLPMetricExporter(
    endpoint=f"{DT_API_URL}/v1/metrics",
    headers={"Authorization": f"Api-Token {DYNATRACE_PAAS_TOKEN}"},
    preferred_temporality={
        Counter: AggregationTemporality.DELTA,
        UpDownCounter: AggregationTemporality.CUMULATIVE,
        Histogram: AggregationTemporality.DELTA,
        ObservableCounter: AggregationTemporality.DELTA,
        ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
    }
)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
set_meter_provider(meter_provider)

# Global Meter object is assigned here and is ready for import!
meter = get_meter("notification-service-app", "1.0.0")

# Logging Provider Setup
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(
        OTLPLogExporter(
            endpoint=f"{DT_API_URL}/v1/logs",
            headers={"Authorization": f"Api-Token {DT_API_TOKEN}"},
            insecure=False
        )
    )
)

# -------------------------------------------------------------------------
# init_telemetry function (now only handles final logging setup)
# -------------------------------------------------------------------------
def init_telemetry():
    """Initializes standard Python logging handler after OTel providers are set."""
    otel_handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=logger_provider
    )
    logging.basicConfig(
        level=logging.INFO,
        handlers=[otel_handler],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("init").info("OpenTelemetry for Dynatrace initialized.")
