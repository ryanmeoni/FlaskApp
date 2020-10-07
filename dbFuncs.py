import sqlite3

db_conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = db_conn.cursor()


def create_tables():
    global cursor, db_conn
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username text, email text, password text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (sendingUser text, receivingUser text, messageContent text)")
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
        # Return None if no user exists with given username
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


def create_message(sendingUser, recievingUser, messageContent):
    global cursor, db_conn
    cursor.execute(f"INSERT INTO messages VALUES ('{sendingUser}', '{recievingUser}', '{messageContent}')")
    db_conn.commit()


# Used for debugging
def print_all_messages():
    global cursor, db_conn
    result = cursor.execute(f"SELECT * FROM messages")
    for row in result:
        print(row)


def get_all_messages_sent_to_user(username):
    global cursor, db_conn
    result = cursor.execute(f"SELECT * FROM messages WHERE receivingUser = '{username}'")
    return result


def delete_tables():
    global cursor
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS messages")
    db_conn.commit()


def clean_up():
    global cursor
    cursor.close()
    db_conn.close()
