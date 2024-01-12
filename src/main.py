from bootstrap import start_app
from fastapi import FastAPI

app = start_app()

# app = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "world"}
