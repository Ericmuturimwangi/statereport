from cryptography.fernet import Fernet
import tempfile

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
    
    # Create a temporary file to save the decrypted content
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    
    with open(file_path, "rb") as file:
        encrypted = file.read()

    # Decrypt the content
    decrypted = cipher.decrypt(encrypted)
    
    # Write the decrypted content to the temporary file
    with open(temp_file.name, "wb") as temp:
        temp.write(decrypted)

    return temp_file.name  # Return the path of the temporary file