from fastapi.testclient import TestClient
from unittest import mock ,TestCase

from src import main

client = TestClient(main.app)


def test_invalid_get_redisCache():
   response = client.get("/redis/invalidTest")
   expected_result =  ["No value found in cache"]
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