from cryptography.fernet import Fernet
import argparse
import manager

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

        Pass_Manager = manager.Manager(new_user, new_key)
        Pass_Manager.create_user()
        exit()

    USER = args.user
    KEY =  args.key

    print("PasswordManager v0.1")
    print("\nWhat would you like to do?")
    print("\n1.Retreive all\n2.Add Password\n3.Delete Record\n4.Delete All Passwords\n5.Update Record\n6.Exit\n")
    
    with open(KEY, "r") as key_file:
        KEY = key_file.read()
    
    Pass_Manager = manager.Manager(USER, KEY)
    
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
                        Pass_Manager.pass_db.close_db()
                        exit()

                    case 99:
                        print(Pass_Manager.return_all_passwords())
        except KeyboardInterrupt:
            Pass_Manager.pass_db.close_db()
            exit()