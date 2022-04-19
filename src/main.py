import asyncio
import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import platform
from src.redis_backend import get_redis_value

load_dotenv()

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
logging.basicConfig(level=logging.INFO)

app = FastAPI()



@app.get('/redis/{redis_id}')
async def get_redisCache(redis_id: str):
    message = "value"  
    if redis_id.isspace():
          return{'invalid format'}      
    value = await get_redis_value(redis_id)    
    if not value:
          message = 'No value found in redis or local cache'
          value = ''
    return{message : value}


if __name__ == "__main__":      
    uvicorn.run(app, host=os.getenv('PROXY_HOST'), port=(int(os.getenv('PROXY_PORT'))))