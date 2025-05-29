from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import os

# Initialize OpenTelemetry Metric Exporter
exporter = OTLPMetricExporter(
    endpoint=os.getenv("DYNATRACE_API_URL"),
    headers={"Authorization": f"Api-Token {os.getenv('DYNATRACE_PAAS_TOKEN')}"}
)

# Set up the MeterProvider with the exporter
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

# Get a meter instance for this module
meter = metrics.get_meter(__name__)

# Create a custom counter metric for login events
login_event_metric = meter.create_counter(
    name="login_event_counter",
    description="Counts the number of login events processed",
    unit="1",
)