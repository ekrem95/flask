from lib.psql import exec

def setup():
    exec("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, name varchar unique, password bytea);")

setup()