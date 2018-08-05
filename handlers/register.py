from flask import jsonify
from json import loads
from models.user import User
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
    except Exception as e:
        return err_response(str(e))

    return jsonify(data)
