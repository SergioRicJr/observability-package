import random
import uvicorn
import httpx
from fastapi import FastAPI
from middleware.ObservabilityMiddleware import ObservabilityMiddleware
from observability_mtl_instrument.tracer.trace_config import TraceConfig
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.propagate import inject
from observability_mtl_instrument.logs.builders.fullLogConfigAsync import (
    FullLogConfigAsync,
)
from dotenv import load_dotenv
import os

load_dotenv()

trace_config = TraceConfig(
    service_name="fastapi-module", tempo_url=os.getenv("TEMPO_URL")
)
trace = trace_config.get_trace()

log_config = FullLogConfigAsync(
    service_name="fastapi-app", loki_url=os.getenv("LOKI_URL")
).get_log_config()

logger = log_config.logger

app = FastAPI()

app.add_middleware(ObservabilityMiddleware)


@app.get("/")
async def welcome():
    logger.info(
        "hello message was sent",
        extra={"extra_labels": {"foo": "bar"}},
    )
    return {"message": "Hello, welcome to the application!"}


@app.get("/random")
async def get_random_number():
    random_number = random.randint(0, 100)
    logger.info("random number between 0 and 100 was calculated")
    return {"message": f"The random number was created", "number": random_number}


def calc_factorial(number):
    factorial = 1
    for i in range(1, number + 1):
        factorial *= i
    return factorial


@app.get("/factorial")
async def get_factorial():
    headers = {}
    inject(headers)  
    logger.critical(headers)

    async with httpx.AsyncClient() as client:
        random_number = await client.get(
            "http://localhost:8000/random", headers=headers
        )
    random_number = random_number.json()
    random_number = random_number["number"]
    factorial = calc_factorial(random_number)
    logger.info("factorial was calculated successfully")
    return {"message": f"The factorial of number {random_number} is {factorial}"}


@app.get("/requests")
async def multiple_requests():
    headers = {}
    inject(headers)  
    logger.critical(headers)
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/", headers=headers)
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/random", headers=headers)
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/factorial", headers=headers)
    logger.info("multiple requests were made successfully")
    return {"message": "Multiple requests are sent"}


FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
