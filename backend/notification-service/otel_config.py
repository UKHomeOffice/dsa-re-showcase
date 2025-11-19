import json
import os
import logging
from opentelemetry.sdk.resources import Resource
# Import exporters
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
# Trace imports
from opentelemetry.trace import set_tracer_provider, get_tracer_provider
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# Metric imports
from opentelemetry import metrics as metrics
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.metrics import MeterProvider, Counter, UpDownCounter, Histogram, ObservableCounter, ObservableUpDownCounter
from opentelemetry.metrics import set_meter_provider, get_meter_provider
# Logs import
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider

# ===== GENERAL SETUP =====
# environment
DT_API_URL = os.getenv("OTLP_ENDPOINT")      
DT_API_TOKEN = os.getenv("DYNATRACE_LOGS_TOKEN")
DYNATRACE_PAAS_TOKEN = os.getenv("DYNATRACE_PAAS_TOKEN")
os.environ["REQUESTS_CA_BUNDLE"] = "/app/acp_root_ca.crt"


merged = dict()
for name in ["dt_metadata_e617c525669e072eebe3d0f08212e8f2.json", "/var/lib/dynatrace/enrichment/dt_metadata.json", "/var/lib/dynatrace/enrichment/dt_host_metadata.json"]:
  try:
    data = ''
    with open(name) as f:
      data = json.load(f if name.startswith("/var") else open(f.read()))
      merged.update(data)
  except:
    pass

merged.update({
  "service.name": "notification-service", #TODO Replace with the name of your application
  "service.version": "1.0.1", #TODO Replace with the version of your application
  "service.namespace": "dsa-re-dev" #TODO Replace with the namespace of your application
})
resource = Resource.create(merged)

# ===== METRIC SETUP =====

exporter = OTLPMetricExporter(
  endpoint = DT_API_URL + "/v1/metrics",
  headers = {"Authorization": "Api-Token " + DYNATRACE_PAAS_TOKEN},
  preferred_temporality = {
    Counter: AggregationTemporality.DELTA,
    UpDownCounter: AggregationTemporality.CUMULATIVE,
    Histogram: AggregationTemporality.DELTA,
    ObservableCounter: AggregationTemporality.DELTA,
    ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
  }
)

reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader], resource=resource)
set_meter_provider(provider)
meter = get_meter_provider().get_meter("notification-service", "0.1.2") #TODO Replace with the name of your meter

# ===== LOG SETUP =====

logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)

logger_provider.add_log_record_processor(
  BatchLogRecordProcessor(OTLPLogExporter(
    endpoint = DT_API_URL + "/v1/logs",
    headers = {"Authorization": "Api-Token " + DT_API_TOKEN}
  ))
)
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

# Attach OTLP handler to root logger
logging.getLogger().addHandler(handler)
logging.info("Logging is set up")
