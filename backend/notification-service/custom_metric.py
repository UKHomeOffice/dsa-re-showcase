from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import Measurement
import os

# Set the CA certificate path via an environment variable
os.environ["REQUESTS_CA_BUNDLE"] = "/app/acp_root_ca.crt"
# Global variable to track the total number of login events
total_login_events = 0

# Initialize OpenTelemetry Metric Exporter
exporter = OTLPMetricExporter(
    endpoint="https://dynatrace-activegate-notprod.dynatrace.svc.cluster.local/e/ewo35763/api/v2/otlp/v1/metrics",
    headers={
        "Authorization": f"Api-Token {os.getenv('DYNATRACE_PAAS_TOKEN')}",
        "Content-Type": "application/x-protobuf"
    },
)

# Set up the MeterProvider with the exporter
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

# Get a meter instance for this module
meter = metrics.get_meter(__name__)

# Create a regular counter for login events (delta metric)
login_event_delta_metric = meter.create_counter(
    name="login_event_delta",
    description="Counts the delta of login events processed",
    unit="1",
)

# Create an observable gauge for total login events
def observe_login_events(callback_options):
    return [Measurement(value=total_login_events, attributes={"event_type": "login"})]

login_event_total_metric = meter.create_observable_gauge(
    name="login_event_total",
    description="Tracks the total number of login events processed",
    unit="1",
    callbacks=[observe_login_events]
)