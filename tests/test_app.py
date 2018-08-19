from app import app
import base64, json, unittest
from lib.psql import exec, query
from lib.memcache import client as memcache_client

# python -m unittest filename.py
test_name = 'test_name'
test_pass = 'test_pass'

class Tests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_00_clean_up(self):
        results = query("SELECT id FROM users WHERE name = %s;", (test_name,))
        if results is None:
            return

        user_id, = results
        access_token = memcache_client.get('atoken_' + str(user_id))
        client = memcache_client.get('client_' + str(user_id))

        if access_token is not None:
            memcache_client.delete('atoken_' + str(user_id))

        if client is not None:
            memcache_client.delete('client_' + str(user_id))

        exec("DELETE FROM users WHERE name = %s;", (test_name,))

    def test_01_register(self):
        r = self.app.post('/user')
        assert r.status == '400 BAD REQUEST'
        assert b'{"message":"Request must have \\"Content-Type: application/json\\" header"}\n' == r.data

    def test_02_register(self):
        r = self.app.post('/user', json={'name': 'test_name'})
        assert r.status == '400 BAD REQUEST'
        assert b'{"message":"Request is missing required parameter(s)"}\n' == r.data

    def test_03_register(self):
        r = self.app.post('/user', json={
        'name': test_name, 'password': test_pass
        })
        assert r.status == '200 OK'
        assert b'{"access_token":"' in r.data

    def test_04_login(self):
        r = self.app.post('/login')
        assert r.status == '400 BAD REQUEST'
        assert b'{"message":"Request must have \\"Content-Type: application/json\\" header"}\n' == r.data

    def test_05_login(self):
        r = self.app.post('/login', json={'name': 'test_name'})
        assert r.status == '400 BAD REQUEST'
        assert b'{"message":"Request is missing required parameter(s)"}\n' == r.data

    def test_06_login(self):
        r = self.app.post('/login', json={
        'name': 'random_name', 'password': test_pass
        })
        assert r.status == '400 BAD REQUEST'
        assert b'{"message":"User not found"}\n' == r.data

    def test_07_login(self):
        r = self.app.post('/login', json={
        'name': test_name, 'password': test_pass
        })
        assert r.status == '200 OK'
        assert b'{"access_token":"' in r.data

    def test_08_user_info(self):
        r = self.app.get('/user')
        assert r.status == '400 BAD REQUEST'
        assert b'{"message":"Missing authorization header"}\n' == r.data

    def test_09_user_info(self):
        r = self.app.get('/user', headers={'Authorization': 'null'})
        assert r.status == '400 BAD REQUEST'
        assert b'{"message":"Not enough segments"}\n' == r.data

    def test_10_user_info(self):
        # login and use access token
        r = self.app.post('/login', json={'name': test_name, 'password': test_pass})
        assert r.status == '200 OK'
        assert b'{"access_token":"' in r.data

        decoded = r.data.decode('utf-8')
        json_data = json.loads(decoded)
        auth_header = json_data['access_token']
        # --------------------------------------------------------------------
        r = self.app.get('/user', headers={'Authorization': auth_header})
        assert r.status == '200 OK'

        decoded = r.data.decode('utf-8')
        json_data = json.loads(decoded)

        assert type(json_data['id']) == int
        assert json_data['name'] == test_name
