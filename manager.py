from cryptography.fernet import Fernet
import pass_db
import argparse

class Manager():
    def __init__(self, user, key, database = ""):
        self.user = user
        self.key = key
        self.db = database

        # make Fernet object for encryption/decryption
        self.f = Fernet(self.key)

    def return_all_passwords(self) -> dict:
        # returns a dict with all decrypted passwords
        pass_list = pass_db.return_all_records(self.user)
        all_values = {}

        if pass_list:
            for value in pass_list:
                all_values[value[0]] = [self.f.decrypt(value[1]).decode(), self.f.decrypt(value[2]).decode()]

        return all_values
    
    def delete_all_passwords(self):
        pass_db.delete_all(self.user)

    def delete_from_db(self, id: int):
        pass_db.delete_from_database(id)

    def create_user(self):
        pass_db.create_user(self.user, self.key)

    def print_all_passwords(self):
        pass_list = pass_db.return_all_records(self.user)

        if pass_list:
            for value in pass_list:
                print(f"{value[0]}:")
                print(f"\tName: {self.f.decrypt(value[1]).decode()}")
                print(f"\tPassword: {self.f.decrypt(value[2]).decode()}")

    def save_to_database(self, user, password):
        pass_db.add_to_database(pass_db.check_current_index() + 1, self.user, pass_db.check_current_pass_index(self.user) + 1, self.f.encrypt(bytes(user, 'utf-8')).decode(), self.f.encrypt(bytes(password, 'utf-8')).decode())

    def update_record(self, index, user, password):
        pass_db.update_database(index, self.user, self.f.encrypt(bytes(user, 'utf-8')).decode(), self.f.encrypt(bytes(password, 'utf-8')).decode())

# run as cmd if not imported
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog='PasswordManager v0.1',
        description='Manage your password, securely.',
    )
    arg_parser.add_argument('-u', '--user', type=str)
    arg_parser.add_argument('-k', '--key', type=str)
    arg_parser.add_argument('-cu', '--create_user', action='store_true')
    args = arg_parser.parse_args()

    if args.create_user:
        new_user = input("Enter your new username: ")
        new_key = Fernet.generate_key().decode()

        print(f"[!] NEW KEY CREATED, SAVE IT [!]\n\t{new_key}")

        Pass_Manager = Manager(new_user, new_key)
        Pass_Manager.create_user()
        exit()

    USER = args.user
    KEY =  args.key

    print("PasswordManager v0.1")
    print("\nWhat would you like to do?")
    print("\n1.Retreive all\n2.Add Password\n3.Delete Record\n4.Delete All Passwords\n5.Update Record\n6.Exit\n")
    
    with open(KEY, "r") as key_file:
        KEY = key_file.read()
    
    Pass_Manager = Manager(USER, KEY)

    while True:
        try:
            choice = input(">")

            if choice.isnumeric():
                match int(choice):
                    case 1:
                        Pass_Manager.print_all_passwords()
                    case 2:
                        name = input("Name: ")
                        password = input("Password: ")
                        Pass_Manager.save_to_database(name, password)

                    case 3:
                        id = input("ID of record you wish to delete>")

                        if id.isnumeric():
                            Pass_Manager.delete_from_db(int(id))

                    case 4:
                        delete = input("Delete all records? y/n>")
                        if delete == "y":
                            Pass_Manager.delete_all_passwords()

                    case 5:
                        index = input("Which record would you like to update? (index)")

                        if index.isnumeric():
                            name = input("Name: ")
                            password = input("Password: ")
                            Pass_Manager.update_record(int(index), name, password)

                    case 6:
                        pass_db.close_db()
                        exit()

                    case 99:
                        print(Pass_Manager.return_all_passwords())
        except KeyboardInterrupt:
            pass_db.close_db()
            exit()