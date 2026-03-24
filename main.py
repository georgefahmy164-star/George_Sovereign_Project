# ==============================================================================
# 👑 PROJECT: GEORGE TITAN - THE SUPREME ARCHITECT (V12.1 FULL)
# 👑 ARCHITECT: GEORGE FAHMY (ELITE FULL-STACK OPERATOR)
# 👑 FEATURES: ALL-IN-ONE (SECURITY, AI, NOTIFICATIONS, DATABASE, ADMIN)
# ==============================================================================

import streamlit as st
import sqlite3
import requests
import hashlib
import pandas as pd
from datetime import datetime

# -----------------------------
# ⚙️ SECRETS & API CONFIG
# -----------------------------
# يتم سحب البيانات من ملف secrets.toml في Streamlit
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")
BACKEND_URL = "https://your-backend-url.onrender.com/analyze" # رابط الـ API الخاص بك

# -----------------------------
# 📡 MODULE: TELEGRAM NOTIFIER
# -----------------------------
class TitanNotifier:
    @staticmethod
    def send_alert(msg):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🔱 **TITAN SYSTEM ALERT**\n\n{msg}",
            "parse_mode": "Markdown"
        }
        try: requests.post(url, json=payload, timeout=5)
        except: pass

# -----------------------------
# 🏗️ MODULE: DATABASE MANAGER
# -----------------------------
class TitanDB:
    def __init__(self):
        self.conn = sqlite3.connect("titan_supreme.db", check_same_thread=False)
        self.c = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT, status TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS logs 
            (operator TEXT, target TEXT, carrier TEXT, time TEXT)''')
        self.conn.commit()

db = TitanDB()

# -----------------------------
# 🧠 MODULE: AI STRATEGY CORE
# -----------------------------
def get_ai_insight(data):
    if not OPENAI_KEY: return "⚠️ OpenAI Key missing."
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a Senior Cyber Intel Analyst for GEORGE TITAN system."},
            {"role": "user", "content": f"Analyze this packet and provide strategic insights: {data}"}
        ]
    }
    try:
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
        return res.json()["choices"][0]["message"]["content"]
    except: return "⚠️ AI Engine temporarily bypassed."

# -----------------------------
# 🎨 UI: THE NEON EMPIRE STYLE
# -----------------------------
st.set_page_config(page_title="GEORGE TITAN V12", layout="wide", page_icon="🔱")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #020202; color: #D4AF37; font-family: 'JetBrains Mono', monospace; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 5rem; text-align: center; 
                  background: linear-gradient(180deg, #D4AF37, #FFFFFF); -webkit-background-clip: text; 
                  -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px #D4AF37); margin: 0; }
    .stSidebar { border-right: 1px solid #D4AF37; background: #000 !important; }
    div.stButton > button { border: 1px solid #D4AF37 !important; background: transparent !important; color: #D4AF37 !important; 
                            font-weight: bold; width: 100%; transition: 0.4s; height: 3em; }
    div.stButton > button:hover { background: #D4AF37 !important; color: black !important; box-shadow: 0 0 50px #D4AF37; }
    .report-card { border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; background: rgba(212, 175, 55, 0.05); }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🚀 MAIN CONTROLLER
# -----------------------------
def main():
    if "auth" not in st.session_state: st.session_state.auth = None

    # --- PHASE 1: AUTHENTICATION ---
    if not st.session_state.auth:
        st.markdown("<h1 class='main-title'>TITAN SUPREME</h1>", unsafe_allow_html=True)
        st.write("<p style='text-align:center;'>COMMUNITY EDITION | UNLOCKED</p>", unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["🔐 SECURE ACCESS", "🆔 IDENTITY INITIALIZATION"])
        
        with tab_log:
            u = st.text_input("Operator ID")
            p = st.text_input("Access Code", type="password")
            if st.button("AUTHENTICATE"):
                hp = hashlib.sha256(p.encode()).hexdigest()
                db.c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hp))
                user = db.c.fetchone()
                if user:
                    if user[4] == "BANNED": st.error("ACCESS REVOKED: ACCOUNT SUSPENDED")
                    else:
                        st.session_state.auth = {"user": user[1], "role": user[3]}
                        TitanNotifier.send_alert(f"🟢 **LOGIN SUCCESS**\nOperator: {u}")
                        st.rerun()
                else: st.error("INVALID IDENTITY")

        with tab_reg:
            nu = st.text_input("New ID")
            np = st.text_input("New Code", type="password")
            if st.button("LOCK IDENTITY"):
                try:
                    hp = hashlib.sha256(np.encode()).hexdigest()
                    role = "ADMIN" if nu.lower() == "george" else "OPERATOR"
                    db.c.execute("INSERT INTO users (username, password, role, status) VALUES (?,?,?,?)", (nu, hp, role, "ACTIVE"))
                    db.conn.commit()
                    st.success("Identity Synchronized. You can now login.")
                    TitanNotifier.send_alert(f"🆕 **NEW REGISTRATION**\nUser: {nu} | Role: {role}")
                except: st.error("ID Already Exists.")

    # --- PHASE 2: OPERATION ---
    else:
        st.sidebar.markdown(f"### 🛡️ ACTIVE: {st.session_state.auth['user']}")
        st.sidebar.markdown(f"**ROLE:** {st.session_state.auth['role']}")
        nav = st.sidebar.radio("SYSTEM MENU", ["🎯 SCANNER", "📊 VAULT", "👑 ADMIN CORE", "🚪 TERMINATE"])

        if nav == "🎯 SCANNER":
            st.markdown("<h2 style='text-align:center;'>INTELLIGENCE SCANNER</h2>", unsafe_allow_html=True)
            target = st.text_input("ENTER TARGET IDENTIFIER (Phone)", placeholder="e.g. 201xxxxxxxxx")
            
            if st.button("EXECUTE OMNI-SCAN"):
                if target:
                    with st.spinner("Bypassing Network Filters..."):
                        try:
                            # استدعاء الـ API الخاص بك
                            res = requests.post(BACKEND_URL, json={"phone": target}, timeout=15)
                            data = res.json()
                            
                            if data.get("valid"):
                                st.markdown("<div class='report-card'>", unsafe_allow_html=True)
                                st.success("✅ TARGET COMPROMISED")
                                
                                # عرض البيانات
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.write(f"📡 **Carrier:** {data.get('carrier')}")
                                    st.write(f"🌍 **Country:** {data.get('country', {}).get('name')}")
                                    st.write(f"📱 **Type:** {data.get('type')}")
                                
                                with col_b:
                                    st.subheader("🤖 AI Strategic Insights")
                                    st.info(get_ai_insight(data))
                                
                                st.markdown("</div>", unsafe_allow_html=True)

                                # التسجيل في القاعدة والإشعارات
                                db.c.execute("INSERT INTO logs VALUES (?,?,?,?)", 
                                             (st.session_state.auth['user'], target, data.get('carrier'), str(datetime.now())))
                                db.conn.commit()
                                TitanNotifier.send_alert(f"🎯 **SCAN SUCCESS**\nBy: {st.session_state.auth['user']}\nTarget: {target}")
                            else: st.error("Target Node Invalid.")
                        except: st.error("CRITICAL: Backend offline.")
                else: st.warning("Target identifier required.")

        elif nav == "📊 VAULT":
            st.header("📂 Operation Archives")
            logs_df = pd.read_sql_query("SELECT * FROM logs", db.conn)
            st.dataframe(logs_df.sort_index(ascending=False), use_container_width=True)

        elif nav == "👑 ADMIN CORE":
            if st.session_state.auth['role'] == "ADMIN":
                st.header("Admin Level Control")
                u_list = pd.read_sql_query("SELECT id, username, role, status FROM users", db.conn)
                st.table(u_list)
                
                target_user = st.selectbox("Select User to Modify", u_list['username'])
                c1, c2 = st.columns(2)
                if c1.button("🚫 BAN USER"):
                    db.c.execute("UPDATE users SET status='BANNED' WHERE username=?", (target_user,))
                    db.conn.commit()
                    st.warning(f"User {target_user} Suspended.")
                if c2.button("✅ ACTIVATE USER"):
                    db.c.execute("UPDATE users SET status='ACTIVE' WHERE username=?", (target_user,))
                    db.conn.commit()
                    st.success(f"User {target_user} Reactivated.")
            else: st.error("SECURITY ALERT: ACCESS DENIED.")

        elif nav == "🚪 TERMINATE":
            TitanNotifier.send_alert(f"🔴 **TERMINATED**\nOperator: {st.session_state.user_auth['user']}")
            st.session_state.auth = None
            st.rerun()

if __name__ == "__main__":
    main()
