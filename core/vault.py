import sqlite3, hashlib, base64
from Crypto.Cipher import AES
from datetime import datetime

class JosephVault:
    def __init__(self, master_key="JOSEPH_FAHMY_2026"):
        self.key = hashlib.sha256(master_key.encode()).digest()
        self.db_path = "shadow_vault.db"

    def secure_save(self, tag, content):
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher.encrypt_and_digest(content.encode())
        # تخزين (النونص + التاج + المشفر)
        payload = base64.b64encode(cipher.nonce + auth_tag + ciphertext).decode()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS intel (tag TEXT, data BLOB, ts TIMESTAMP)")
            conn.execute("INSERT INTO intel (tag, data, ts) VALUES (?, ?, ?)", (tag, payload, datetime.now()))
