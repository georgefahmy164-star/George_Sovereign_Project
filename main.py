import streamlit as st
from core.vault import JosephVault
from core.analytics import IntelAnalyzer
import time
from datetime import datetime
import re

# 1. إعدادات الواجهة الملكية (Black & Gold)
st.set_page_config(page_title="JOSEPH FAHMY - SOVEREIGN", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* الخلفية العامة */
    .stApp { background-color: #050505; color: #D4AF37; }
    
    /* تخصيص صندوق الإدخال */
    .stTextInput input {
        color: #D4AF37 !important;
        background-color: #111 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    
    /* تخصيص الزر الذهبي المتوهج */
    div.stButton > button {
        background: linear-gradient(45deg, #D4AF37, #8A6D3B);
        color: black !important;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.6);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_headers=True)

# 2. منطقة المنطق البرمجي (الـ 800 سطر الخاصة بك)
# قمت بتحويل الكود الخاص بك من PyQt6 إلى دوال بايثون نقية
class JosephLogic:
    def __init__(self):
        # مصفوفة بيانات افتراضية محاكية للبحث (استبدلها بقاعدة بياناتك الحقيقية)
        self.simulation_db = {
            "0102030405": {"name": "أحمد علي", "job": "مهندس", "notes": "عاجل جداً"},
            "0150607080": {"name": "ليلى محمود", "job": "طبيبة", "notes": "رمز تفعيل بنكي"}
        }

    def clean_number(self, number):
        """تنظيف الرقم من الرموز والمسافات"""
        return re.sub(r'[^\d+]', '', number)

    def extract_pattern(self, raw_data, pattern_name):
        """استخراج أنماط محددة (أرقام، بريد إلكتروني، إلخ)"""
        patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'codes': r'\b( رمز | تفعيل | code ):?\s*(\d{4,6})\b'
        }
        if pattern_name in patterns:
            return re.findall(patterns[pattern_name], raw_data)
        return []

    def run_deep_scan(self, target):
        """تشغيل محرك البحث العميق"""
        cleaned_target = self.clean_number(target)
        results = f">>> Initiating Deep Scan for: {cleaned_target}\n"
        results += ">>> Core modules online...\n"
        results += f">>> Log: Joseph Vault initiated at {datetime.now().isoformat()}\n\n"
        
        # محاكاة زمن البحث
        time.sleep(1.5)
        
        # البحث في البيانات الافتراضية
        simulated_match = self.simulation_db.get(cleaned_target)
        if simulated_match:
            results += "[-] TARGET ACQUIRED IN SHADOW VAULT\n"
            results += f"[-] Associated Name: {simulated_match['name']}\n"
            results += f"[-] Associated Job: {simulated_match['job']}\n"
            results += f"[-] Primary Classification: Critical Data Found\n\n"
            results += "[-] Initiating Intel Extraction for Pattern recognition...\n"
            results += f"[-] Intelligence found: {simulated_match['notes']}\n"
            
            # محاكاة الاستخراج
            time.sleep(1)
            results += "[-] Codes Extracted: Yes\n"
            results += "[-] Location Pin: Locked\n"
        else:
            results += "[-] TARGET NOT FOUND IN PRIMARY VAULT.\n"
            results += "[-] Initiating secondary passive scanning for pattern recognition...\n"
            results += "[-] General info found only.\n"
            
        results += "\n>>> End of Scan Report."
        return results

# 3. الواجهة الرئيسية
def main():
    st.title("🛡️ SOVEREIGN COMMAND CENTER v10")
    st.markdown("---")
    
    # تهيئة المنطق والخزنة
    logic = JosephLogic()
    vault = JosephVault()
    analyzer = IntelAnalyzer()

    # تقسيم الشاشة
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📡 Intelligence Acquisition")
        target_input = st.text_input("ENTER TARGET ID / NUMBER", placeholder="e.g. 010...")
        
        if st.button("RUN DEEP ANALYSIS"):
            if target_input:
                # هذا هو الجزء الذي يربط الزر بالكود الخاص بك
                with st.spinner("Analyzing patterns and vaulting data..."):
                    # تشغيل المسح العميق
                    scan_report = logic.run_deep_scan(target_input)
                    
                    # تحليل البيانات المشفرة
                    analysis = analyzer.analyze_content(scan_report)
                    risk_score = analyzer.get_critical_score(analysis)
                    
                    # حفظ التقرير في الخزنة المشفرة
                    vault.secure_store(f"WEB_REQ_{target_input}", f"Risk: {risk_score} | Report: {scan_report}")
                    
                    # حفظ النتائج في session_state لعرضها
                    st.session_state['last_scan_report'] = scan_report
                    st.success(f"Analysis complete for {target_input}. Data secured.")
            else:
                st.warning("Please enter a Target ID to begin analysis.")

    with col2:
        st.subheader("🖥️ Monitor")
        if 'last_scan_report' in st.session_state:
            st.code(st.session_state['last_scan_report'], language="bash")
        else:
            st.info("System Ready. Awaiting Command Input...")

    # قسم السجلات في الأسفل
    st.markdown("---")
    with st.expander("📂 ENCRYPTED LOGS"):
        logs = vault.get_all_logs()
        if logs:
            for log in logs[:10]:
                st.markdown(f"**[{log[1]}]** - ID: {log[0]}")
        else:
            st.write("No logs available in shadow_vault.db")

    st.sidebar.markdown("### 👑 Operator: Joseph Fahmy")
    st.sidebar.write("Sovereign AI Project v10.0")

if __name__ == "__main__":
    main()
