from cryptography.fernet import Fernet
# 鍵作成
async def create_key():
    """
    暗号化・復号化する際に使用するKeyを生成します。

    Returns
    -------
        str: ランダムな文字列

    Example
    -------
    .. code-block:: python3
        key = create_key()
    """
    key = Fernet.generate_key()
    return key.decode('utf-8')

# 暗号化
async def encrypt(key: str, data: str):
    """
    keyを使用し与えられたデータを暗号化します。

    Parameters
    -------
        key(str): 暗号化に使用するkey
        data(str): 暗号化する文字列

    Returns
    -------
        str: 暗号化されたデータ

    Example
    -------
    .. code-block:: python3
        password = 'password'
        key = create_key()
        encrypted_password = encrypt(key, password)
    """
    fernet = Fernet(bytes(key, 'utf-8'))
    encrypted_pass = fernet.encrypt(bytes(data, 'utf-8'))
    return encrypted_pass.decode('utf-8')

# 復号化
async def decrypt(key: str, data: str):
    """
    keyを使用し与えられたデータを復号化します。

    Parameters
    -------
        key(str): 復号化に使用するkey
        data(str): 復号化する文字列

    Returns
    -------
        str: 復号化されたデータ

    Example
    -------
    .. code-block:: python3
        decrypt_password = decrypt(key, encrypted_password)
    """
    fernet = Fernet(bytes(key, 'utf-8'))
    decrypted_pass = fernet.decrypt(bytes(data, 'utf-8'))
    return decrypted_pass.decode('utf-8')