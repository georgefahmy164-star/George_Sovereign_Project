# ==============================================================================
# 👑 PROJECT: GEORGE TITAN - THE OMNI-ARCHITECT (FINAL V17.5)
# 👑 FEATURES: PHONE OSINT + IP TRACKER + SATELLITE MAPS
# 👑 SECURITY: ENHANCED SESSION & SECRETS MANAGEMENT
# ==============================================================================

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime

# -----------------------------
# 🛡️ CONFIGURATION (SECRETS)
# -----------------------------
# تأكد من إضافة المفتاح في إعدادات Secrets بالموقع باسم: NUMVERIFY_KEY
NUM_KEY = st.secrets.get("NUMVERIFY_KEY", "")

class TitanCore:
    @staticmethod
    @st.cache_data(ttl=600) # تخزين النتائج لمدة 10 دقائق لتقليل استهلاك الـ API والـ Crash
    def scan_phone(phone, api_key):
        clean_phone = phone.strip().replace(" ", "").replace("+", "")
        # الـ API يحتاج الرقم بدون + وبكود الدولة
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={clean_phone}"
        try:
            res = requests.get(url, timeout=10)
            return res.json()
        except: return {"error": "Connection Timeout"}

    @staticmethod
    @st.cache_data(ttl=600)
    def scan_ip(ip_address):
        url = f"http://ip-api.com/json/{ip_address}"
        try:
            res = requests.get(url, timeout=10)
            return res.json()
        except: return {"error": "IP Trace Failed"}

# --- 🎨 UI: ROYAL DARK THEME ---
st.set_page_config(page_title="GEORGE TITAN V17", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .stApp { background-color: #050505; color: #D4AF37; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 3rem; text-align: center; 
                  color: #D4AF37; text-shadow: 0 0 20px #D4AF37; margin-bottom: 30px; }
    .stTextInput>div>div>input { background-color: #111; color: #D4AF37; border: 1px solid #D4AF37; }
    div.stButton > button { border: 2px solid #D4AF37 !important; background: transparent !important; color: #D4AF37 !important; width: 100%; height: 3em; font-weight: bold; }
    div.stButton > button:hover { background: #D4AF37 !important; color: black !important; box-shadow: 0 0 30px #D4AF37; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🚀 APP INTERFACE
# -----------------------------
def main():
    st.markdown("<h1 class='main-title'>🔱 GEORGE TITAN OMNI-V17</h1>", unsafe_allow_html=True)
    
    # القائمة الجانبية (Sidebar)
    with st.sidebar:
        st.header("🛠️ Command Center")
        module = st.radio("Select Mission:", ["🎯 Phone Scanner", "🌐 IP Map Tracker"])
        st.divider()
        st.write("👤 Operator: **GEORGE**")
        st.caption(f"System Time: {datetime.now().strftime('%H:%M:%S')}")

    # 1. موديل فحص الهاتف
    if module == "🎯 Phone Scanner":
        st.subheader("Target Intelligence: Phone Metadata")
        target_phone = st.text_input("Enter Phone Number (e.g., 201229166011)")
        
        if st.button("LAUNCH PHONE ANALYSIS"):
            if not NUM_KEY:
                st.error("🚨 API Key missing! Add 'NUMVERIFY_KEY' to Streamlit Secrets.")
            elif target_phone:
                with st.spinner("Decrypting Network Signals..."):
                    data = TitanCore.scan_phone(target_phone, NUM_KEY)
                    if data.get("valid"):
                        st.success("Target Synchronized ✅")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Carrier", data.get("carrier"))
                        col2.metric("Country", data.get("country_name"))
                        col3.metric("Line Type", data.get("line_type"))
                        with st.expander("Show Full Metadata"):
                            st.json(data)
                    else: st.error("Target verification failed. Check format.")

    # 2. موديل تتبع الـ IP والخرائط
    elif module == "🌐 IP Map Tracker":
        st.subheader("Target Intelligence: Satellite IP Mapping")
        target_ip = st.text_input("Enter IP Address (e.g., 8.8.8.8)")
        
        if st.button("TRACE & VISUALIZE"):
            if target_ip:
                with st.spinner("Locking Satellite Coordinates..."):
                    ip_data = TitanCore.scan_ip(target_ip)
                    if ip_data.get("status") == "success":
                        st.success(f"Node Located: {ip_data.get('city')}, {ip_data.get('country')} ✅")
                        
                        # استخراج الإحداثيات ورسم الخريطة
                        lat, lon = ip_data.get('lat'), ip_data.get('lon')
                        m = folium.Map(location=[lat, lon], zoom_start=12, tiles="CartoDB dark_matter")
                        folium.Marker(
                            [lat, lon], 
                            popup=f"IP: {target_ip}",
                            icon=folium.Icon(color='orange', icon='dot')
                        ).add_to(m)
                        
                        # عرض الخريطة
                        st_folium(m, width="100%", height=450)
                        
                        # تفاصيل إضافية
                        st.info(f"📍 ISP: {ip_data.get('isp')} | Org: {ip_data.get('org')}")
                    else: st.error("IP Node not found.")

if __name__ == "__main__":
    main()
