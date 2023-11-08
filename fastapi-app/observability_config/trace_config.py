from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from dotenv import load_dotenv
import os

load_dotenv()

resource = Resource.create({SERVICE_NAME: "fastapi-app"})
trace.set_tracer_provider(TracerProvider(resource=resource))

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=os.environ.get('TEMPO_URL')))
)

tracer = trace.get_tracer(__name__)