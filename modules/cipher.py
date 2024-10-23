from cryptography.fernet import Fernet

# 鍵作成
def create_key():
    key = Fernet.generate_key()
    print(key.decode('utf-8'))
    return key.decode('utf-8')

# 暗号化する
def encrypt(key: str, data: str):
    fernet = Fernet(bytes(key, 'utf-8'))
    encrypted_pass = fernet.encrypt(bytes(data, 'utf-8'))
    print(encrypted_pass.decode('utf-8'))
    return encrypted_pass.decode('utf-8')

# 復号する
def decrypt(key: str, data: str):
    fernet = Fernet(bytes(key, 'utf-8'))
    decrypted_pass = fernet.decrypt(bytes(data, 'utf-8'))
    print(decrypted_pass.decode('utf-8'))
    return decrypted_pass.decode('utf-8')

# password = 'password'
# key = create_key()

# encrypted_pass = encrypt(key, password)
# decrypt(key, encrypted_pass)