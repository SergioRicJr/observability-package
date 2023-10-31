import random
import uvicorn
import httpx
from fastapi import FastAPI
from  middleware.ObservabilityMiddleware import ObservabilityMiddleware
from observability_config.log_config import logger

app = FastAPI()

app.add_middleware(ObservabilityMiddleware)

@app.get("/")
def welcome():
    logger.info('hello message was sent')
    return {"message": "Hello, welcome to the application!"}

@app.get("/random")
def get_random_number():
    random_number = random.randint(0, 100)
    logger.info('random number between 0 and 100 was calculated')
    return {"message": f"The random number was created", "number": random_number}

def calc_factorial(number):
    factorial = 1
    for i in range(1, number + 1):
        factorial *= i
    return factorial

@app.get("/factorial")
async def get_factorial():
    async with httpx.AsyncClient() as client:
        random_number = await client.get('http://localhost:8000/random')
        random_number = random_number.json()
        random_number = random_number['number']
        factorial = calc_factorial(random_number)
        logger.info('factorial was calculated successfully')
        return {"message": f"The factorial of number {random_number} is {factorial}"}
    
@app.get("/requests")
async def multiple_requests():
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/")
        await client.get("http://localhost:8000/random")
        await client.get("http://localhost:8000/factorial")
        logger.info('multiple requests were made successfully')
        return {"message": "Multiple requests are sent"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )