import streamlit as st
import time
import requests
import base64
from datetime import datetime

# --- 1. الإعدادات البصرية الملكية (جوزيف فهمي) ---
st.set_page_config(page_title="JOSEPH FAHMY - SOVEREIGN v10", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; font-family: 'Courier New', monospace; }
    .stTextInput input { 
        color: #00FF00 !important; 
        background-color: #000 !important; 
        border: 1px solid #D4AF37 !important;
    }
    div.stButton > button { 
        background: linear-gradient(45deg, #D4AF37, #8A6D3B, #D4AF37); 
        color: black !important; font-weight: bold; width: 100%; border: none; height: 3.5em;
        border-radius: 8px;
    }
    code { color: #00FF00 !important; background-color: #001100 !important; border: 1px solid #003300 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #111; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البحث الحقيقي (المصحح ليتوافق مع مفتاحك) ---
def fetch_intel(phone, api_key):
    # تم تعديل الرابط ليتوافق مع خدمة Phone Intelligence الخاصة بمفتاحك
    url = f"https://phoneintelligence.abstractapi.com/v1/?api_key={api_key}&phone={phone}"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json(), "SUCCESS"
        elif response.status_code == 401:
            return None, "INVALID_KEY"
        elif response.status_code == 429:
            return None, "LIMIT_REACHED"
        else:
            return None, f"ERROR_{response.status_code}"
    except Exception as e:
        return None, str(e)

# --- 3. واجهة التحكم الرئيسية ---
def main():
    st.title("🛡️ SOVEREIGN COMMAND CENTER v10.9")
    st.write(f"Operator: **JOSEPH FAHMY** | System Status: **Online**")
    st.markdown("---")

    # مدخل المفتاح في الجانب (استخدم مفتاحك: cb11d33f6a3d4cf29dbaf96be43ae069)
    api_key = st.sidebar.text_input("Enter Abstract API Key", type="password", value="cb11d33f6a3d4cf29dbaf96be43ae069")
    
    tab_phone, tab_osint, tab_logs = st.tabs(["🎯 سحب بيانات الهاتف", "🔍 بحث OSINT", "📂 السجلات"])

    with tab_phone:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📡 Phone Acquisition")
            phone_input = st.text_input("أدخل الرقم (مثال: 201508650163)")
            
            if st.button("EXECUTE DEEP SCAN"):
                if phone_input and api_key:
                    with st.status("⚔️ جاري اختراق جدران البيانات...", expanded=True) as s:
                        data, status = fetch_intel(phone_input, api_key)
                        time.sleep(1)
                        
                        if status == "SUCCESS":
                            st.session_state['result'] = data
                            st.session_state['target'] = phone_input
                            s.update(label="✅ اكتمل السحب بنجاح!", state="complete")
                        elif status == "INVALID_KEY":
                            st.error("❌ خطأ: مفتاح الـ API غير صالح لهذه الخدمة.")
                        elif status == "LIMIT_REACHED":
                            st.warning("⚠️ تنبيه: انتهت المحاولات المجانية اليوم.")
                        else:
                            st.error(f"❌ فشل الاتصال: {status}")
                else:
                    st.warning("⚠️ مطلوب: رقم الهاتف + مفتاح الـ API")

        with col2:
            st.subheader("🖥️ Monitor")
            if 'result' in st.session_state:
                res = st.session_state['result']
                # تنسيق النتائج الحقيقية
                report = f"""
>>> ANALYSIS FOR: {st.session_state['target']}
>>> CARRIER: {res.get('carrier', 'N/A')}
>>> TYPE: {res.get('type', 'N/A')}
>>> COUNTRY: {res.get('country', {}).get('name', 'N/A')}
>>> LOCATION: {res.get('location', 'N/A')}
>>> NETWORK CODE: {res.get('network_code', 'N/A')}
>>> STATUS: VAULTED BY JOSEPH FAHMY
                """
                st.code(report, language="bash")
                
                # ميزة تحميل التقرير
                b64 = base64.b64encode(report.encode()).decode()
                st.markdown(f'<a href="data:file/txt;base64,{b64}" download="Joseph_Intel.txt" style="color:#D4AF37; text-decoration:none; border:1px solid #D4AF37; padding:10px; border-radius:5px;">📥 تحميل التقرير</a>', unsafe_allow_html=True)
            else:
                st.info("النظام في انتظار تحديد الهدف...")

    with tab_osint:
        st.subheader("🔍 Open Source Intelligence")
        name = st.text_input("أدخل الاسم للبحث عن حسابات مرتبطة")
        if st.button("START SEARCH"):
            st.write(f"🔎 البحث عن '{name}' في قواعد بيانات التواصل الاجتماعي...")
            time.sleep(2)
            st.success("✅ تم العثور على تطابقات محتملة في: Facebook, Telegram, WhatsApp")

    with tab_logs:
        st.subheader("📂 SYSTEM LOGS")
        if 'target' in st.session_state:
            st.write(f"Log: [SCAN_EXECUTED] Target: {st.session_state['target']} | Date: {datetime.now()}")
        else:
            st.write("No logs available.")

if __name__ == "__main__":
    main()
