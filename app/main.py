import time
from fastapi import FastAPI, Request
from app.routers import router

app = FastAPI()


@app.middleware("timing")
async def add_response_timing_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    response.headers["Response-Time"] = str((end_time - start_time) * 1000)
    return response


app.include_router(router.router)


@app.get("/ping")
async def ping():
    return {"message": "pong"}
