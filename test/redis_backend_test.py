from io import StringIO
import io
from time import sleep
from unittest import mock ,IsolatedAsyncioTestCase
from src import redis_backend
import sys
import asyncio


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    

class TestBackEnd(IsolatedAsyncioTestCase):    
  
    # async def test_none_get_redisCache(self):             
    #     expected_result = None          
    #     acutal_result = await redis_backend.get_redis_value('username')
    #     self.assertEqual(acutal_result, expected_result)
    
    
    # @mock.patch('builtins.print')
    # async def test_invalid_get_redisCache(self,mock_print):
    #     sys.stdout.flush()
    #     acutal_result = await redis_backend.get_redis_value('test')            
    #     mock_print.assert_called_with('Not Found in local cache..')    
        
    @mock.patch('builtins.print')
    async def test_valid_get_redisCache(self,mock_print):
        sys.stdout.flush()
        #saving to local cache
        await redis_backend.get_redis_value('0')
        acutal_result = await redis_backend.get_redis_value('0')            
        mock_print.assert_called_with('Found in local cache..')
    
    @mock.patch('builtins.print')
    async def test_save_get_redisCache(self,mock_print):
        sys.stdout.flush()
        #saving to local cache
        await redis_backend.get_redis_value('0')
        acutal_result = await redis_backend.get_redis_value('test')            
        mock_print.assert_called_with('Saving to local cache...')
        

