import streamlit as st
import sys
import os
from datetime import datetime

# 1. حل مشكلة المسارات برمجياً (لضمان رؤية مجلد core)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.vault import JosephVault
    from core.analytics import IntelAnalyzer
except ImportError as e:
    st.error(f"❌ خطأ في استيراد الوحدات الأساسية: {e}")
    st.info("تأكد من وجود مجلد باسم core وبداخله ملف __init__.py")
    st.stop()

# 2. إعدادات الصفحة
st.set_page_config(
    page_title="JOSEPH FAHMY - SOVEREIGN v10",
    page_icon="🛡️",
    layout="wide"
)

# 3. تصميم الواجهة (Black & Gold) بأسلوب يحمي من SyntaxError
custom_css = """
<style>
    .stApp {
        background-color: #050505;
        color: #D4AF37;
    }
    .stTextInput input {
        color: #D4AF37 !important;
        background-color: #111 !important;
        border: 1px solid #D4AF37 !important;
    }
    div.stButton > button {
        background: linear-gradient(45deg, #D4AF37, #8A6D3B);
        color: black !important;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def main():
    st.title("🛡️ SOVEREIGN COMMAND CENTER")
    st.subheader(f"System Operator: {st.sidebar.text_input('Operator Name', 'Joseph Fahmy')}")
    st.write("---")

    # تهيئة المحركات
    vault = JosephVault()
    analyzer = IntelAnalyzer()

    # تقسيم الشاشة
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📡 Intelligence Input")
        target_input = st.text_input("ENTER TARGET DATA", placeholder="Phone, Email, or ID...")
        
        if st.button("EXECUTE SYSTEM SCAN"):
            if target_input:
                with st.spinner("Analyzing & Vaulting..."):
                    # تحليل البيانات
                    analysis = analyzer.analyze_content(target_input)
                    risk_level = analyzer.get_critical_score(analysis)
                    
                    # حفظ في الخزنة المشفرة
                    vault.secure_store(f"SCAN_{target_input}", f"Risk: {risk_level} | Time: {datetime.now()}")
                    
                    st.session_state['last_scan'] = {
                        'target': target_input,
                        'risk': risk_level,
                        'tags': analysis
                    }
                    st.success("Data secured in JosephVault.")
            else:
                st.warning("Please enter data to proceed.")

    with col2:
        st.markdown("### 🖥️ Live Monitor")
        if 'last_scan' in st.session_state:
            data = st.session_state['last_scan']
            st.code(f""">>> TARGET: {data['target']}
>>> RISK_LEVEL: {data['risk']}
>>> DETECTED_TAGS: {data['tags']}
>>> ENCRYPTION: AES-256 GCM
>>> STATUS: SECURELY STORED""", language="bash")
        else:
            st.info("Awaiting command input...")

    # قسم السجلات السفلي
    st.write("---")
    with st.expander("📂 SYSTEM LOGS (ENCRYPTED)"):
        logs = vault.get_all_logs()
        if logs:
            for log in logs[:10]:
                st.text(f"ID: {log[0]} | Tag: {log[1]}")
        else:
            st.write("No logs found.")

if __name__ == "__main__":
    main()
