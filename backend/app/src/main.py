from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import submissions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(submissions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Judge System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
