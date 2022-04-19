# Redis Proxy Service

Hi my name is Hassan and this is my first python project ( well at least the first finished one)

This is an asynchronous service that will provide an HTTP overlay to a Redis background service that is able to add functionality such as a local cache using fast API. The local cache is an LRU cache system with Time To Kill or TTL/ Global expiry
Any time a local cache item is called its timer gets reset to the global_expiry time. The cache also has a limit rate that allows you to only have the N Top used local cache.

## Local Cache Algorithm

The local cache is made up of 4 objects:
cache which is an ordered dictionary where the values are stored.
capacity, which defines how many objects can be stored until the LRU starts
global_expiry which is a dictionary where we will store the key from the cache and the value will be the current time
lock , which will provide us to perform these actions in a thread-safe manner


## Installation

use make to download the requirements and build the project 

```bash
make build
```

## Run and Test

after the build has finished downloading everything has been download, you can test and run it with these commands:


run uvicorn on specified variables defined in the .env file
```cmd
make run
```

```diff
-Please make sure before the test you have run the make build command and download requirements , also you need to have a 
- redis server up and running or the backend / end-to-end test will fail
``` 


```cmd
make test
```

## Debug

since I used windows machine with wsl2, some of my configurations might be a bit different compared to your machine. for example in docker and docker-compose I had to put ``` --host 0.0.0.0 --port 8000 ``` 
under the build command as wsl2  networking localhost is different than my machine localhost.

