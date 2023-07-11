# TO DO:
# create a better logic to see and recive and send messages between users.
# improve (a lot) the recognition of various operating systems.
import bcrypt
from cryptography.fernet import Fernet
import datetime
import random
import string
import ctypes
import sys
import webbrowser
import platform

class EnigmaMessaging:
    def __init__(self):
        self._hashed_password = None
        self._encryption_method = None
        self._password = None

    def generate_password(self):
        self._password = self._generate_random_password()
        self._hashed_password = bcrypt.hashpw(self._password.encode(), bcrypt.gensalt(rounds=12))

    def change_encryption_method(self):
        self._encryption_method = self._get_new_encryption_method()

    def encrypt_message(self, message):
        cipher = Fernet(self._password.encode())
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        cipher = Fernet(self._password.encode())
        decrypted_message = cipher.decrypt(encrypted_message.encode())
        return decrypted_message.decode()

    @staticmethod
    def _generate_random_password(length=10):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    @staticmethod
    def _get_new_encryption_method():
        encryption_methods = [
            "AES-256",
            "RSA",
            "Blowfish",
            "Twofish",
            "Serpent",
            "Camellia",
        ]
        return random.choice(encryption_methods)


def print_logo():
    logo = """
 ▓█████  ███▄    █  ██▓  ▄████  ███▄ ▄███▓ ▄▄▄      
▓█   ▀  ██ ▀█   █ ▓██▒ ██▒ ▀█▒▓██▒▀█▀ ██▒▒████▄    
▒███   ▓██  ▀█ ██▒▒██▒▒██░▄▄▄░▓██    ▓██░▒██  ▀█▄  
▒▓█  ▄ ▓██▒  ▐▌██▒░██░░▓█  ██▓▒██    ▒██ ░██▄▄▄▄██ 
░▒████▒▒██░   ▓██░░██░░▒▓███▀▒▒██▒   ░██▒ ▓█   ▓██▒
░░ ▒░ ░░ ▒░   ▒ ▒ ░▓   ░▒   ▒ ░ ▒░   ░  ░ ▒▒   ▓▒█░
 ░ ░  ░░ ░░   ░ ▒░ ▒ ░  ░   ░ ░  ░      ░  ▒   ▒▒ ░
   ░      ░   ░ ░  ▒ ░░ ░   ░ ░      ░     ░   ▒   
   ░  ░         ░  ░        ░        ░         ░  ░
                                                   
    """
    print(logo)


def run_as_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    except:
        print("Error while requesting administrator privileges.")
        sys.exit(1)


def show_credits():
    webbrowser.open("")


def check_supported_os():
    supported_os = ["Windows", "Darwin"]
    current_os = platform.system()

    if current_os not in supported_os:
        print("Unsupported operating system.")
        sys.exit(1)


def main():
    check_supported_os()

    enigma = EnigmaMessaging()

    run_as_admin()

    # User authentication
    print_logo()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    stored_hashed_password = b'$2b$12$SqRWHU21.AMzjYy41VmYUeWuJra4LZpSKeaAVh1qXRDcQwhP6exI6'
    if bcrypt.checkpw(password.encode(), stored_hashed_password):
        print("Authentication successful!")
        enigma._hashed_password = stored_hashed_password
    else:
        print("Authentication failed.")
        exit()

    # Main menu
    while True:
        print_logo()
        print("1. Send message")
        print("2. View received messages")
        print("3. Enigma Credits")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            recipient = input("Enter recipient's username: ")
            message = input("Enter message: ")

            # Encrypt the message
            encrypted_message = enigma.encrypt_message(message)

            # Send the encrypted message to the recipient
            send_message(recipient, encrypted_message)

            print("Encrypted message sent to the recipient.")

        elif choice == "2":
            print("Viewing received messages is not supported on this operating system.")

        elif choice == "3":
            show_credits()

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")

        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            enigma.generate_password()
            enigma.change_encryption_method()

    print("Exiting the application.")


if __name__ == "__main__":
    main()
