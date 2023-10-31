from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
import time
from observability_config.metric_config import requests_in_progress, status_http_counter, http_request_duration, send_metrics

class ObservabilityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str = "fastapi-app") -> None:
        super().__init__(app)
        self.app_name = app_name

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        before_time = time.perf_counter()
        requests_in_progress.inc()
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
        except BaseException as error:
            # adicionar logs
            pass

        finally:
            status_code = response.status_code
            status_http_counter.labels(http_code=status_code)
            requests_in_progress.dec()
            after_time = time.perf_counter()
            http_request_duration.labels(url_path=path, http_method=method).observe(
                after_time - before_time
            )
            send_metrics()
        return response