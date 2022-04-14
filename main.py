from fastapi import FastAPI

from pydantic import BaseModel

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from redis_backend import *

app = FastAPI()

db= []

class City(BaseModel):
    name: str
    timezone: str

@app.get('/redis')
def get_redisCache(redis_id: str):
    print(redis_id)
    value = get_redis_value(redis_id)
    return {'key': value}

# @app.get('/redis/{redis_id}')
# def get_redisCache(redis_id: str):
#     value = get_redis_value()
#     return {'key': value}

# @app.get('/redis/{redis_id}')
# async def get_rediscacheasync(redis_id: str):
#     return db[redis_id-1]

if __name__ == "__main__":
    asyncio.run("hypercorn.main:app", host=env['PROXY.HOST'], port=env['PROXY.PORT'], reload=True, workers=2)