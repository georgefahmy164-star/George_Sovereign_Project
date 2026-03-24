# ==============================================================================
# 👑 PROJECT: JOSEPH TITAN OMNI V25 - THE SOVEREIGN
# 👑 ARCHITECT: JOSEPH FAHMY (FULL-STACK AI ENGINEER)
# 👑 FEATURES: PHONE OSINT | IP TRACKER | WEB RECON | CYBER VAULT (Encryption + Stegano)
# ==============================================================================

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import sqlite3
import hashlib
import base64
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from stegano import lsb
import os

# -----------------------------
# 🛡️ CONFIGURATION (Secrets)
# -----------------------------
NUM_KEY = st.secrets.get("NUMVERIFY_KEY", "")
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")

# -----------------------------
# 🏗️ MODULE: DATABASE & AUTH
# -----------------------------
class TitanDB:
    def __init__(self):
        self.conn = sqlite3.connect("joseph_titan.db", check_same_thread=False)
        self.c = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)')
        self.c.execute('CREATE TABLE IF NOT EXISTS logs (op TEXT, target TEXT, info TEXT, time TEXT)')
        self.conn.commit()

    def verify_user(self, u, p):
        hp = hashlib.sha256(p.encode()).hexdigest()
        self.c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hp))
        return self.c.fetchone()

    def log_operation(self, op, target, info):
        self.c.execute("INSERT INTO logs (op, target, info, time) VALUES (?,?,?,?)",
                       (op, target, info, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

db = TitanDB()

# -----------------------------
# 🔐 MODULE: CRYPTOGRAPHY & STEGANOGRAPHY
# -----------------------------
class TitanSecure:
    @staticmethod
    def generate_key_from_pwd(password):
        """توليد مفتاح Fernet من كلمة مرور"""
        hasher = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(hasher)

    @staticmethod
    def encrypt_msg(text, pwd):
        """تشفير نص باستخدام كلمة مرور"""
        try:
            key = TitanSecure.generate_key_from_pwd(pwd)
            f = Fernet(key)
            return f.encrypt(text.encode()).decode()
        except Exception as e:
            return f"❌ Encryption Error: {str(e)}"

    @staticmethod
    def decrypt_msg(token, pwd):
        """فك تشفير نص باستخدام كلمة مرور"""
        try:
            key = TitanSecure.generate_key_from_pwd(pwd)
            f = Fernet(key)
            return f.decrypt(token.encode()).decode()
        except:
            return "❌ Wrong Key or Corrupted Data"

    @staticmethod
    def hide_in_image(image_bytes, message, output_path="secret.png"):
        """إخفاء رسالة داخل صورة (PNG فقط)"""
        try:
            # حفظ الصورة مؤقتاً
            temp_path = "temp_host.png"
            with open(temp_path, "wb") as f:
                f.write(image_bytes)
            # إخفاء الرسالة
            secret = lsb.hide(temp_path, message)
            secret.save(output_path)
            os.remove(temp_path)
            return True, output_path
        except Exception as e:
            return False, str(e)

    @staticmethod
    def reveal_from_image(image_path):
        """استخراج الرسالة المخفية من صورة"""
        try:
            return lsb.reveal(image_path)
        except Exception as e:
            return f"❌ Reveal Failed: {str(e)}"

# -----------------------------
# 🤖 MODULE: AI ENGINE
# -----------------------------
def gemini_analyze(prompt):
    if not GEMINI_KEY: return "⚠️ Gemini Key Missing"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    try:
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: return "⚠️ AI Engine Offline"

# -----------------------------
# 📡 MODULE: INTELLIGENCE CORES
# -----------------------------
class IntelCore:
    @staticmethod
    def scan_phone(phone):
        clean = phone.strip().replace(" ", "").replace("+", "")
        if clean.startswith('0'): clean = '20' + clean[1:]
        url = f"http://apilayer.net/api/validate?access_key={NUM_KEY}&number={clean}"
        try:
            return requests.get(url, timeout=10).json()
        except:
            return {"error": "Phone API Timeout"}

    @staticmethod
    def scan_ip(ip):
        try:
            return requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        except:
            return {"error": "IP API Timeout"}

    @staticmethod
    def web_recon(url):
        if not url.startswith('http'):
            url = 'https://' + url
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            return {
                "Title": soup.title.string if soup.title else "N/A",
                "Server": res.headers.get('Server', 'Hidden'),
                "Links": len(soup.find_all('a')),
                "Status": res.status_code
            }, soup.get_text()[:1000]
        except:
            return {"error": "Website unreachable"}, ""

# -----------------------------
# 🎨 UI: ROYAL INTERFACE (مع تحديث القائمة)
# -----------------------------
st.set_page_config(page_title="JOSEPH TITAN V25", layout="wide")
st.markdown("<h1 style='text-align:center; color:#D4AF37; font-family:Orbitron;'>🔱 JOSEPH TITAN OMNI V25</h1>", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h3 style='text-align:center;'>⚜️ Secure Authentication</h3>", unsafe_allow_html=True)
    u = st.text_input("Operator ID")
    p = st.text_input("Access Key", type="password")
    if st.button("AUTHENTICATE"):
        # يمكنك تغيير كلمة السر أو ربطها بقاعدة البيانات
        if u.lower() == "joseph" and p == "titan2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied")
else:
    # القائمة الجانبية مع إضافة Cyber Vault
    module = st.sidebar.radio("CHOOSE MISSION", 
                              ["📱 Phone Scanner", "🌐 IP Tracker", "🔍 Web Recon", "🔐 Cyber Vault", "🚪 Logout"])

    # ========================
    # 1. PHONE SCANNER
    # ========================
    if module == "📱 Phone Scanner":
        st.subheader("📱 Advanced Phone Intelligence")
        target = st.text_input("Target Number", placeholder="e.g. 01229166011")
        if st.button("EXECUTE"):
            if target:
                with st.spinner("Analyzing..."):
                    data = IntelCore.scan_phone(target)
                    if data.get("valid"):
                        st.success("Target Synchronized ✅")
                        st.json(data)
                        # تسجيل العملية
                        db.log_operation(st.session_state.get('user', 'Joseph'), target, data.get('carrier', 'Unknown'))
                        if GEMINI_KEY:
                            st.info(gemini_analyze(f"Analyze this phone data: {data}"))
                    else:
                        st.error("Target identification failed")
            else:
                st.warning("Enter a target number")

    # ========================
    # 2. IP TRACKER
    # ========================
    elif module == "🌐 IP Tracker":
        st.subheader("🌍 Global IP Node Mapping")
        ip_target = st.text_input("Target IP", placeholder="e.g. 8.8.8.8")
        if st.button("TRACE"):
            if ip_target:
                with st.spinner("Locating node..."):
                    ip_data = IntelCore.scan_ip(ip_target)
                    if ip_data.get("status") == "success":
                        st.success(f"Located: {ip_data['city']}, {ip_data['country']}")
                        lat, lon = ip_data['lat'], ip_data['lon']
                        m = folium.Map(location=[lat, lon], zoom_start=12, tiles="CartoDB dark_matter")
                        folium.Marker([lat, lon], popup=f"IP: {ip_target}").add_to(m)
                        st_folium(m, width="100%", height=400)
                        st.write(f"**ISP:** {ip_data.get('isp')} | **Org:** {ip_data.get('org')}")
                        db.log_operation(st.session_state.get('user', 'Joseph'), ip_target, ip_data.get('isp', 'Unknown'))
                    else:
                        st.error("Node not found")
            else:
                st.warning("Enter an IP address")

    # ========================
    # 3. WEB RECON
    # ========================
    elif module == "🔍 Web Recon":
        st.subheader("🔍 Website Intelligence")
        url_target = st.text_input("Target URL", placeholder="https://example.com")
        if st.button("START RECON"):
            if url_target:
                with st.spinner("Scanning..."):
                    recon, text = IntelCore.web_recon(url_target)
                    if "error" not in recon:
                        st.write("### 📋 Recon Results")
                        st.json(recon)
                        if GEMINI_KEY:
                            st.info(gemini_analyze(f"Summarize this website: {recon}\nContent snippet: {text[:500]}"))
                        db.log_operation(st.session_state.get('user', 'Joseph'), url_target, recon.get('Title', 'Unknown'))
                    else:
                        st.error(recon["error"])
            else:
                st.warning("Enter a URL")

    # ========================
    # 4. CYBER VAULT (جديد)
    # ========================
    elif module == "🔐 Cyber Vault":
        st.subheader("🔐 Military-Grade Encryption & Steganography")
        tab1, tab2 = st.tabs(["💬 Text Cipher", "🖼️ Image Steganography"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                msg_input = st.text_area("Enter Message or Ciphertext", height=150)
                key_input = st.text_input("Secret Key", type="password")
                if st.button("ENCRYPT", key="enc"):
                    if msg_input and key_input:
                        encrypted = TitanSecure.encrypt_msg(msg_input, key_input)
                        st.code(encrypted)
                    else:
                        st.warning("Message and Key required")
                if st.button("DECRYPT", key="dec"):
                    if msg_input and key_input:
                        decrypted = TitanSecure.decrypt_msg(msg_input, key_input)
                        st.info(decrypted)
                    else:
                        st.warning("Ciphertext and Key required")
            with col2:
                st.markdown("**📌 Example**")
                st.code("""
# Encrypt:
"secret message" + key -> token
# Decrypt:
token + same key -> original
                """)

        with tab2:
            st.write("📸 Hide a secret message inside a PNG image")
            uploaded_file = st.file_uploader("Upload Host Image (PNG only)", type=['png'])
            secret_msg = st.text_area("Message to Hide", placeholder="Your confidential text...")
            
            if st.button("🕵️ Hide & Download"):
                if uploaded_file and secret_msg:
                    with st.spinner("Embedding secret..."):
                        img_bytes = uploaded_file.getvalue()
                        success, result = TitanSecure.hide_in_image(img_bytes, secret_msg, "secret_output.png")
                        if success:
                            st.success("Message hidden successfully!")
                            with open("secret_output.png", "rb") as f:
                                st.download_button("Download Secret Image", f, "secret.png")
                        else:
                            st.error(f"Error: {result}")
                else:
                    st.warning("Please provide an image and a message.")
            
            st.divider()
            st.write("🔍 Extract hidden message from an image")
            reveal_file = st.file_uploader("Upload Image with Hidden Message", type=['png'], key="reveal")
            if st.button("Reveal Message"):
                if reveal_file:
                    with st.spinner("Extracting..."):
                        temp_path = "temp_reveal.png"
                        with open(temp_path, "wb") as f:
                            f.write(reveal_file.getvalue())
                        message = TitanSecure.reveal_from_image(temp_path)
                        os.remove(temp_path)
                        st.info(f"**Hidden Message:** {message}")
                else:
                    st.warning("Upload an image")

    # ========================
    # 5. LOGOUT
    # ========================
    elif module == "🚪 Logout":
        st.session_state.auth = False
        st.rerun()

    # شريط معلومات في الـ sidebar
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Operator:** Joseph Fahmy")
    st.sidebar.write(f"**Session:** Active")
    st.sidebar.caption("Powered by Joseph Titan")
