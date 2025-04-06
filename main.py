import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.middleware.log import log_incoming_request
from app.api.middleware.request_id import apply_request_id
from app.api.v1.notification import router as notifications_router
from app.core.rabbitmq import RabbitMQ


@asynccontextmanager
async def lifespan(app:FastAPI):
    ### Init MQ
    mq = RabbitMQ()
    app.state.mq = mq
    yield
    mq.close()
app = FastAPI(lifespan=lifespan)

app.middleware("http")(apply_request_id)
app.middleware("http")(log_incoming_request)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}





app.include_router(notifications_router)

if __name__ == "__main__":
    logging.info("Starting app")
    uvicorn.run(app, host="0.0.0.0", port=8000,log_level="info")