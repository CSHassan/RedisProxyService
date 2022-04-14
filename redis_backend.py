import redis
from envyaml import EnvYAML

# read file env.yaml and parse config
env = EnvYAML('/../env.yaml')

redis_client = redis.Redis(host=env['REDIS.REDIS_HOST'],port=env['REDIS.REDIS_PORT'])

def get_redis_value(redis_id: str):
    username = redis_client.get(redis_id)
    return username

 


  
