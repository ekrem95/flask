from psycopg2 import connect

conn_str = 'host=localhost dbname=default user=root password=pass'

def exec(stmt, args=None):
    conn = connect(conn_str)
    cur = conn.cursor()

    cur.execute(stmt, args)
    conn.commit()

    cur.close()
    conn.close()

def query(stmt, args=None):
    conn = connect(conn_str)
    cur = conn.cursor()

    cur.execute(stmt, args)
    data = cur.fetchone()

    cur.close()
    conn.close()

    return data