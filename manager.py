from cryptography.fernet import Fernet
import hashlib
import pass_db as db



class Manager():
    def __init__(self, user, key, database = ""):
        self.user = user
        self.key = key
        self.db = database

        # make Fernet object for encryption/decryption
        self.f = Fernet(self.key)
        self.pass_db = db.Database(self.user, hashlib.md5(self.key.encode('utf-8')).hexdigest())

        self.login_user()

    def return_all_passwords(self) -> dict:
        # returns a dict with all decrypted passwords
        pass_list = self.pass_db.return_all_records(self.user)
        all_values = {}

        if pass_list:
            for value in pass_list:
                all_values[value[0]] = [self.f.decrypt(value[1]).decode(), self.f.decrypt(value[2]).decode()]

        return all_values
    
    def delete_all_passwords(self):
        self.pass_db.delete_all(self.user)

    def delete_from_db(self, id: int):
        self.pass_db.delete_from_database(self.user, id)

    def create_user(self):
        self.pass_db.create_user(self.user, hashlib.md5(self.key.encode('utf-8')).hexdigest())

    def login_user(self):
        if self.pass_db.user_login_check():
            print("[!] LOGIN OK [!]")

    def print_all_passwords(self):
        pass_list = self.pass_db.return_all_records(self.user)

        if pass_list:
            for value in pass_list:
                print(f"{value[0]}:")
                print(f"\tName: {self.f.decrypt(value[1]).decode()}")
                print(f"\tPassword: {self.f.decrypt(value[2]).decode()}")

    def save_to_database(self, user, password):
        self.pass_db.add_to_database(self.pass_db.check_current_index() + 1, self.user, self.pass_db.check_current_pass_index(self.user) + 1, self.f.encrypt(bytes(user, 'utf-8')).decode(), self.f.encrypt(bytes(password, 'utf-8')).decode())

    def update_record(self, index, user, password):
        self.pass_db.update_database(index, self.user, self.f.encrypt(bytes(user, 'utf-8')).decode(), self.f.encrypt(bytes(password, 'utf-8')).decode())
