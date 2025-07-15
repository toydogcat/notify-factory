import os
import logging
from dotenv import load_dotenv
from cryptography.fernet import Fernet

class Master:
    def __init__(self):
        # check the .env file
        if not os.path.exists(".env"):
            ENV_KEY = Fernet.generate_key().decode()

            # 建立 .env 並寫入 ENV_KEY
            with open(".env", "w") as env_file:
                env_file.write(f"ENV_KEY={ENV_KEY}\n")
                logging.info(f'🔑 .env 檔案已建立並寫入 ENV_KEY')
        else:    
            load_dotenv()
            ENV_KEY = os.getenv("ENV_KEY")

            if not ENV_KEY:
                # if ENV_KEY is empty
                ENV_KEY = Fernet.generate_key().decode()
                with open(".env", "w") as env_file:
                    env_file.write(f"ENV_KEY={ENV_KEY}\n")
                    logging.info(f'🔑 .env 檔案已更新並寫入新的 ENV_KEY')
            else:
                logging.info(f'🔑 ENV_KEY 已從 .env 讀取')

        key_bytes = ENV_KEY.encode()
        self.fernet = Fernet(key_bytes)
    
    def encrypt_content(self, content: str):
        return self.fernet.encrypt(content.encode()).decode()
    
    def decrypt_content(self, token: str):
        try:
            return self.fernet.decrypt(token.encode()).decode()
        except Exception as e:
            logging.info(f'🔑 [解密失敗] 錯誤原因：{e}')
            return "[解密失敗]"
    

# def encrypt_content(content: str) -> str:
#     return fernet.encrypt(content.encode()).decode()

# def encrypt_content_by_key(content: str, key: bytes = KEY) -> str:
#     fernet = Fernet(key)
#     return fernet.encrypt(content.encode()).decode()

# def decrypt_content(token: str, key: bytes = KEY) -> str:
#     try:
#         return Fernet(key).decrypt(token.encode()).decode()
#     except Exception:
#         return "[解密失敗]"
