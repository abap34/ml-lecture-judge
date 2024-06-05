# fast api and uvicorn

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{name}")
def read_item(name: str):
    return {"Hello": name}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)