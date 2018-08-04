import bcrypt
from lib.psql import exec, query

class User():
    def __init__(self, name, password):
        self.id = ''
        self.name = name
        self.password = self.generate_password(password)

    def generate_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def compare_passwords(self, password, hash):
        return bcrypt.checkpw(password.encode('utf-8'), hash)

    def save(self):
        exec('INSERT INTO users (name, password) VALUES (%s, %s)', (self.name, self.password))

    def find(self):
        return query('SELECT id, password FROM users WHERE name = %s;', (self.name,))