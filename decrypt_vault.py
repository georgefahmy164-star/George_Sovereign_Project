import sqlite3, hashlib, base64
from Crypto.Cipher import AES

def decrypt_data(password, encrypted_blob):
    key = hashlib.sha256(password.encode()).digest()
    raw_data = base64.b64decode(encrypted_blob)
    
    # تقسيم البيانات (Nonce: 16, Tag: 16, Ciphertext: Rest)
    nonce, tag, ciphertext = raw_data[:16], raw_data[16:32], raw_data[32:]
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# فك تشفير كافة البيانات في القاعدة
def export_report():
    conn = sqlite3.connect("shadow_vault.db")
    cursor = conn.execute("SELECT tag, data FROM intel")
    for tag, blob in cursor:
        try:
            decrypted = decrypt_data("JOSEPH_FAHMY_2026", blob)
            print(f"[{tag}] -> {decrypted}")
        except:
            print(f"[-] Failed to decrypt {tag}")

if __name__ == "__main__":
    export_report()
