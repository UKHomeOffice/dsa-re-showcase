from otel_config import meter

# Create a counter for login events
login_event_counter = meter.create_up_down_counter(
    name="login_event_counter",
    description="Counts the number of login events processed",
    unit="1"
)