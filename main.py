import streamlit as st
from core.vault import JosephVault
from core.analytics import IntelAnalyzer
from datetime import datetime

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="JOSEPH FAHMY SOVEREIGN", layout="centered")

# عنوان التطبيق
st.title("🛡️ SOVEREIGN COMMAND v10")

# تهيئة المحركات
try:
    vault = JosephVault()
    analyzer = IntelAnalyzer()
except Exception as e:
    st.error(f"Core Module Error: {e}")
    st.stop()

# واجهة المدخلات
target = st.text_input("ENTER TARGET ID")

if st.button("RUN ANALYSIS"):
    if target:
        # تنفيذ الحفظ في الخزنة
        vault.secure_store(f"WEB_SCAN_{target}", f"Request logged at {datetime.now()}")
        
        st.success(f"Analysis for {target} is being processed.")
        st.code(f">>> Target Locked: {target}\n>>> Status: Data Encrypted in shadow_vault.db")
    else:
        st.warning("Please input a valid target.")

# عرض السجلات (للتأكد من عمل الخزنة)
if st.checkbox("Show System Logs"):
    logs = vault.get_all_logs()
    for log in logs[:5]:
        st.text(f"[{log[1]}] {log[0]}")
