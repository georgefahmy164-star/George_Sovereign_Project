import streamlit as st
import sys
import os
from datetime import datetime

# 1. حل مشكلة المسارات: إجبار بايثون على رؤية مجلد core كحزمة برمجية
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. محاولة استيراد الأدوات مع عرض رسالة خطأ ذكية إذا فشل الاستيراد
try:
    from core.vault import JosephVault
    from core.analytics import IntelAnalyzer
except (ImportError, ModuleNotFoundError) as e:
    st.error(f"❌ خطأ في النظام الأساسي: {e}")
    st.info("تأكد من أن 'core' مجلد يحتوي على ملف __init__.py وملفات البرمجة.")
    st.stop()

# 3. إعدادات الصفحة والجماليات (الأسود والذهبي)
st.set_page_config(page_title="JOSEPH FAHMY - SOVEREIGN v10", layout="wide")

# تعريف التنسيق في متغير منفصل لتجنب أخطاء SyntaxError التي ظهرت في صورك
style_code = """
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
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 15px #D4AF37;
    }
</style>
"""
st.markdown(style_code, unsafe_allow_html=True)

def main():
    st.title("🛡️ SOVEREIGN COMMAND CENTER v10")
    st.write(f"Logged as: **Joseph Fahmy** | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown("---")

    # تهيئة الكلاسات
    vault = JosephVault()
    analyzer = IntelAnalyzer()

    # تقسيم الواجهة
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📡 Intelligence Acquisition")
        target_id = st.text_input("ENTER TARGET ID", placeholder="e.g. +201XXXXXXXXX")
        
        if st.button("EXECUTE DEEP SCAN"):
            if target_id:
                with st.spinner("Analyzing and Vaulting..."):
                    # حفظ البيانات في الخزنة المشفرة
                    vault.secure_store(f"SCAN_{target_id}", f"System analysis performed at {datetime.now()}")
                    st.session_state['current_scan'] = target_id
                    st.success("Target data secured in JosephVault.")
            else:
                st.warning("Please enter a valid target ID.")

    with col2:
        st.subheader("🖥️ System Monitor")
        if 'current_scan' in st.session_state:
            st.code(f""">>> ACCESSING CORE...
>>> TARGET_LOCKED: {st.session_state['current_scan']}
>>> ENCRYPTION: AES-256 GCM
>>> VAULT_STATUS: ACTIVE
>>> LOG_STAMP: {datetime.now().isoformat()}""", language="bash")
        else:
            st.info("System Ready. Awaiting operator command...")

    # عرض السجلات المشفرة في الأسفل
    st.markdown("---")
    with st.expander("📂 VIEW ENCRYPTED SECURITY LOGS"):
        logs = vault.get_all_logs()
        if logs:
            for log in logs[:5]:
                st.markdown(f"**ID:** `{log[0]}` | **Stamp:** `{log[1]}`")
        else:
            st.write("No logs available in shadow_vault.db")

if __name__ == "__main__":
    main()
