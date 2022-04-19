import json
from fastapi.testclient import TestClient
from unittest import mock ,TestCase
from unittest import mock ,IsolatedAsyncioTestCase
from fastapi.responses import JSONResponse
from src import main, redis_backend


client = TestClient(main.app)


def test_empty_get_redisCache():
   response = client.get("/redis/invalidTest")
   expected_result =  {'No value found in redis or local cache': ''}
   assert response.status_code == 200
   assert response.json() == expected_result


def test_invalid_route_get_redisCache():
   response = client.get("/test")
   expected_result =  {'detail': 'Not Found'}
   assert response.status_code == 404
   assert response.json() == expected_result
   
def test_empty_route_get_redisCache():
   response = client.get("/redis/")
   expected_result =  {'detail': 'Not Found'}
   assert response.status_code == 404
   assert response.json() == expected_result
   
class TestCalculator(IsolatedAsyncioTestCase):
   
   def mock_return_redis(value: str):
          return str.encode(value)
          
   
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
      redis = await redis_backend._get_redis_client()  
      await redis.set('testab','testcd')   
      expected_result =  {"value" : "testcd"}
      result = client.get("/redis/testab")           
      self.assertEqual(result.json(),expected_result)
      
   async def test_end_to_end_invalid(self): 
      expected_result =  {'No value found in redis or local cache' : ''}
      result = client.get("/redis/testoo")           
      self.assertEqual(result.json(),expected_result)
      
