from fastapi import FastAPI
from pydantic import BaseModel
from redis_backend import *
from envyaml import EnvYAML
import uvicorn

env = EnvYAML('./env.yaml')
app = FastAPI()

@app.get('/redis')
async def get_redisCache(redis_id: str):
    print(redis_id)
    value = await get_redis_value(redis_id)
    return {'key': value}

 


if __name__ == "__main__":   
    uvicorn.run(app, host=env['PROXY.HOST'], port=env['PROXY.PORT'])