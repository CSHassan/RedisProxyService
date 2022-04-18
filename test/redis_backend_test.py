import fakeredis
from time import sleep
from unittest import mock ,IsolatedAsyncioTestCase
from src import redis_backend
import sys
import asyncio


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    

class TestBackEnd(IsolatedAsyncioTestCase):
    def get_fake_redis():
        fake_server = fakeredis.FakeServer()  
        return fakeredis.FakeStrictRedis(server=fake_server)
    
    @mock.patch('src.redis_backend._check_local_cache', return_value='test')  
    async def test_valid_get_redisCache(self,mock_local_cache):
        mock_local_cache('test')            
        expected_result = 'test'          
        acutal_result = await redis_backend.get_redis_value('username')
        self.assertEqual(acutal_result, expected_result)
    
    
    @mock.patch('src.redis_backend._get_redis_client',side_effect= get_fake_redis)
    async def test_invalid_get_redisCache(self,mock_redis):
        await mock_redis()            
        expected_result = False          
        acutal_result = await redis_backend.get_redis_value('test')
        self.assertEqual(acutal_result, expected_result)    
        
    # @mock.patch('builtins.print')
    # async def test_valid_get_redisCache(self,mock_print):
    #     sys.stdout.flush()
    #     #saving to local cache
    #     await redis_backend.get_redis_value('0')
    #     acutal_result = await redis_backend.get_redis_value('0')            
    #     mock_print.assert_called_with('Found in local cache..')
    
    # @mock.patch('builtins.print')
    # async def test_save_get_redisCache(self,mock_print):
    #     sys.stdout.flush()
    #     #saving to local cache
    #     await redis_backend.get_redis_value('0')
    #     acutal_result = await redis_backend.get_redis_value('test')            
    #     mock_print.assert_called_with('Saving to local cache...')
        

