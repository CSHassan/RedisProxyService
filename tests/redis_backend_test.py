import logging
from time import sleep
from unittest import mock ,IsolatedAsyncioTestCase
from src import redis_backend
import sys
import asyncio


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TestBackEnd(IsolatedAsyncioTestCase):    
    
    @mock.patch('src.redis_backend._check_local_cache', return_value='test')  
    async def test_valid_get_redisCache(self,mock_local_cache):
        mock_local_cache('test')            
        expected_result = 'test'          
        acutal_result = await redis_backend.get_redis_value('username')
        self.assertEqual(acutal_result, expected_result)
    
    async def test_invalid_at_client_get_redisCache(self):                  
        expected_result = None          
        acutal_result = await redis_backend.get_redis_value('hello')
        self.assertEqual(acutal_result, expected_result)    
        
    
    async def test_valid_return_value_get_redisCache(self):         
        expected_result = b'test123'  
        redis = await redis_backend._get_redis_client()  
        await redis.set('test','test123')   
        acutal_result = await redis_backend.get_redis_value('test')
        self.assertEqual(acutal_result, expected_result)    
    
    def test_valid_set_local_cache(self):       
        expected_result = None         
        acutal_result =  redis_backend._set_local_cache('test0','test0')
        self.assertEqual(acutal_result, expected_result)    
 
    def test_found_in_local_cache_check_local_cache(self):       
        expected_result = -1         
        acutal_result =  redis_backend._check_local_cache('test0')
        self.assertEqual(acutal_result, expected_result)  
        
    @mock.patch.object(redis_backend.LRUCache, 'get')  
    def test_not_found_in_local_cache_check_local_cache(self,mock_inmem_cache):  
        mock_inmem_cache.return_value='hello'            
        expected_result = 'hello'         
        acutal_result =  redis_backend._check_local_cache('test0')
        self.assertEqual(acutal_result, expected_result)  
    
    async def test_invalid_get_redis_client(self):                  
        await redis_backend._get_redis_client() 
        with self.assertLogs('root', level='INFO') as cm:
            logging.getLogger('root').info('Not found in local cache,feching from redis...')
            self.assertEqual(cm.output, ['INFO:root:Not found in local cache,feching from redis...'])
     
   