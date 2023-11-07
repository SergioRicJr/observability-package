# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# from main import app
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# resource = Resource.create({SERVICE_NAME: "fastapi-app"})
# trace.set_tracer_provider(TracerProvider(resource=resource))

# trace.get_tracer_provider().add_span_processor(
#     BatchSpanProcessor(OTLPSpanExporter(endpoint="http://nginx:80/tempo/v1/traces"))
# )

# tracer = trace.get_tracer(__name__)

# FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())