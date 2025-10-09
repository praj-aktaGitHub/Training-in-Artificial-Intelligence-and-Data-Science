from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import time
import traceback

app = FastAPI()

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

visit_count = 0

@app.middleware("http")
async def count_requests(request: Request, call_next):
    global visit_count
    visit_count += 1
    logging.info(f"Website visited: {visit_count} times")
    response = await call_next(request)
    return response

@app.get("/")
async def home():
    return JSONResponse(
        content={
            "total_visits": visit_count,
        }
    )

