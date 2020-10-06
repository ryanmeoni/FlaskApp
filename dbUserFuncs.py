import sqlite3

db_conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = db_conn.cursor()


def create_tables():
    global cursor, db_conn
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username text, email text, password text)")
    db_conn.commit()


def create_user(username, email, password):
    global cursor, db_conn
    cursor.execute(f"INSERT INTO users VALUES ('{username}', '{email}', '{password}')")
    db_conn.commit()


def get_user(username):
    global cursor, db_conn
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    for row in cursor:
        if row[0] == username:
            return row

        return None


def check_if_user_exists(username):
    global cursor, db_conn
    result = cursor.execute(f"SELECT COUNT(*) FROM users WHERE username = '{username}'")

    # Check if the query matched any values.
    for row in result:
        if row[0] == 0:
            return False
        else:
            return True


def delete_tables():
    global cursor
    cursor.execute("DROP TABLE IF EXISTS users")
    db_conn.commit()


def clean_up():
    global cursor
    cursor.close()
    db_conn.close()
