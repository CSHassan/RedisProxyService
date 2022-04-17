import asyncio
from fastapi import FastAPI
from redis_backend import *
from envyaml import EnvYAML
import uvicorn
import platform

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


env = EnvYAML('./env.yaml')
app = FastAPI()


@app.get('/redis/{redis_id}')
async def get_redisCache(redis_id: str):
    value = await get_redis_value(redis_id)
    if not value:
        return {'No value found in cache'}
    else:
        return {'key': value}


if __name__ == "__main__":   
    uvicorn.run(app, host=env['PROXY.HOST'], port=env['PROXY.PORT'])