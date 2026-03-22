import streamlit as st
from core.vault import JosephVault
from core.analytics import IntelAnalyzer
from datetime import datetime

# إعدادات الواجهة الرسومية
st.set_page_config(page_title="JOSEPH FAHMY - SOVEREIGN v10", layout="wide")

# التصميم الأسود والذهبي (Premium Dark Theme)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #D4AF37; }
    .stTextInput input { border: 1px solid #D4AF37; background: #111; color: #D4AF37; }
    .stButton button { background: linear-gradient(45deg, #D4AF37, #8A6D3B); color: black; border: none; }
    </style>
    """, unsafe_allow_headers=True)

def main():
    st.title("🛡️ SOVEREIGN COMMAND CENTER")
    st.write(f"System Status: <span style='color:#00FF41'>ACTIVE</span>", unsafe_allow_headers=True)
    
    vault = JosephVault()
    analyzer = IntelAnalyzer()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Target Intelligence")
        target = st.text_input("Enter Target ID/Number")
        if st.button("RUN DEEP ANALYSIS"):
            if target:
                with st.spinner("Analyzing Patterns..."):
                    # تشفير وحفظ الطلب صامتاً
                    vault.secure_save(f"REQ_{target}", f"Analysis initiated at {datetime.now()}")
                    st.session_state['last_target'] = target
            else:
                st.warning("Please enter a target.")

    with col2:
        st.subheader("Operation Logs")
        if 'last_target' in st.session_state:
            st.code(f">>> Target: {st.session_state['last_target']}\n>>> Status: Encrypted & Vaulted\n>>> Analysis: Pattern Recognition Online")
        else:
            st.info("System Idle. Waiting for Target input.")

if __name__ == "__main__":
    main()
