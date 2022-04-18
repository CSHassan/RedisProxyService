from collections import OrderedDict
import time
from threading import Lock
from envyaml import EnvYAML

env = EnvYAML('./env.yaml')

# we have two dict, cache and global expiry
# cache takes in the key/value pair from redis
#global expiry takes the key and current time
#lock for concurrency
class LRUCache:
 
    # initialising
    def __init__(self):
        self.cache = OrderedDict()
        self.capacity = env['CACHE.SIZE']
        self.global_expiry = {}
        self.lock = Lock()
 
    # first we lock and check if the key is expired
    # we return the value of the key
    # that is queried in O(1) and return -1 if we
    # don't find the key in out dict / cache.
    # and also move the key to the end
    # also refresing the expiry timeout
    # to show that it was recently used.
    def get(self, key: int):
        with self.lock:
            if self._has_expired(key):
                self._delete(key)                
            if key not in self.cache:
                return -1
            else:
                self.cache.move_to_end(key)            
                self.global_expiry[key] = time.time()
                return self.cache[key]
 
    # first, we add / update the key by conventional methods.
    # And also move the key to the end to show that it was recently used.
    # But here we will also check whether the length of our
    # ordered dictionary has exceeded our capacity,
    # If so we remove the first key (least recently used)
    # also refresh the expiry time
    def put(self, key: int, value: int):
        with self.lock:
            print(len(self.cache))
            if len(self.cache) > self.capacity:
                self.cache.popitem(last = False)         
            self.cache[key] = value            
            self.cache.move_to_end(key)
            self.global_expiry[key] = time.time()            
                        
            
    def _delete(self, key):
        try:
            del self.cache[key]
            del self.global_expiry[key]
        except KeyError:
            return False
        return True
    
    def _has_expired(self, key):
        exp = self.global_expiry.get(key, -1)
        current_time = time.time()             
        active_time = current_time - exp
        if (exp is not None and active_time >=env['CACHE.EXPIRY']):            
            return True
        else:
            return False 