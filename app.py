from flask import Flask, jsonify, request
from lib.memcache import client

from handlers.register import Register
from handlers.login import Login
from handlers.user_info import UserInfo
 
app = Flask(__name__)
                
@app.route("/")
def index():    
    client.set('key', {'a':'b', 'c':'d'})
    result = client.get('key')
    return jsonify(result)

@app.route("/user", methods=['GET','POST'])
def user():
    if request.method == 'GET':
        return UserInfo(request)
    if request.method == 'POST':
        return Register(request)

@app.route("/login", methods=['POST'])
def login():
    return Login(request)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
