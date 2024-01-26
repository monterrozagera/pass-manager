import sqlite3

def open_database() -> sqlite3.Connection:
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
    return conn

class Database():
    def __init__(self, user, key_hash):
        self.user = user
        self.key_hash = key_hash
        self.conn = open_database()

    def user_login_check(self) -> bool:
        res = self.conn.execute("SELECT name, password FROM users WHERE name = ?", (self.user,))
        exists = res.fetchall()

        if exists:
            if exists[0][1] == self.key_hash:
                return True
        
        return False


    def return_all_records(self, user) -> list:
        if self.user_login_check():
            return self.conn.execute(f"""SELECT pass_id, name, password FROM passwords WHERE user_id = ?""", (user,))
        else:
            return []


    def add_to_database(self, id: int, user: str, pass_id: int, name: str, password: str):
        if self.user_login_check():
            self.conn.execute(f"""INSERT INTO PASSWORDS (ID,USER_ID,PASS_ID,NAME,PASSWORD)
                        VALUES (?, ?, ?, ?, ?)""", (id, user, pass_id, name, password))
            self.conn.commit()

    def create_user(self, name: str, password: str):
        if not self.user_login_check():
            self.conn.execute(f"""INSERT INTO users (name,password)
                        VALUES (?, ?)""", (name, password))
            self.conn.commit()
        else:
            print("[!] Error creating user [!]")

    def update_database(self, id, user_id, name, password):
        if self.user_login_check():
            self.conn.execute(f"""UPDATE PASSWORDS
                            SET name = ? , password = ?
                            WHERE pass_id = ? AND user_id = ?""", (name, password, id, user_id))
            self.conn.commit()

    def delete_from_database(self, user, id: int):
        if self.user_login_check():
            self.conn.execute(f"""DELETE FROM PASSWORDS
                        WHERE user_id =? AND pass_id = ?""", (user,id))
            self.conn.commit()

    def delete_all(self, user_id):
        if self.user_login_check():
            self.conn.execute("DELETE FROM PASSWORDS WHERE user_id = ?", (user_id,))
            self.conn.commit()

    def check_current_index(self, ) -> int:
        if self.user_login_check():
            query = self.conn.execute(f"""SELECT id from PASSWORDS""")

            try:

                return query.fetchall()[-1][0]
            except IndexError:
                return 0
        else:
            return 0

    def check_current_pass_index(self, user) -> int:
        if self.user_login_check():
            try:
                query = self.conn.execute(f"""SELECT pass_id FROM passwords WHERE user_id = ?""", (user,))
                try:
                    return query.fetchall()[-1][0]
                except IndexError:
                    return 0
            except sqlite3.OperationalError:
                return 0
        else:
            return 0

    def close_db(self, ):
        self.conn.close()
