import os
import time
from unittest import mock ,IsolatedAsyncioTestCase
from src import local_cache
import sys
import asyncio


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
inmem_cache = local_cache.LRUCache()

class TestBackEnd(IsolatedAsyncioTestCase):    
    
    def test_not_in_cache_local_cache(self):       
        expected_result = -1     
        print(inmem_cache)    
        acutal_result = inmem_cache.get('test0')
        self.assertEqual(acutal_result, expected_result)  
    
    def test_in_cache_local_cache(self):       
        expected_result = 'test1'    
        inmem_cache.put('test','test1')    
        acutal_result = inmem_cache.get('test')
        self.assertEqual(acutal_result, expected_result) 
    
    def test_LRU_cache_local_cache(self):          
        inmem_cache.capacity = 2;    
        expected_result = -1
        inmem_cache.put('test1','hello') #0
        inmem_cache.put('test2','world') #1
        inmem_cache.put('test3','goodbye') #2
        inmem_cache.put('test4','takecare') #3  
        acutal_result = inmem_cache.get('test1')
        self.assertEqual(acutal_result, expected_result) 
        
    
    def test_global_expiry_in_cache_local_cache(self):       
        expected_result = -1         
        inmem_cache.put('test5','hello')   
        inmem_cache.global_expiry['test5'] = time.time()-25      
        inmem_cache._has_expired('test5')
        acutal_result = inmem_cache.get('test5')
        self.assertEqual(acutal_result, expected_result) 
    
    def test_has_expired_in_cache_local_cache(self):       
        expected_result = True         
        inmem_cache.put('test5','hello')   
        inmem_cache.global_expiry['test5'] = time.time()- (int(os.getenv('CACHE_EXPIRY')))
        acutal_result =  inmem_cache._has_expired('test5')
        self.assertEqual(acutal_result, expected_result) 

    def test_not_expired_in_cache_local_cache(self):       
        expected_result = False         
        inmem_cache.put('test5','hello')   
        time_till_expiry = time.time()+ (int(os.getenv('CACHE_EXPIRY')))
        inmem_cache.global_expiry['test5'] = time_till_expiry + 2
        acutal_result =  inmem_cache._has_expired('test5')
        self.assertEqual(acutal_result, expected_result) 
        
    def test_delete_in_cache_local_cache(self):       
        expected_result = True   
        inmem_cache.put('test6','test6')
        self.assertEqual(inmem_cache.get('test6'),'test6')
        acutal_result = inmem_cache._delete('test6')
        self.assertEqual(acutal_result, expected_result) 
    
    def test_delete_where_no_value_exist_in_cache_local_cache(self):       
        expected_result = False   
        acutal_result = inmem_cache._delete('test6')
        self.assertEqual(acutal_result, expected_result) 