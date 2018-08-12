from flask import jsonify
from json import loads
from models.user import User
from models.access_token import generate_access_token, sign_token
from models.client import generate_client
from .response import err_response

def Register(request):    
    if not request.json:
        return err_response('Request must have "Content-Type: application/json" header')

    data = loads(request.data)
    
    if 'name' not in data or 'password' not in data:
        return err_response('Request is missing required parameter(s)')
    
    user = User(name=data['name'], password=data['password'])

    try:
        user.save()
        id, _ = user.find()

        client = generate_client()
        access_token = generate_access_token(client_id=client['id'], user_id=id)

        encoded = sign_token(str(id), client, access_token)
        
        return jsonify({'access_token': encoded})
    except Exception as e:
        return err_response(str(e))