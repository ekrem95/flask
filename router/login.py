from flask import jsonify
from json import loads
from models.user import User
from models.access_token import generate_access_token
from models.client import generate_client
from .response import err_response

not_found_err = "'NoneType' object is not iterable"

def Login(request):    
    if not request.json:
        return err_response('Request must have "Content-Type: application/json" header')

    data = loads(request.data)
    
    if 'name' not in data or 'password' not in data:
        return err_response('Request is missing required parameter(s)')

    name=data['name']    
    password=data['password']    
    user = User(name=name, password=password)

    try:
        id, hash = user.find()

        if not user.compare_passwords(password, bytes(hash)):
            return err_response('Passwords do not match')

        client = generate_client()
        print(generate_access_token(client_id=client['id'], user_id=id))
    except Exception as e:
        if str(e) == not_found_err:
            return err_response('User not found')
        return err_response(str(e))

    return jsonify(data)
