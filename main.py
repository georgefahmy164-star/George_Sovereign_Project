# ==============================================================================
# 👑 PROJECT: GEORGE TITAN - THE APEX (V20 - FINAL STABLE)
# 👑 ARCHITECT: GEORGE FAHMY (OSINT SPECIALIST)
# 👑 SECURITY: MAXIMUM | STATUS: 100% OPERATIONAL
# ==============================================================================

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# -----------------------------
# 🛡️ CONFIGURATION (SECRETS)
# -----------------------------
# تأكد من وضع المفتاح في Streamlit Secrets باسم: NUMVERIFY_KEY
NUM_KEY = st.secrets.get("NUMVERIFY_KEY", "")

class TitanApex:
    @staticmethod
    def fix_phone_format(phone):
        """تنظيف وتعديل صيغة الرقم تلقائياً لضمان استجابة الـ API"""
        clean = phone.strip().replace(" ", "").replace("+", "")
        # لو بدأ بـ 0، بنحوله لكود مصر 20
        if clean.startswith('0'):
            clean = '20' + clean[1:]
        # لو الرقم 10 أرقام (بدون كود الدولة وبدون 0) بنضيف 20
        elif len(clean) == 10:
            clean = '20' + clean
        return clean

    @staticmethod
    @st.cache_data(ttl=600) # يمنع الـ Crash ويحفظ النتائج مؤقتاً
    def get_intel(phone, key):
        formatted_target = TitanApex.fix_phone_format(phone)
        url = f"http://apilayer.net/api/validate?access_key={key}&number={formatted_target}"
        try:
            res = requests.get(url, timeout=15)
            return res.json()
        except Exception as e:
            return {"error": {"info": str(e)}}

# --- 🎨 UI DESIGN: THE ROYAL DARK THEME ---
st.set_page_config(page_title="GEORGE TITAN V20", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .stApp { background-color: #050505; color: #D4AF37; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 3rem; text-align: center; 
                  color: #D4AF37; text-shadow: 0 0 20px #D4AF37; margin-bottom: 20px; }
    div.stButton > button { border: 2px solid #D4AF37 !important; background: transparent !important; color: #D4AF37 !important; width: 100%; font-weight: bold; }
    div.stButton > button:hover { background: #D4AF37 !important; color: black !important; box-shadow: 0 0 30px #D4AF37; }
</style>
""", unsafe_allow_html=True)

# 🚀 MAIN APP
st.markdown("<h1 class='main-title'>🔱 TITAN APEX V20</h1>", unsafe_allow_html=True)
st.sidebar.markdown(f"### 🛡️ OPERATOR: **GEORGE**")

# اختيار الوحدة
module = st.sidebar.selectbox("COMMAND MODULE", ["🎯 Phone Scanner", "🌐 IP Map Tracker"])

if module == "🎯 Phone Scanner":
    st.subheader("Advanced Phone Intelligence")
    target = st.text_input("Enter Target Number (e.g. 01229166011)")
    
    if st.button("EXECUTE ANALYSIS"):
        if not NUM_KEY:
            st.error("🚨 API Key is missing in Streamlit Secrets!")
        elif target:
            with st.spinner("Bypassing Network Nodes..."):
                data = TitanApex.get_intel(target, NUM_KEY)
                
                if data.get("valid"):
                    st.success("Target Synchronized ✅")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Carrier", data.get("carrier"))
                    col2.metric("Country", data.get("country_name"))
                    col3.metric("Type", data.get("line_type"))
                    with st.expander("Show Detailed Metadata"):
                        st.json(data)
                else:
                    error_msg = data.get("error", {}).get("info", "Check Number Format")
                    st.error(f"❌ Analysis Failed: {error_msg}")
                    st.info("💡 Pro Tip: Try entering 201229166011")

elif module == "🌐 IP Map Tracker":
    st.subheader("Global Node Mapping")
    ip_target = st.text_input("Enter IP Address (e.g. 8.8.8.8)")
    
    if st.button("TRACE IP"):
        if ip_target:
            with st.spinner("Locking Satellite..."):
                ip_res = requests.get(f"http://ip-api.com/json/{ip_target}").json()
                if ip_res.get("status") == "success":
                    st.success(f"Located: {ip_res.get('city')}, {ip_res.get('country')}")
                    lat, lon = ip_res.get('lat'), ip_res.get('lon')
                    m = folium.Map(location=[lat, lon], zoom_start=12, tiles="CartoDB dark_matter")
                    folium.Marker([lat, lon], popup=ip_target).add_to(m)
                    st_folium(m, width="100%", height=400)
                else: st.error("IP Node not found.")

st.sidebar.divider()
st.sidebar.caption("Project: GEORGE SOVEREIGN")
