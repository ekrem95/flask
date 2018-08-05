from flask import jsonify

def err_response(message):
    content = {'message': message}
    return jsonify(content), 400