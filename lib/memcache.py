from json import dumps, loads
from pymemcache.client.base import Client

def json_serializer(key, value):
     if type(value) == str:
         return value, 1
     return dumps(value), 2

def json_deserializer(key, value, flags):
    if flags == 1:
        return value.decode('utf-8')
    if flags == 2:
        return loads(value.decode('utf-8'))
    raise Exception("Unknown serialization format")
 

client = Client(('localhost', 11211), serializer=json_serializer,
                deserializer=json_deserializer) 