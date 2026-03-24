# ==============================================================================
# 👑 PROJECT: JOSEPH TITAN OMNI V26 – THE SOVEREIGN (FINAL)
# 👑 ARCHITECT: JOSEPH FAHMY
# 👑 MODULES: Phone OSINT | IP Tracker | Web Recon | AI Analysis | Cyber Vault
#            | User Auth | SQLite Logs | Telegram Alerts
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
import json

# -----------------------------
# 🛡️ SECURE CONFIGURATION (Secrets)
# -----------------------------
NUM_KEY = st.secrets.get("NUMVERIFY_KEY", "")
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")

# -----------------------------
# 📡 TELEGRAM NOTIFIER (Optional)
# -----------------------------
def send_telegram(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": f"🔱 **TITAN OMNI**\n{msg}", "parse_mode": "Markdown"}
        try: requests.post(url, json=payload, timeout=5)
        except: pass

# -----------------------------
# 🏗️ DATABASE & AUTH
# -----------------------------
class TitanDB:
    def __init__(self):
        self.conn = sqlite3.connect("joseph_titan.db", check_same_thread=False)
        self.c = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, password TEXT, role TEXT, created TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, operator TEXT, target TEXT, info TEXT, time TEXT)''')
        self.conn.commit()

    def verify_user(self, u, p):
        hp = hashlib.sha256(p.encode()).hexdigest()
        self.c.execute("SELECT role FROM users WHERE username=? AND password=?", (u, hp))
        row = self.c.fetchone()
        return row[0] if row else None

    def add_user(self, u, p, role="OPERATOR"):
        hp = hashlib.sha256(p.encode()).hexdigest()
        try:
            self.c.execute("INSERT INTO users (username, password, role, created) VALUES (?,?,?,?)",
                           (u, hp, role, datetime.now().strftime("%Y-%m-%d")))
            self.conn.commit()
            return True
        except: return False

    def log(self, op, target, info=""):
        self.c.execute("INSERT INTO logs (operator, target, info, time) VALUES (?,?,?,?)",
                       (op, target, info, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

    def get_logs(self):
        return pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", self.conn)

db = TitanDB()

# -----------------------------
# 🔐 CRYPTOGRAPHY & STEGANOGRAPHY
# -----------------------------
class TitanSecure:
    @staticmethod
    def derive_key(pwd):
        h = hashlib.sha256(pwd.encode()).digest()
        return base64.urlsafe_b64encode(h)

    @staticmethod
    def encrypt(text, pwd):
        try:
            f = Fernet(TitanSecure.derive_key(pwd))
            return f.encrypt(text.encode()).decode()
        except: return "❌ Encryption Error"

    @staticmethod
    def decrypt(token, pwd):
        try:
            f = Fernet(TitanSecure.derive_key(pwd))
            return f.decrypt(token.encode()).decode()
        except: return "❌ Wrong Key or Data Corrupted"

    @staticmethod
    def hide_in_image(img_bytes, msg, out_path="secret.png"):
        try:
            temp = "temp_host.png"
            with open(temp, "wb") as f: f.write(img_bytes)
            secret = lsb.hide(temp, msg)
            secret.save(out_path)
            os.remove(temp)
            return True, out_path
        except Exception as e: return False, str(e)

    @staticmethod
    def reveal_from_image(img_path):
        try: return lsb.reveal(img_path)
        except Exception as e: return f"❌ Reveal Failed: {e}"

# -----------------------------
# 🤖 AI ENGINE (Gemini)
# -----------------------------
def gemini_analyze(prompt):
    if not GEMINI_KEY: return "⚠️ Gemini key missing."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=15)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: return "⚠️ AI engine offline."

# -----------------------------
# 📡 OSINT MODULES
# -----------------------------
class IntelCore:
    @staticmethod
    def phone_scan(phone):
        clean = phone.strip().replace(" ", "").replace("+", "")
        if clean.startswith('0'): clean = '20' + clean[1:]
        if len(clean) == 10: clean = '20' + clean
        url = f"http://apilayer.net/api/validate?access_key={NUM_KEY}&number={clean}"
        try: return requests.get(url, timeout=10).json()
        except: return {"error": "API timeout"}

    @staticmethod
    def ip_scan(ip):
        try: return requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        except: return {"error": "IP API timeout"}

    @staticmethod
    def web_recon(url):
        if not url.startswith("http"): url = "https://" + url
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            return {
                "Status": r.status_code,
                "Title": soup.title.string if soup.title else "N/A",
                "Server": r.headers.get("Server", "Hidden"),
                "Links": len(soup.find_all("a")),
                "MetaDesc": (soup.find("meta", attrs={"name":"description"}) or {}).get("content", "N/A")
            }, soup.get_text()[:1000]
        except: return {"error": "Unreachable"}, ""

# -----------------------------
# 🎨 UI: ROYAL THEME & LAYOUT
# -----------------------------
st.set_page_config(page_title="JOSEPH TITAN OMNI", layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #050505; color: #D4AF37; font-family: 'JetBrains Mono', monospace; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 4rem; text-align: center;
                  background: linear-gradient(180deg, #D4AF37, #FFF); -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 30px #D4AF37); }
    div.stButton > button { border: 2px solid #D4AF37 !important; background: transparent !important;
                            color: #D4AF37 !important; font-weight: bold; width: 100%; height: 3.5em; }
    div.stButton > button:hover { background: #D4AF37 !important; color: black !important;
                                  box-shadow: 0 0 30px #D4AF37; }
    .stTextInput > div > div > input { background-color: #111; color: #D4AF37; border: 1px solid #D4AF37; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🧠 MAIN APPLICATION
# -----------------------------
def main():
    if "auth" not in st.session_state:
        st.session_state.auth = None

    # ---- AUTHENTICATION SCREEN ----
    if not st.session_state.auth:
        st.markdown("<h1 class='main-title'>JOSEPH TITAN OMNI</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            tab1, tab2 = st.tabs(["🔐 Login", "🆕 Register"])
            with tab1:
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.button("Login"):
                    role = db.verify_user(u, p)
                    if role:
                        st.session_state.auth = {"user": u, "role": role}
                        send_telegram(f"🟢 **LOGIN**\nUser: {u}")
                        st.rerun()
                    else: st.error("Invalid credentials")
            with tab2:
                nu = st.text_input("New Username")
                np = st.text_input("New Password", type="password")
                if st.button("Register"):
                    if nu and np:
                        if db.add_user(nu, np):
                            st.success("Account created. Please login.")
                        else: st.error("Username already exists")
                    else: st.warning("Fill all fields")
        return

    # ---- MAIN DASHBOARD ----
    st.sidebar.markdown(f"### 🛡️ Operator: **{st.session_state.auth['user']}**")
    st.sidebar.markdown(f"Role: {st.session_state.auth['role']}")
    st.sidebar.divider()

    module = st.sidebar.radio("COMMAND MODULE",
        ["📱 Phone Scanner", "🌐 IP Tracker", "🔍 Web Recon", "🔐 Cyber Vault", "📊 Logs", "🚪 Logout"])

    # ---------- 1. PHONE SCANNER ----------
    if module == "📱 Phone Scanner":
        st.subheader("📱 Phone Intelligence")
        target = st.text_input("Target Number", placeholder="e.g. 01229166011")
        if st.button("EXECUTE"):
            if target:
                with st.spinner("Decoding network signals..."):
                    data = IntelCore.phone_scan(target)
                    if data.get("valid"):
                        st.success("Target synchronized ✅")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Carrier", data.get("carrier"))
                        col2.metric("Country", data.get("country_name"))
                        col3.metric("Line Type", data.get("line_type"))
                        with st.expander("Full Metadata"):
                            st.json(data)
                        # AI Analysis
                        if GEMINI_KEY:
                            prompt = f"OSINT analysis of phone number {target}: {data}"
                            st.info(gemini_analyze(prompt))
                        db.log(st.session_state.auth['user'], target, data.get("carrier", "Unknown"))
                        send_telegram(f"📞 **Phone Scan**\nUser: {st.session_state.auth['user']}\nTarget: {target}\nCarrier: {data.get('carrier')}")
                    else:
                        st.error(data.get("error", {}).get("info", "Invalid number"))
            else: st.warning("Enter target number")

    # ---------- 2. IP TRACKER ----------
    elif module == "🌐 IP Tracker":
        st.subheader("🌐 IP Geolocation")
        ip_target = st.text_input("IP Address")
        if st.button("TRACE"):
            if ip_target:
                with st.spinner("Satellite triangulation..."):
                    ip_data = IntelCore.ip_scan(ip_target)
                    if ip_data.get("status") == "success":
                        st.success(f"Node: {ip_data['city']}, {ip_data['country']}")
                        lat, lon = ip_data['lat'], ip_data['lon']
                        m = folium.Map(location=[lat, lon], zoom_start=12, tiles="CartoDB dark_matter")
                        folium.Marker([lat, lon], popup=ip_target).add_to(m)
                        st_folium(m, width="100%", height=400)
                        st.write(f"**ISP:** {ip_data.get('isp')} | **Org:** {ip_data.get('org')}")
                        db.log(st.session_state.auth['user'], ip_target, ip_data.get('isp', 'Unknown'))
                        send_telegram(f"🌍 **IP Trace**\nUser: {st.session_state.auth['user']}\nIP: {ip_target}\nLocation: {ip_data['city']}")
                    else: st.error("Node not found")
            else: st.warning("Enter IP address")

    # ---------- 3. WEB RECON ----------
    elif module == "🔍 Web Recon":
        st.subheader("🔍 Website Reconnaissance")
        url_target = st.text_input("Target URL")
        if st.button("SCAN"):
            if url_target:
                with st.spinner("Harvesting metadata..."):
                    recon, raw = IntelCore.web_recon(url_target)
                    if "error" not in recon:
                        st.json(recon)
                        if GEMINI_KEY:
                            prompt = f"Website intelligence: {recon}\nContent snippet: {raw[:500]}"
                            st.info(gemini_analyze(prompt))
                        db.log(st.session_state.auth['user'], url_target, recon.get('Title', 'Unknown'))
                        send_telegram(f"🌐 **Web Recon**\nUser: {st.session_state.auth['user']}\nTarget: {url_target}")
                    else: st.error(recon["error"])
            else: st.warning("Enter URL")

    # ---------- 4. CYBER VAULT ----------
    elif module == "🔐 Cyber Vault":
        st.subheader("🔐 Military‑Grade Cryptography")
        tab1, tab2 = st.tabs(["💬 Text Cipher", "🖼️ Image Steganography"])
        with tab1:
            msg = st.text_area("Message / Ciphertext")
            pwd = st.text_input("Secret Key", type="password")
            c1, c2 = st.columns(2)
            if c1.button("ENCRYPT"):
                if msg and pwd:
                    st.code(TitanSecure.encrypt(msg, pwd))
                else: st.warning("Message and key required")
            if c2.button("DECRYPT"):
                if msg and pwd:
                    st.info(TitanSecure.decrypt(msg, pwd))
                else: st.warning("Ciphertext and key required")
        with tab2:
            st.write("Hide a secret message in a PNG image")
            img_file = st.file_uploader("Host Image (PNG)", type=['png'])
            secret = st.text_area("Message to hide")
            if st.button("Hide & Download"):
                if img_file and secret:
                    ok, out = TitanSecure.hide_in_image(img_file.getvalue(), secret)
                    if ok:
                        with open(out, "rb") as f:
                            st.download_button("Download Secret Image", f, "secret.png")
                    else: st.error(out)
                else: st.warning("Provide image and message")
            st.divider()
            st.write("Extract hidden message from an image")
            reveal_file = st.file_uploader("Image with Hidden Message", type=['png'], key="reveal")
            if st.button("Reveal"):
                if reveal_file:
                    tmp = "temp_reveal.png"
                    with open(tmp, "wb") as f: f.write(reveal_file.getvalue())
                    msg = TitanSecure.reveal_from_image(tmp)
                    os.remove(tmp)
                    st.info(f"**Hidden message:** {msg}")
                else: st.warning("Upload image")

    # ---------- 5. LOGS ----------
    elif module == "📊 Logs":
        st.subheader("📊 Operation Logs")
        logs = db.get_logs()
        if not logs.empty:
            st.dataframe(logs, use_container_width=True)
            csv = logs.to_csv(index=False).encode('utf-8')
            st.download_button("Export CSV", csv, "titan_logs.csv")
        else: st.info("No logs yet.")

    # ---------- 6. LOGOUT ----------
    elif module == "🚪 Logout":
        send_telegram(f"🔴 **LOGOUT**\nUser: {st.session_state.auth['user']}")
        st.session_state.auth = None
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("JOSEPH TITAN OMNI V26")

if __name__ == "__main__":
    main()
