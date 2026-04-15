import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. إعدادات الهوية البصرية (ألوان المسودة الأولى مع تحسين الخطوط)
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1c2128; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    .header-text { text-align: center; color: #00c853; font-weight: bold; font-size: 2.5rem; }
    .recommendation-box { padding: 20px; border-radius: 15px; text-align: center; margin-top: 10px; }
    html, body, [class*="st-"] { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. قاعدة بيانات الشركات والقطاعات (لتحسين المقارنة)
ticker_data = {
    "أرامكو السعودية (2222)": {"id": "2222", "sector": "الطاقة"},
    "مصرف الراجحي (1120)": {"id": "1120", "sector": "البنوك"},
    "سابك (2010)": {"id": "2010", "sector": "المواد الأساسية"},
    "إس تي سي - stc (7010)": {"id": "7010", "sector": "الاتصالات"},
    "الأهلي السعودي (1180)": {"id": "1180", "sector": "البنوك"},
    "معادن (1211)": {"id": "1211", "sector": "المواد الأساسية"},
    "كهرباء السعودية (5110)": {"id": "5110", "sector": "المرافق العامة"},
    "مجموعة تداول (1111)": {"id": "1111", "sector": "الخدمات المالية"},
    "جرير (4190)": {"id": "4190", "sector": "التجزئة"},
    "المراعي (2280)": {"id": "2280", "sector": "الأغذية"}
}

# 3. الشريط الجانبي (تحسين الهوية الأكاديمية)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=110)
    st.markdown("<h3 style='text-align: center;'>إشراف</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00c853; font-weight: bold;'>د. حنين بنت عبد الرحمن المطيري</p>", unsafe_allow_html=True)
    st.divider()
    st.info("📊 **تطوير:** تم استخدام نماذج تحليل البيانات التاريخية لتقدير مستويات الأمان الاستثماري.")

# 4. العنوان الرئيسي
st.markdown("<h1 class='header-text'>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>النظام الذكي لتقييم أمان الأوراق المالية في السوق السعودي</p>", unsafe_allow_html=True)

# 5. منطقة الاختيار المحسنة (UI/UX)
col_a, col_b = st.columns([2, 1])
with col_a:
    selection = st.selectbox("🎯 اختر الشركة للتحليل المتقدم:", list(ticker_data.keys()) + ["أدخل رمزاً مخصصاً..."])
with col_b:
    period = st.select_slider("📅 فترة التحليل:", options=["6 أشهر", "سنة", "سنتين"], value="سنة")

ticker = ticker_data[selection]["id"] if selection != "أدخل رمزاً مخصصاً..." else st.text_input("الرمز (4 أرقام):")

if st.button("🚀 تشغيل المحرك التحليلي"):
    if ticker:
        with st.spinner('جاري معالجة البيانات الضخمة...'):
            try:
                full_ticker = f"{ticker}.SR"
                time_map = {"6 أشهر": "180d", "سنة": "1y", "سنتين": "2y"}
                data = yf.download(full_ticker, period=time_map[period], progress=False)
                
                if not data.empty:
                    # حسابات مالية متقدمة
                    curr_price = data['Close'].iloc[-1]
                    data['Returns'] = data['Close'].pct_change()
                    volatility = data['Returns'].std() * (252**0.5) * 100
                    risk_score = min(int(volatility * 2.8), 100)
                    
                    # مؤشر RSI (لقوة الاتجاه)
                    delta = data['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs)).iloc[-1]

                    # منطق التوصية المحسن
                    if risk_score < 45 and rsi < 70:
                        rec, color, note = "فرصة شراء (آمن)", "#00c853", "المخاطرة منخفضة والسهم في منطقة سعرية جيدة."
                    elif risk_score > 75 or rsi > 80:
                        rec, color, note = "بيع / جني أرباح", "#ff4b4b", "المخاطرة مرتفعة جداً أو السهم متضخم سعرياً."
                    else:
                        rec, color, note = "انتظار / مراقبة", "#ffa500", "حالة السوق غير مستقرة لهذا السهم حالياً."

                    # عرض الواجهة (UX Optimization)
                    st.markdown(f"### 📊 نتائج تحليل: {selection}")
                    
                    # الصف الأول: السعر والتوصية
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("السعر اللحظي", f"{float(curr_price):.2f} ريال")
                    with c2:
                        st.markdown(f"<div class='recommendation-box' style='border: 2px solid {color};'>"
                                    f"<h3 style='color:{color}; margin:0;'>{rec}</h3>"
                                    f"<p style='margin:0; font-size:0.9rem;'>{note}</p></div>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # الصف الثاني: تفاصيل المخاطرة
                    c3, c4, c5 = st.columns(3)
                    c3.metric("مؤشر المخاطرة", f"{risk_score}/100")
                    c4.metric("التذبذب (Volatility)", f"{volatility:.1f}%")
                    c5.metric("مؤشر القوة (RSI)", f"{rsi:.1f}")

                    # الرسم البياني المتقدم
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='السعر', line=dict(color='#00c853', width=2)))
                    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,b=0,t=40),
                                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#333'))
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"حدث خطأ: {e}")
