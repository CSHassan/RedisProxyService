import logging
import redis.asyncio as redis
from envyaml import EnvYAML
from local_cache import LRUCache

# read file env.yaml and parse config
env = EnvYAML('./env.yaml')


#intialize the cache
inmem_cache = LRUCache()

#make a redis pool to reuse the connection instead of a new connection
async def _get_redis_client():
    try:
        backing_redis =redis.ConnectionPool(host=env['REDIS.REDIS_HOST'],port=env['REDIS.REDIS_PORT'])
        redis_client = await redis.Redis(connection_pool=backing_redis, decode_responses=True)             
        if (await redis_client.ping()):            
            logging.info("Successfully connected to redis")
            return redis_client                 
    except Exception as e:
        logging.fatal("Redis Error: Something went wrong with connecting to redis: %s" % str(e)) 
        return False
    return False


async def get_redis_value(redis_id: str):
    cache_value = _check_local_cache(redis_id) 
    if(cache_value != -1):
        return cache_value
    else:
        redis_client = await _get_redis_client()
        if not redis_client:
            return False
        redis_value = await redis_client.get(redis_id)       
        _set_local_cache(redis_id,redis_value)
        return redis_value


def _set_local_cache(redis_id: str,redis_value: str):
    inmem_cache.put(redis_id,redis_value)
    logging.info(" Saving to local cache...")
    return


def _check_local_cache(redis_id: str):
    value = inmem_cache.get(redis_id)
    print(value)
    if( value != -1):
         logging.info(" Found in local cache..")
         return value
    else:
        logging.info(" Not found in local cache,feching from redis...")        
        return -1
     


    