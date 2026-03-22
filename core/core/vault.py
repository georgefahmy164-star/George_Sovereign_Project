import sqlite3
import hashlib
import base64
from datetime import datetime
from Crypto.Cipher import AES

class JosephVault:
    """محرك التشفير العسكري وقاعدة البيانات المشفرة"""
    
    def __init__(self, master_key="JOSEPH_FAHMY_2026"):
        # توليد مفتاح 256-بت من كلمة المرور باستخدام SHA-256
        self.key = hashlib.sha256(master_key.encode()).digest()
        self.db_path = "shadow_vault.db"
        self._init_db()

    def _init_db(self):
        """تهيئة قاعدة البيانات بنظام WAL لسرعة الكتابة القصوى"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS intel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT,
                    payload BLOB,
                    timestamp DATETIME
                )
            """)

    def encrypt_content(self, plain_text):
        """تشفير النص باستخدام AES-GCM (Authenticated Encryption)"""
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher.encrypt_and_digest(plain_text.encode())
        
        # دمج (النونص + التاج + النص المشفر) في حزمة واحدة للقاعدة
        # Nonce (16 bytes) + Tag (16 bytes) + Ciphertext (Variable)
        combined_data = cipher.nonce + auth_tag + ciphertext
        return base64.b64encode(combined_data).decode()

    def secure_store(self, tag, content):
        """تشفير وحفظ البيانات في القاعدة بضغطة واحدة"""
        try:
            encrypted_blob = self.encrypt_content(content)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO intel (tag, payload, timestamp) VALUES (?, ?, ?)",
                    (tag, encrypted_blob, datetime.now())
                )
            return True
        except Exception as e:
            print(f"[-] Vault Error: {e}")
            return False

    def get_all_logs(self):
        """استرجاع كافة السجلات (ستظهر مشفرة في الواجهة للحماية)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT tag, timestamp FROM intel ORDER BY timestamp DESC")
            return cursor.fetchall()
