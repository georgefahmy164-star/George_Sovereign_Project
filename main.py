# ==============================================================================
# 👑 PROJECT: GEORGE TITAN - THE FORTRESS (V13)
# 👑 ARCHITECT: GEORGE FAHMY (PROFESSIONAL ARCHITECT)
# 👑 SECURITY STATUS: MAXIMUM | DATA TYPE: OSINT (LEGAL)
# ==============================================================================

import streamlit as st
import sqlite3
import requests
import hashlib
import pandas as pd
from datetime import datetime

# -----------------------------
# 🛡️ SECURITY & CONFIG (SAFE MODE)
# -----------------------------
# استدعاء المفاتيح من Secrets وليس كتابتها يدوياً لحماية حسابك
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
NUMVERIFY_KEY = st.secrets.get("NUMVERIFY_KEY", "") # مفتاح الـ API الخاص بالاتصالات
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")

# -----------------------------
# 📡 MODULE: SYSTEM MONITOR (TELEGRAM)
# -----------------------------
def send_telegram_alert(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": f"🔱 **TITAN MONITOR**\n{msg}", "parse_mode": "Markdown"}
        try: requests.post(url, json=payload, timeout=5)
        except: pass

# -----------------------------
# 🏗️ MODULE: DATA VAULT (SQLITE)
# -----------------------------
class TitanDB:
    def __init__(self):
        self.conn = sqlite3.connect("titan_fortress.db", check_same_thread=False)
        self.c = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS logs (op TEXT, target TEXT, time TEXT)''')
        self.conn.commit()

db = TitanDB()

# -----------------------------
# 🧠 MODULE: AI ANALYSIS
# -----------------------------
def get_ai_analysis(data):
    if not OPENAI_KEY: return "AI Engine not configured."
    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a Professional OSINT Analyst."},
            {"role": "user", "content": f"Analyze this telecom metadata: {data}"}
        ]
    }
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
        return r.json()["choices"][0]["message"]["content"]
    except: return "AI temporarily offline."

# -----------------------------
# 🎨 UI: IMPERIAL NEON DESIGN
# -----------------------------
st.set_page_config(page_title="GEORGE TITAN V13", layout="wide", page_icon="🔱")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&display=swap');
    .stApp { background-color: #050505; color: #D4AF37; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 4rem; text-align: center; 
                  background: linear-gradient(180deg, #D4AF37, #FFF); -webkit-background-clip: text; 
                  -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 20px #D4AF37); }
    div.stButton > button { border: 2px solid #D4AF37 !important; background: black !important; color: #D4AF37 !important; font-weight: bold; }
    div.stButton > button:hover { background: #D4AF37 !important; color: black !important; box-shadow: 0 0 30px #D4AF37; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🚀 CORE ENGINE
# -----------------------------
def main():
    if "session_user" not in st.session_state: st.session_state.session_user = None

    if not st.session_state.session_user:
        st.markdown("<h1 class='main-title'>TITAN FORTRESS</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            u = st.text_input("Operator ID")
            p = st.text_input("Access Key", type="password")
            if st.button("AUTHENTICATE"):
                hp = hashlib.sha256(p.encode()).hexdigest()
                db.c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hp))
                user = db.c.fetchone()
                if user:
                    st.session_state.session_user = {"name": u, "role": user[3]}
                    send_telegram_alert(f"🟢 **LOGIN**\nUser: {u}")
                    st.rerun()
                else: st.error("Access Denied.")

        with col2:
            st.write("### Identity Initialization")
            nu = st.text_input("New ID")
            np = st.text_input("New Key", type="password")
            if st.button("CREATE IDENTITY"):
                try:
                    hp = hashlib.sha256(np.encode()).hexdigest()
                    role = "ADMIN" if nu.lower() == "george" else "OPERATOR"
                    db.c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (nu, hp, role))
                    db.conn.commit()
                    st.success("Identity Created.")
                    send_telegram_alert(f"🆕 **NEW USER**\nID: {nu}")
                except: st.error("ID Exists.")

    else:
        st.sidebar.title(f"🛡️ {st.session_state.session_user['name']}")
        menu = st.sidebar.radio("COMMANDS", ["🎯 SCANNER", "📂 VAULT", "🚪 TERMINATE"])

        if menu == "🎯 SCANNER":
            st.header("Intelligence Gathering (OSINT)")
            target = st.text_input("Target Number (e.g. 201xxxxxxxxx)")
            
            if st.button("EXECUTE ANALYSIS"):
                if target:
                    with st.spinner("Extracting Metadata..."):
                        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_KEY}&number={target}"
                        try:
                            res = requests.get(url, timeout=10)
                            data = res.json()
                            if data.get("valid"):
                                st.success("Target Synchronized ✅")
                                c1, c2 = st.columns(2)
                                c1.json(data)
                                with c2:
                                    st.subheader("🤖 AI Strategic Insights")
                                    st.info(get_ai_analysis(data))
                                
                                db.c.execute("INSERT INTO logs VALUES (?,?,?)", (st.session_state.session_user['name'], target, str(datetime.now())))
                                db.conn.commit()
                                send_telegram_alert(f"🎯 **SCAN SUCCESS**\nTarget: {target}")
                            else: st.error("Target identification failed.")
                        except: st.error("Backend Error.")

        elif menu == "📂 VAULT":
            st.header("Operation Archives")
            df = pd.read_sql_query("SELECT * FROM logs", db.conn)
            st.table(df)

        elif menu == "🚪 TERMINATE":
            send_telegram_alert(f"🔴 **LOGOUT**\nUser: {st.session_state.session_user['name']}")
            st.session_state.session_user = None
            st.rerun()

if __name__ == "__main__":
    main()
