from time import time
from uuid import uuid4

def generate_client():
    return {
        "id": str(uuid4()),
        "created": int(time()),
        }
