import base64
import hashlib


class CryptoManager:
    """
    Crypto Manager v2
    - Password encryption (shift)
    - Vault encryption (key-based XOR)
    """

    SHIFT = 3

    def encrypt_password(self, text):
        encrypted = ""
        for char in text:
            encrypted += chr(ord(char) + self.SHIFT)
        return encrypted

    def decrypt_password(self, text):
        decrypted = ""
        for char in text:
            decrypted += chr(ord(char) - self.SHIFT)
        return decrypted

    def generate_key(self, master_password):
        return hashlib.sha256(master_password.encode()).digest()

    def encrypt_vault(self, data, key):

        data_bytes = data.encode()
        encrypted = bytearray()

        for i in range(len(data_bytes)):
            encrypted.append(
                data_bytes[i] ^ key[i % len(key)]
            )

        return base64.b64encode(encrypted).decode()

    def decrypt_vault(self, data, key):

        data_bytes = base64.b64decode(data.encode())
        decrypted = bytearray()

        for i in range(len(data_bytes)):
            decrypted.append(
                data_bytes[i] ^ key[i % len(key)]
            )

        return decrypted.decode()
