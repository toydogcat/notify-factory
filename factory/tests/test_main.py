import pytest
from secretary.encryptor import encrypt_content, decrypt_content

def test_encryption_decryption():
    original = "測試訊息"
    encrypted = encrypt_content(original)
    decrypted = decrypt_content(encrypted)
    assert decrypted == original

def test_decryption_failure():
    assert decrypt_content("invalidtoken") == "[解密失敗]"
