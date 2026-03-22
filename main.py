import sys, os, threading, sqlite3, hashlib, base64, re
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# محرك الربط مع نظام أندرويد Java API
try:
    from jnius import autoclass
    ANDROID_MODE = True
except ImportError:
    ANDROID_MODE = False

# ==========================================================
# الطبقة الأولى: الخزنة المشفرة (The Vault)
# ==========================================================
class JosephVault:
    def __init__(self, key="JOSEPH_FAHMY_2026"):
        self.key = hashlib.sha256(key.encode()).digest()
        self.db_path = "shadow_vault.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS intel (id INTEGER PRIMARY KEY, tag TEXT, data BLOB, ts TIMESTAMP)")

    def secure_save(self, tag, content):
        from Crypto.Cipher import AES
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher.encrypt_and_digest(content.encode())
        # تخزين البيانات بتنسيق (Nonce + Tag + Ciphertext)
        payload = base64.b64encode(cipher.nonce + auth_tag + ciphertext).decode()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO intel (tag, data, ts) VALUES (?, ?, ?)", (tag, payload, datetime.now()))

# ==========================================================
# الطبقة الثانية: محرك سحب البيانات (Intel Engine)
# ==========================================================
class IntelEngine:
    def __init__(self):
        if ANDROID_MODE:
            self.Activity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.Resolver = self.Activity.getContentResolver()
            self.Uri = autoclass('android.net.Uri')
        else:
            self.Resolver = None

    def deep_extract(self, target):
        if not self.Resolver: return "Simulated Data: No Android Environment Detected."
        
        report = f"--- REPORT FOR {target} ---\n"
        # 1. سحب الأسماء المرتبطة
        Contacts = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
        cur = self.Resolver.query(Contacts.CONTENT_URI, [Contacts.DISPLAY_NAME], f"{Contacts.NUMBER} LIKE ?", [f"%{target}%"], None)
        if cur and cur.moveToFirst():
            report += f"Identity: {cur.getString(0)}\n"
            cur.close()

        # 2. سحب آخر 5 رسائل نصية
        sms_uri = self.Uri.parse("content://sms/")
        sms_cur = self.Resolver.query(sms_uri, ["body", "type"], "address LIKE ?", [f"%{target}%"], "date DESC LIMIT 5")
        if sms_cur:
            while sms_cur.moveToNext():
                msg_type = "RECV" if sms_cur.getInt(1) == 1 else "SENT"
                report += f"[{msg_type}]: {sms_cur.getString(0)}\n"
            sms_cur.close()
            
        return report

# ==========================================================
# الطبقة الثالثة: واجهة التحكم (Command Center)
# ==========================================================
class SovereignUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.vault = JosephVault()
        self.intel = IntelEngine()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("JOSEPH FAHMY - SOVEREIGN CORE")
        self.resize(1100, 750)
        self.setStyleSheet("background: #000; color: #00FF41; font-family: 'Consolas';")
        
        layout = QVBoxLayout()
        self.target_input = QLineEdit(); self.target_input.setPlaceholderText("ENTER TARGET NUMBER")
        self.target_input.setStyleSheet("border: 1px solid #00FF41; padding: 12px; background: #0a0a0a; color: #fff;")
        
        self.log_screen = QTextEdit(); self.log_screen.setReadOnly(True)
        self.log_screen.setStyleSheet("background: #050505; border: 1px solid #333; color: #00FF41;")
        
        run_btn = QPushButton("EXECUTE EXTRACTION"); run_btn.clicked.connect(self.start_task)
        run_btn.setStyleSheet("background: #00FF41; color: #000; font-weight: bold; height: 45px;")
        
        layout.addWidget(QLabel("SYSTEM COMMANDER v10.0"))
        layout.addWidget(self.target_input)
        layout.addWidget(run_btn)
        layout.addWidget(self.log_screen)
        
        container = QWidget(); container.setLayout(layout); self.setCentralWidget(container)

    def start_task(self):
        num = self.target_input.text()
        if not num: return
        self.log_screen.append(f">>> Scanning Target: {num}")
        
        def run_thread():
            data = self.intel.deep_extract(num)
            self.vault.secure_save(f"TARGET_{num}", data)
            # تحديث الواجهة من الـ Thread
            QMetaObject.invokeMethod(self.log_screen, "append", Qt.ConnectionType.QueuedConnection, 
                                     Q_ARG(str, f">>> Extraction Finished & Vaulted.\n{data}"))
        
        threading.Thread(target=run_thread, daemon=True).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SovereignUI()
    window.show()
    sys.exit(app.exec())
