from flask import Flask, jsonify, request
from lib.memcache import client

from router.register import Register
from router.login import Login
 
app = Flask(__name__)
                
@app.route("/")
def index():    
    client.set('key', {'a':'b', 'c':'d'})
    result = client.get('key')
    return jsonify(result)

@app.route("/user", methods=['POST'])
def user():
    if request.method == 'POST':
        return Register(request)

    return '_'

@app.route("/login", methods=['POST'])
def login():
    return Login(request)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
