# TO DO:
# create a logic to see and send messages between users.
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
    webbrowser.open("https://github.com/Mr-Zanzibar/Enigma-Game-Python")


def check_windows_version():
    supported_versions = ["10", "11"]
    windows_version = platform.win32_ver()[0]
    major_version = windows_version.split('.')[0]
    if major_version in supported_versions:
        return True
    else:
        return False


def check_mac_version():
    supported_versions = ["12"]
    mac_version = platform.mac_ver()[0]
    major_version = mac_version.split('.')[1]
    if major_version in supported_versions:
        return True
    else:
        return False


def check_linux_version():
    supported_distributions = ["kali", "Kali Purple"]
    linux_distribution = platform.linux_distribution()[0]
    if linux_distribution.lower() in supported_distributions:
        return True
    else:
        return False


def main():
    if platform.system() == "Windows":
        if not check_windows_version():
            print("The program is only supported on Windows 10 and 11.")
            sys.exit(1)
    elif platform.system() == "Darwin":
        if not check_mac_version():
            print("The program is only supported on macOS 12 (Monterey).")
            sys.exit(1)
    elif platform.system() == "Linux":
        if not check_linux_version():
            print("The program is only supported on Kali Linux and Kali Purple.")
            sys.exit(1)
    else:
        print("Unsupported operating system.")
        sys.exit(1)

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

            encrypted_message = enigma.encrypt_message(message)
            # Logic to send the encrypted message to the recipient
            print("Encrypted message sent to the recipient.")

        elif choice == "2":
            # Logic to retrieve received messages for the user
            # Decrypt and display the messages

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
