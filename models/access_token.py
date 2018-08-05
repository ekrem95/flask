from time import time
from uuid import uuid4
from lib.memcache import client as memcache_client
# from datetime import datetime

expires_in = 60 * 60 * 24 * 30 # one month

def generate_access_token(client_id, user_id):
    return {
        "id": str(uuid4()),
        "client_id": client_id,
        "user_id": user_id,
        "expires_in": expires_in,
        "created": int(time()),
    }

def response(user_id, client, access_token):
    _token = {
        "client_id": client['id'],
        "access_token_id": access_token['id'],
    }

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
    # print(memcache_client.get('atoken_' + user_id))
