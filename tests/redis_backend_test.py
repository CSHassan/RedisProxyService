import logging
import fakeredis.aioredis
from time import sleep
from unittest import mock ,IsolatedAsyncioTestCase
from src import redis_backend
import sys
import asyncio


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TestBackEnd(IsolatedAsyncioTestCase):
    async def get_fake_redis():
        fake_server = fakeredis.aioredis.FakeRedis()
        await fake_server.set('test','test123')
        return fake_server
    
    @mock.patch('src.redis_backend._check_local_cache', return_value='test')  
    async def test_valid_get_redisCache(self,mock_local_cache):
        mock_local_cache('test')            
        expected_result = 'test'          
        acutal_result = await redis_backend.get_redis_value('username')
        self.assertEqual(acutal_result, expected_result)
    
    @mock.patch('src.redis_backend._check_local_cache', return_value= -1)  
    @mock.patch('src.redis_backend._get_redis_client',side_effect= get_fake_redis)
    async def test_invalid_at_client_get_redisCache(self,mock_redis,mock_local_val):
        mock_local_val()
        await mock_redis()            
        expected_result = None          
        acutal_result = await redis_backend.get_redis_value('hello')
        self.assertEqual(acutal_result, expected_result)    
        
    @mock.patch('src.redis_backend._check_local_cache', return_value= -1)  
    @mock.patch('src.redis_backend._get_redis_client',side_effect= get_fake_redis)
    async def test_valid_return_value_get_redisCache(self,mock_redis,mock_local_val):
        mock_local_val()
        await mock_redis()   
        expected_result = b'test123'          
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
        expected_result = -1         
        acutal_result = await redis_backend._get_redis_client() 
        with self.assertLogs('root', level='INFO') as cm:
            logging.getLogger('root').info('Not found in local cache,feching from redis...')
            self.assertEqual(cm.output, ['INFO:root:Not found in local cache,feching from redis...'])

      
    @mock.patch('src.redis_backend.redis',side_effect= get_fake_redis)
    async def test_invalid_fakeredis_get_redis_client(self,mock_redis):        
        fake_redis=await mock_redis()            
        expected_result =  False       
        acutal_result = await redis_backend._get_redis_client()
        self.assertEqual(acutal_result, expected_result)    