from cryptography.fernet import Fernet

def generate_key():
     return Fernet.generate_key()


def encrypt_file(file_path, key):
    cipher = Fernet(key)
    with open(file_path, "rb") as file:
         original = file.read()
    encrypted = cipher.encrypt(original)
    with open(file_path, "wb") as file:
        file.write(encrypted)

def decrypt_file(file_path, key):
    cipher = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted = file.read()
    decrypted = cipher.decrypt(encrypted)
    with open(file_path, "wb") as file:
        file.write(decrypted)