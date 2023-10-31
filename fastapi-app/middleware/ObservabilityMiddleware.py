from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
import time

class ObservabilityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str = "fastapi-app") -> None:
        super().__init__(app)
        self.app_name = app_name

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method
        path = request.url.path

        # if not is_handled_path:
        #     return await call_next(request)

        before_time = time.perf_counter()
        try:
            response = await call_next(request)
        except BaseException as error:
            pass
        else:
            status_code = response.status_code
            after_time = time.perf_counter()

        finally:
            pass
        return response