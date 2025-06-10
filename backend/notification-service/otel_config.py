import os
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Set the CA certificate path via an environment variable
os.environ["REQUESTS_CA_BUNDLE"] = "/app/acp_root_ca.crt"

# Initialize OpenTelemetry Metric Exporter
metric_exporter = OTLPMetricExporter(
    endpoint="https://dynatrace-activegate-notprod.dynatrace.svc.cluster.local/e/ewo35763/api/v2/otlp/v1/metrics",
    headers={
        "Authorization": f"Api-Token {os.getenv('DYNATRACE_PAAS_TOKEN')}",
        "Content-Type": "application/x-protobuf"
    },
)

# Set up the MeterProvider with the Metric Exporter
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Get a reusable meter instance
meter = metrics.get_meter("notification-service")