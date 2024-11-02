from fastapi import FastAPI, Depends
import uvicorn
from redis.asyncio import Redis

from app.database import get_redis
from app.routes import router

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
