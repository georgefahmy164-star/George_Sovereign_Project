import streamlit as st
from core.vault import JosephVault
from core.analytics import IntelAnalyzer
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="JOSEPH FAHMY SOVEREIGN", layout="wide")

# 2. تعريف التصميم في متغير مستقل لتجنب أخطاء الـ Syntax
custom_style = """
<style>
    .stApp { background-color: #050505; color: #D4AF37; }
    .stTextInput input { 
        color: #D4AF37 !important; 
        background-color: #111 !important; 
        border: 2px solid #D4AF37 !important; 
    }
    div.stButton > button {
        background: linear-gradient(45deg, #D4AF37, #F9E27D);
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }
</style>
"""
st.markdown(custom_style, unsafe_allow_headers=True)

# 3. تشغيل النظام
def run_system():
    st.title("🛡️ SOVEREIGN COMMAND CENTER v10")
    st.markdown("---")

    # تهيئة الموديلات من مجلد core
    try:
        vault = JosephVault()
        analyzer = IntelAnalyzer()
    except Exception as e:
        st.error(f"Core System Failure: {e}")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📡 Acquisition")
        target = st.text_input("ENTER TARGET ID", placeholder="e.g. +2010...")
        if st.button("EXECUTE SCAN"):
            if target:
                vault.secure_store(f"SCAN_{target}", f"Logged at {datetime.now()}")
                st.session_state['active_target'] = target
                st.success("Target Vaulted.")
            else:
                st.warning("Please enter an ID.")

    with col2:
        st.subheader("🖥️ Monitor")
        if 'active_target' in st.session_state:
            st.code(f">>> TARGET: {st.session_state['active_target']}\n>>> STATUS: ENCRYPTED\n>>> VAULT: ACTIVE")
        else:
            st.info("System Ready...")

    # عرض السجلات في الأسفل
    st.markdown("---")
    with st.expander("VIEW SECURITY LOGS"):
        logs = vault.get_all_logs()
        for log in logs[:5]:
            st.text(f"[{log[1]}] {log[0]}")

if __name__ == "__main__":
    run_system()
