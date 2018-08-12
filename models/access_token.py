from time import time
from uuid import uuid4
from lib.memcache import client as memcache_client
from jwt import encode, decode
# from datetime import datetime

expires_in = 60 * 60 * 24 * 30 # one month
key = 'secret'
malformed_access_token = 'Malformed access token'

def generate_access_token(client_id, user_id):
    return {
        "id": str(uuid4()),
        "client_id": client_id,
        "user_id": str(user_id),
        "expires_in": expires_in,
        "created": int(time()),
    }

def sign_token(user_id, client, access_token):
    memcache_client.set('client_' + user_id, {
        "id": client['id'],
        "created": client['created'],
        })
    memcache_client.set('atoken_' + user_id, {
        "id": access_token['id'],
        "client_id": access_token['client_id'],
        "user_id": access_token['user_id'],
        "expires_in": access_token['expires_in'],
        "created": access_token['created'],
        })

    encoded = encode({
        "client_id": client['id'],
        "access_token_id": access_token['id'],
        "user_id": user_id,
        }, key, algorithm='HS256')

    return encoded

def verify(auth_header):
    if auth_header is None:
        raise ValueError('Missing authorization header')

    decoded = decode(auth_header, key, algorithms=['HS256'])

    client_id = decoded['client_id'] if 'client_id' in decoded else None
    access_token_id = decoded['access_token_id'] if 'access_token_id' in decoded else None
    user_id = decoded['user_id'] if 'user_id' in decoded else None

    if client_id is None or access_token_id is None or user_id is None:
        raise ValueError(malformed_access_token)
        
    if memcache_client.get('client_' + user_id)['id'] != client_id:
        raise ValueError(malformed_access_token)

    access_token = memcache_client.get('atoken_' + user_id)

    if access_token['id'] != access_token_id or access_token['client_id'] != client_id or access_token['user_id'] != user_id:
        raise ValueError(malformed_access_token)
    
    return user_id
