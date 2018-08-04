from time import time
from uuid import uuid4
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
