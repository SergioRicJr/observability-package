from fastapi import FastAPI, Response
from  middleware.ObservabilityMiddleware import ObservabilityMiddleware
import random
import requests
import uvicorn

app = FastAPI()

app.add_middleware(ObservabilityMiddleware)

@app.get("/")
def welcome():
    return {"message": "Hello, welcome to the application!"}

@app.get("/random")
def get_random_number():
    random_number = random.randint(0, 1000)
    return {"message": f"The random number is {random_number}"}

def calc_factorial(number):
    factorial = 1
    for i in range(1, number + 1):
        factorial *= i
    return factorial

@app.get("/factorial")
def get_factorial():
    random_number = random.randint(10, 100)
    factorial = calc_factorial(random_number)
    return {"message": f"The factorial of number {random_number} is {factorial}"}
    
@app.get("/requests")
def multiple_requests():
    requests.get("http://localhost:8000/")
    requests.get("http://localhost:8000/random")
    requests.get("http://localhost:8000/factorial")

    return {"message": "Multiple requests are sent"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )