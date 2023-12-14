from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
import time
from observability_mtl_instrument.metrics.metric_config import MetricConfig
from dotenv import load_dotenv
import os

load_dotenv()


metric_config = MetricConfig(
    job_name="fastapi-app", prometheus_url=os.getenv("PROMETHEUS_URL")
)

metrics = metric_config.metrics


class ObservabilityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str = "fastapi-app") -> None:
        super().__init__(app)
        self.app_name = app_name

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        before_time = time.perf_counter()
        metrics["requests_in_progress"].labels(service_name="fastapi-app").inc(1)
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
        except BaseException as error:
            pass

        finally:
            status_code = response.status_code
            metrics["http_requests_total_by_code"].labels(
                service_name="fastapi-app",
                http_code=status_code,
                unmapped=True if status_code == 404 else False,
            ).inc(1)
            metrics["requests_in_progress"].labels(service_name="fastapi-app").dec()
            after_time = time.perf_counter()
            metrics["http_requests_duration_seconds"].labels(
                service_name="fastapi-app",
                url_path=path,
                http_method=method,
                unmapped=True if status_code == 404 else False,
            ).observe(after_time - before_time)
            metric_config.send_metrics()
        return response
