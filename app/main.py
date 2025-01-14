from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return {"hello": "world!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
