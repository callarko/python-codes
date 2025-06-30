from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/process/")
async def process(request: Request):
    data = await request.json()
    return {"received": data}
