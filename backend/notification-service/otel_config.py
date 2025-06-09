import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace.export import BatchSpanProcessor

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

# Initialize OpenTelemetry Trace Exporter
trace_exporter = OTLPSpanExporter(
    endpoint="https://dynatrace-activegate-notprod.dynatrace.svc.cluster.local/e/ewo35763/api/v2/otlp/v1/traces",
    headers={
        "Authorization": f"Api-Token {os.getenv('DYNATRACE_PAAS_TOKEN')}",
        "Content-Type": "application/x-protobuf"
    },
)

# Set up the MeterProvider with the Metric Exporter
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Set up the TracerProvider with the Trace Exporter
tracer_provider = TracerProvider()
span_processor = BatchSpanProcessor(trace_exporter)
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# Get reusable tracer and meter instances
tracer = trace.get_tracer("notification-service")
meter = metrics.get_meter("notification-service")