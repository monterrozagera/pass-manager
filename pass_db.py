import sqlite3

class Database():
    def init(self, path):
        try:
            with open("pass.db", 'r') as db:
                pass
            self.conn = sqlite3.connect('pass.db')
        except FileNotFoundError:
            self.conn = sqlite3.connect('pass.db')

            self.conn.execute("""CREATE TABLE PASSWORDS
                        (id INT PRIMARY KEY    NOT NULL,
                        user_id TEXT NOT NULL,
                        pass_id INT NOT NULL,
                        name   TEXT NOT NULL,
                        password   TEXT NOT NULL); 
                        """)

            self.conn.execute("""CREATE TABLE USERS
                        (name  TEXT PRIMARY KEY    NOT NULL,
                        password   TEXT NOT NULL);
                        """)


    def return_all_records(self, user) -> list:

        return self.conn.execute(f"""SELECT pass_id, name, password FROM passwords WHERE user_id = ?""", (user,))


    def add_to_database(self, id: int, user: str, pass_id: int, name: str, password: str):
        self.conn.execute(f"""INSERT INTO PASSWORDS (ID,USER_ID,PASS_ID,NAME,PASSWORD)
                    VALUES (?, ?, ?, ?, ?)""", (id, user, pass_id, name, password))
        self.conn.commit()

    def create_user(self, name: str, password: str):
        self.conn.execute(f"""INSERT INTO users (name,password)
                    VALUES (?, ?)""", (name, password))
        self.conn.commit()

    def update_database(self, id, user_id, name, password):

        self.conn.execute(f"""UPDATE PASSWORDS
                        SET name = ? , password = ?
                        WHERE pass_id = ? AND user_id = ?""", (name, password, id, user_id))
        self.conn.commit()

    def delete_from_database(self, id: int):
        self.conn.execute(f"""DELETE FROM PASSWORDS
                    WHERE ID = ?""", (id,))
        self.conn.commit()

    def delete_all(self, user_id):
        self.conn.execute("DELETE FROM PASSWORDS WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def check_current_index(self, ) -> int:
        query = self.conn.execute(f"""SELECT id from PASSWORDS""")

        try:

            return query.fetchall()[-1][0]
        except IndexError:
            return 0

    def check_current_pass_index(self, user) -> int:
        try:
            query = self.conn.execute(f"""SELECT pass_id FROM passwords WHERE user_id = ?""", (user,))
            try:
                return query.fetchall()[-1][0]
            except IndexError:
                return 0
        except sqlite3.OperationalError as e:
            return 0

    def close_db(self, ):
        self.conn.close()
