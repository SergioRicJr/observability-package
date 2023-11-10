from prometheus_client import Counter, CollectorRegistry, Summary, Gauge, pushadd_to_gateway
from dotenv import load_dotenv
import os
load_dotenv()

registry = CollectorRegistry()

status_http_counter = Counter(
    'http_requests_total_by_code',
    'responses total by status code',
    ['http_code', 'unmapped'],
    registry=registry
)

http_request_duration = Summary(
    'http_requests_duration_seconds',
    'reponse time of request',
    ['url_path', 'http_method', 'unmapped'],
    registry=registry
)

requests_in_progress = Gauge(
    'request_in_progress_total',
    'quantity of requests in progress',
    registry=registry
)

def send_metrics():
    pushadd_to_gateway(os.environ.get('PROMETHEUS_URL'), job='fastapi-app', registry=registry)