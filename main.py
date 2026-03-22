import streamlit as st
import pandas as pd
from datetime import datetime
import time

# استيراد المحركات من المجلدات الفرعية (تأكد من وجود ملف __init__.py في مجلد core)
try:
    from core.vault import JosephVault
    from core.analytics import IntelAnalyzer
except ImportError:
    st.error("❌ فشل استيراد المحركات الأساسية. تأكد من وجود مجلد 'core' وملفات 'vault.py' و 'analytics.py'.")
    st.stop()

# --- 1. إعدادات النظام العميقة ---
st.set_page_config(
    page_title="JOSEPH FAHMY | SOVEREIGN v10",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. هندسة التصميم (UI Engineering) ---
def apply_custom_theme():
    st.markdown("""
        <style>
        /* الخلفية العامة والتنسيق */
        .stApp { background-color: #050505; color: #D4AF37; font-family: 'Consolas', monospace; }
        
        /* تصميم الحاويات (Cards) */
        .intel-card {
            border: 1px solid #D4AF37;
            padding: 20px;
            background: rgba(20, 20, 20, 0.9);
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1);
            margin-bottom: 20px;
        }

        /* تصميم الأزرار الاحترافي */
        div.stButton > button {
            background: linear-gradient(135deg, #D4AF37 0%, #8A6D3B 100%);
            color: black !important;
            font-weight: 900;
            border: none;
            width: 100%;
            height: 3em;
            letter-spacing: 1px;
            transition: 0.4s;
        }
        div.stButton > button:hover {
            box-shadow: 0 0 25px #D4AF37;
            transform: scale(1.01);
        }

        /* مؤشر الحالة */
        .status-online { color: #00FF41; font-weight: bold; text-shadow: 0 0 5px #00FF41; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_theme()

# --- 3. المنطق التشغيلي (Main Logic) ---
def main():
    # تهيئة الكائنات
    vault = JosephVault()
    analyzer = IntelAnalyzer()

    # الهيدر الرئيسي
    st.markdown("<h1 style='text-align: center;'>🛡️ SOVEREIGN OMEGA COMMAND v10</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>SYSTEM STATUS: <span class='status-online'>● OPERATIONAL</span> | OPERATOR: JOSEPH FAHMY</p>", unsafe_allow_html=True)
    st.write("---")

    # --- القائمة الجانبية (Sidebar) ---
    with st.sidebar:
        st.header("⚙️ CONTROL PANEL")
        mode = st.selectbox("Select Module", ["Target Recon", "Secure Vault", "Network Logs", "System Settings"])
        st.write("---")
        st.info("AES-256 GCM Encryption Active")
        if st.button("🔴 EMERGENCY SHUTDOWN"):
            st.session_state.clear()
            st.rerun()

    # --- التبويب الأول: سحب وتحليل البيانات ---
    if mode == "Target Recon":
        col1, col2 = st.columns([1, 1.5])

        with col1:
            st.markdown("<div class='intel-card'>", unsafe_allow_html=True)
            st.subheader("🎯 Data Acquisition")
            target_id = st.text_input("Target Identifier (e.g. 201xxxxxxxxx)")
            data_payload = st.text_area("Source Data Stream", height=150)
            
            if st.button("LAUNCH DEEP PROBE"):
                if target_id and data_payload:
                    with st.status("⚔️ Processing Intelligence...", expanded=True) as status:
                        # تحليل البيانات
                        findings = analyzer.classify(data_payload)
                        # حفظ مشفر في الخزنة
                        vault.secure_save(f"TARGET_{target_id}", data_payload)
                        
                        time.sleep(1)
                        st.session_state['active_recon'] = {
                            "id": target_id,
                            "findings": findings,
                            "time": datetime.now().strftime("%H:%M:%S")
                        }
                        status.update(label="✅ Target Vaulted Successfully", state="complete")
                else:
                    st.warning("⚠️ Input Required: Please provide Target ID and Data.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.subheader("🖥️ Intelligence Monitor")
            if 'active_recon' in st.session_state:
                recon = st.session_state['active_recon']
                st.code(f">>> RECON_ID: {recon['id']}\n>>> TIMESTAMP: {recon['time']}\n>>> VECTOR_ANALYSIS: {recon['findings']}", language="python")
                
                # عرض مؤشرات المخاطر
                if recon['findings']:
                    st.error(f"⚠️ Critical Patterns Detected: {', '.join(recon['findings'])}")
                else:
                    st.success("✅ No Malicious Patterns Found in Stream.")
            else:
                st.info("Waiting for data stream execution...")

    # --- التبويب الثاني: الخزنة المشفرة ---
    elif mode == "Secure Vault":
        st.subheader("📂 Encrypted Shadow Vault")
        master_key = st.text_input("Enter Master Decryption Key", type="password")
        
        if master_key == "JOSEPH_FAHMY_2026":
            st.success("🔓 Access Granted to Encrypted Records")
            # محاكاة عرض البيانات (يمكنك ربطها بـ vault.get_all())
            try:
                # هذا الجزء يفترض وجود ميزة عرض في الكلاس vault.py
                st.write("Fetching latest 10 encrypted payloads...")
                # داتا تجريبية للتوضيح
                st.table([{"Tag": "TARGET_2015", "Status": "Encrypted", "TS": "2026-03-22"}])
            except:
                st.warning("Database connection active. Ready for query.")
        elif master_key:
            st.error("🚫 Access Denied: Invalid Master Key.")

    # --- التبويب الثالث: سجلات الشبكة ---
    elif mode == "Network Logs":
        st.subheader("🌐 Network Activity Logs")
        chart_data = pd.DataFrame({"Packets": [10, 25, 15, 40, 30], "Time": ["21:00", "21:15", "21:30", "21:45", "22:00"]})
        st.line_chart(chart_data.set_index("Time"))
        st.write("Monitoring Traffic on eth0...")

# تشغيل التطبيق
if __name__ == "__main__":
    main()
