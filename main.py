import streamlit as st
from core.vault import JosephVault
from core.analytics import IntelAnalyzer
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="JOSEPH FAHMY SOVEREIGN", layout="wide")

# 2. الواجهة الرسومية الملكية (Black & Gold)
st.markdown("""
    <style>
    /* الخلفية العامة */
    .stApp {
        background-color: #050505;
        color: #D4AF37;
    }
    /* تخصيص صندوق الإدخال */
    .stTextInput input {
        color: #D4AF37 !important;
        background-color: #111 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace;
    }
    /* تخصيص الزر الذهبي المتوهج */
    div.stButton > button {
        background: linear-gradient(45deg, #D4AF37, #F9E27D);
        color: black !important;
        border: none;
        padding: 15px 30px;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.7);
        transform: scale(1.02);
    }
    /* النصوص الجانبية */
    h1, h2, h3 {
        color: #D4AF37 !important;
        text-shadow: 2px 2px 4px #000;
    }
    </style>
    """, unsafe_allow_headers=True)

# 3. تهيئة المحركات
try:
    vault = JosephVault()
    analyzer = IntelAnalyzer()
except Exception as e:
    st.error(f"Module Connection Failed: {e}")
    st.stop()

# 4. بناء هيكل الصفحة
st.title("🛡️ SOVEREIGN COMMAND CENTER v10")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📡 Target Acquisition")
    target = st.text_input("ENTER TARGET ID / NUMBER", placeholder="e.g. +201XXXXXXXXX")
    
    if st.button("EXECUTE DEEP ANALYSIS"):
        if target:
            with st.spinner("Analyzing data patterns..."):
                # تشفير وحفظ في الخزنة
                vault.secure_store(f"WEB_SCAN_{target}", f"Deep scan initiated at {datetime.now()}")
                st.session_state['last_target'] = target
                st.success(f"Target {target} Locked & Vaulted.")
        else:
            st.warning("Input required for execution.")

with col2:
    st.subheader("🖥️ System Status")
    if 'last_target' in st.session_state:
        target_id = st.session_state['last_target']
        st.code(f"""
>>> ACCESSING ENCRYPTED CORE...
>>> TARGET_ID: {target_id}
>>> ENCRYPTION: AES-256 GCM
>>> VAULT_STATUS: SECURE
>>> LOCATION: STREAMLIT_CLOUD_NODE
        """, language="bash")
    else:
        st.info("System Ready. Awaiting Target Command...")

# 5. لوحة السجلات السفلية
st.markdown("---")
with st.expander("📂 ACCESS SECURITY LOGS"):
    logs = vault.get_all_logs()
    if logs:
        for log in logs[:10]:
            st.markdown(f"**[`{log[1]}`]** - `{log[0]}`")
    else:
        st.write("No logs found in shadow_vault.db")

st.sidebar.markdown("### 👑 Developer: Joseph Fahmy")
st.sidebar.write("Sovereign AI Project v10.0")
