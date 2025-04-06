import logging

from fastapi import Request


async def log_incoming_request(request:Request, call_next):
    ### Retrieve request id
    response = await call_next(request)

    request_id = getattr(request.state, "request_id", "N/A")
    logging.info(f"[Incoming Request] - [RequestID : {request_id}] - [Path : {request.url.path}] - [IP : {request.client.host}]")

    return response
