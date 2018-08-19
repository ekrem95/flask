from flask import jsonify
from json import loads
from jwt import decode
from models.user import User
from models.access_token import verify
from .response import err_response

not_found_err = "'NoneType' object is not iterable"

def UserInfo(request):
    auth_header = request.headers.get('Authorization')

    try:    
        user_id = verify(auth_header)
        user = User()

        id, name = user.findById(id=user_id)

        return jsonify({
            'id': id, 'name': name
        })
    except Exception as e:
        return err_response(str(e))
