import streamlit as st
from core.vault import JosephVault
from core.analytics import IntelAnalyzer
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="JOSEPH FAHMY - SOVEREIGN", layout="wide")

# تصحيح الـ CSS (الخطأ كان هنا)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #D4AF37; }
    .stTextInput input { border: 1px solid #D4AF37 !important; background-color: #111 !important; color: #D4AF37 !important; }
    .stButton button { background: linear-gradient(45deg, #D4AF37, #8A6D3B); color: black !important; border: none; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_headers=True)

def main():
    st.title("🛡️ SOVEREIGN COMMAND CENTER v10")
    st.write(f"System Status: <span style='color:#00FF41'>ONLINE</span>", unsafe_allow_headers=True)
    
    # تهيئة المحركات من مجلد core
    try:
        vault = JosephVault()
        analyzer = IntelAnalyzer()
    except Exception as e:
        st.error(f"Error initializing core modules: {e}")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Target Intelligence")
        target = st.text_input("Enter Target ID/Number", key="target_input")
        if st.button("EXECUTE ANALYSIS"):
            if target:
                with st.spinner("Processing..."):
                    # حفظ الطلب في الخزنة
                    vault.secure_store(f"WEB_REQ_{target}", f"Request at {datetime.now()}")
                    st.session_state['active_target'] = target
            else:
                st.warning("Please provide a Target ID.")

    with col2:
        st.subheader("Operation Terminal")
        if 'active_target' in st.session_state:
            t = st.session_state['active_target']
            st.code(f">>> ACCESSING CORE...\n>>> TARGET: {t}\n>>> ENCRYPTION: AES-256 GCM\n>>> STATUS: DATA VAULTED")
            
            # عرض السجلات الأخيرة من الخزنة
            st.write("---")
            st.write("Recent Activity Log:")
            logs = vault.get_all_logs()
            for log in logs[:5]: # عرض آخر 5 سجلات
                st.text(f"[{log[1]}] {log[0]}")
        else:
            st.info("Waiting for Command Input...")

if __name__ == "__main__":
    main()
