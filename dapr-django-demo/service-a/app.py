from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/call-b/")
async def call_b(request: Request):
    data = await request.json()
    response = requests.post(
        "http://localhost:3500/v1.0/invoke/service-b/method/process",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    return {"response_from_b": response.json()}
