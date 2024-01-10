import sqlite3

try:
    with open("pass.db", 'r') as db:
        pass
    conn = sqlite3.connect('pass.db')
except FileNotFoundError:
    conn = sqlite3.connect('pass.db')

    conn.execute("""CREATE TABLE PASSWORDS
                 (id INT PRIMARY KEY    NOT NULL,
                 user_id TEXT NOT NULL,
                 pass_id INT NOT NULL,
                 name   TEXT NOT NULL,
                 password   TEXT NOT NULL); 
                 """)
    
    conn.execute("""CREATE TABLE USERS
                 (name  TEXT PRIMARY KEY    NOT NULL,
                 password   TEXT NOT NULL);
                 """)
    

def return_all_records(user) -> list:
    
    return conn.execute(f"""SELECT pass_id, name, password FROM passwords WHERE user_id = ?""", (user,))


def add_to_database(id: int, user: str, pass_id: int, name: str, password: str):
    conn.execute(f"""INSERT INTO PASSWORDS (ID,USER_ID,PASS_ID,NAME,PASSWORD)
                 VALUES (?, ?, ?, ?, ?)""", (id, user, pass_id, name, password))
    conn.commit()

def create_user(name: str, password: str):
    conn.execute(f"""INSERT INTO users (name,password)
                 VALUES (?, ?)""", (name, password))
    conn.commit()

def update_database(id, user_id, name, password):

    conn.execute(f"""UPDATE PASSWORDS
                     SET name = ? , password = ?
                     WHERE pass_id = ? AND user_id = ?""", (name, password, id, user_id))
    conn.commit()

def delete_from_database(id: int):
    conn.execute(f"""DELETE FROM PASSWORDS
                 WHERE ID = ?""", (id,))
    conn.commit()

def delete_all(user_id):
    conn.execute("DELETE FROM PASSWORDS WHERE user_id = ?", (user_id,))
    conn.commit()

def check_current_index() -> int:
    query = conn.execute(f"""SELECT id from PASSWORDS""")

    try:
        
        return query.fetchall()[-1][0]
    except IndexError:
        return 0

def check_current_pass_index(user) -> int:
    try:
        query = conn.execute(f"""SELECT pass_id FROM passwords WHERE user_id = ?""", (user,))
        try:
            return query.fetchall()[-1][0]
        except IndexError:
            return 0
    except sqlite3.OperationalError as e:
        return 0

def close_db():
    conn.close()
