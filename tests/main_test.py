import os
import time
from fastapi.testclient import TestClient
from unittest import mock ,TestCase
from unittest import mock ,IsolatedAsyncioTestCase
from fastapi.responses import JSONResponse
import logging
from src import main, redis_backend


client = TestClient(main.app)
   
async def get_redis_client():
      redis = await redis_backend._get_redis_client()
      return redis

class TestCalculator(IsolatedAsyncioTestCase):
   
   
   def mock_return_redis(value: str):
     return str.encode(value)

   def test_empty_get_redisCache(self):
      response = client.get("/redis/invalidTest")
      expected_result =  {'No value found in redis or local cache': ''}
      assert response.status_code == 200
      assert response.json() == expected_result


   def test_invalid_route_get_redisCache(self):
      response = client.get("/test")
      expected_result =  {'detail': 'Not Found'}
      assert response.status_code == 404
      assert response.json() == expected_result
      
   def test_empty_route_get_redisCache(self):
      response = client.get("/redis/")
      expected_result =  {'detail': 'Not Found'}
      assert response.status_code == 404
      assert response.json() == expected_result
          
   
   @mock.patch('src.main.get_redis_value', side_effect=mock_return_redis)  
   async def test_valid_route_get_redisCache(self,redis_mock):
      await redis_mock('testing')      
      result = client.get("/redis/testing") 
      expected_result =  {"value" : "testing"}       
      self.assertEqual(result.json(),expected_result)
      
   @mock.patch('src.main.get_redis_value', side_effect=mock_return_redis)  
   async def test_valid_number_route_get_redisCache(self,redis_mock):
      await redis_mock('1')      
      result = client.get("/redis/1") 
      expected_result =  {"value" : "1"}       
      self.assertEqual(result.json(),expected_result)
      
   @mock.patch('src.main.get_redis_value', side_effect=mock_return_redis)  
   async def test_valid_empty_route_get_redisCache(self,redis_mock):
      await redis_mock('')      
      result = client.get("/redis/ ") 
      expected_result =   ['invalid format']       
      self.assertEqual(result.json(),expected_result)
   
   async def test_end_to_end_valid(self):      
      redis = await get_redis_client() 
      await redis.set('testab','testcd')   
      expected_result =  {"value" : "testcd"}
      result = client.get("/redis/testab")           
      self.assertEqual(result.json(),expected_result)
      
   async def test_end_to_end_invalid(self): 
      expected_result =  {'No value found in redis or local cache' : ''}
      result = client.get("/redis/testoo")           
      self.assertEqual(result.json(),expected_result)
      
   async def test_end_to_end_valid(self):      
      redis = await get_redis_client()  
      await redis.set('testab','testcd')   
      expected_result =  {"value" : "testcd"}
      result = client.get("/redis/testab")           
      self.assertEqual(result.json(),expected_result)

   async def test_end_to_end_cached_valid(self):           
      redis = await get_redis_client()
      await redis.set('test01','testa')    
      expected_result =  {"value" : "testa"}
      client.get("/redis/test01") 
      client.get("/redis/test01")           
      with self.assertLogs(level='INFO') as log:         
         client.get("/redis/test01")   
         self.assertEqual(len(log.records), 1) # check that there is only one log message
         self.assertEqual(log.output, ['INFO:root: Found in local cache..'])
   
   def test_end_to_end_global_expiry(self):             
        os.environ['CACHE_EXPIRY'] = '1.0'
        client.get("/redis/test02")  
        time.sleep(1.5)
        with self.assertLogs(level='INFO') as log:         
         client.get("/redis/test02")
         self.assertEqual(len(log.output), 3)   
         self.assertEqual(log.output[0], 'INFO:root: Not found in local cache,feching from redis...')
   
   async def test_end_to_end_LRU(self):      
      redis = await get_redis_client()  
      await redis.set('testing01','testa')
      await redis.set('testing02','testb')
      await redis.set('testing03','testc') 
      os.environ['CACHE_SIZE'] = '1'
      os.environ['CACHE_EXPIRY'] = '1.0'  
      client.get("/redis/testing01")
      client.get("/redis/testing02")
      client.get("/redis/testing03")
      time.sleep(1.5)           
      with self.assertLogs(level='INFO') as log:         
         client.get("/redis/testing01")
         self.assertEqual(len(log.output), 3)   
         self.assertEqual(log.output[2], 'INFO:root: Saving to local cache...')
         
        