from cryptography.fernet import Fernet

# 固定密鑰（可改為環境變數或 config）
KEY = Fernet.generate_key()
fernet = Fernet(KEY)

def encrypt_content(content: str) -> str:
    return fernet.encrypt(content.encode()).decode()

def decrypt_content(token: str, key: bytes = KEY) -> str:
    try:
        return Fernet(key).decrypt(token.encode()).decode()
    except Exception:
        return "[解密失敗]"
