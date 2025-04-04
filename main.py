import uvicorn
from fastapi import FastAPI
from app.api.v1.notification import router as notifications_router
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(notifications_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,log_level="info")