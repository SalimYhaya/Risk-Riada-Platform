import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. إعدادات الهوية البصرية (العودة للألوان والخطوط الأصلية)
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .header-text { text-align: center; color: #00c853; font-weight: bold; }
    /* تحسين الخطوط كما في المسودة الأولى */
    html, body, [class*="st-"] {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. بيانات الشركات والسوق
ticker_dict = {
    "أرامكو السعودية (2222)": "2222",
    "مصرف الراجحي (1120)": "1120",
    "سابك (2010)": "2010",
    "البنك الأهلي السعودي (1180)": "1180",
    "إس تي سي - stc (7010)": "7010",
    "معادن (1211)": "1211",
    "كهرباء السعودية (5110)": "5110",
    "مجموعة تداول (1111)": "1111",
    "جرير (4190)": "4190",
    "المراعي (2280)": "2280"
}

# 3. الشريط الجانبي (الإشراف)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=100)
    st.write(f"### إشراف")
    st.info("د. حنين بنت عبد الرحمن المطيري")
    st.divider()
    st.write("⚠️ **غرض التجربة:** بحث علمي وبرمجي فقط")

# 4. العنوان الرئيسي
st.markdown("<h1 class='header-text'>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>تحليل ذكي ومؤشرات لحظية للسوق السعودي</h3>", unsafe_allow_html=True)

st.divider()

# 5. منطقة المدخلات
col_sel, col_empty = st.columns([2, 1])
with col_sel:
    selected_option = st.selectbox("اختر الشركة أو أدخل الرمز يدوياً:", list(ticker_dict.keys()) + ["أدخل رمزاً مخصصاً..."])

if selected_option == "أدخل رمزاً مخصصاً...":
    manual_ticker = st.text_input("أدخل الرمز (4 أرقام):")
    ticker = manual_ticker.strip()
else:
    ticker = ticker_dict[selected_option]

start_analysis = st.button("تحليل البيانات الآن")

# 6. منطق المعالجة والنتائج
if start_analysis:
    if ticker:
        with st.spinner('جاري سحب البيانات وحساب المؤشرات...'):
            try:
                full_ticker = f"{ticker}.SR"
                stock = yf.Ticker(full_ticker)
                data = stock.history(period="1y")
                
                if data.empty:
                    st.error("لم يتم العثور على بيانات.")
                else:
                    # حساب المؤشرات
                    current_price = data['Close'].iloc[-1]
                    data['Returns'] = data['Close'].pct_change()
                    volatility = data['Returns'].std() * (252**0.5) * 100
                    risk_score = min(int(volatility * 2.5), 100)
                    
                    # منطق التوصية (مبني على المخاطرة والاتجاه)
                    ma20 = data['Close'].rolling(window=20).mean().iloc[-1]
                    if risk_score < 40 and current_price > ma20:
                        recommendation = "شراء (استثماري)"
                        rec_color = "#00c853"
                    elif risk_score > 70:
                        recommendation = "تجنب / بيع"
                        rec_color = "#ff4b4b"
                    else:
                        recommendation = "مراقبة / انتظار"
                        rec_color = "#ffa500"

                    # عرض النتائج في صفوف واضحة
                    st.divider()
                    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
                    col_res1.metric("السعر الحالي", f"{current_price:.2f} ريال")
                    col_res2.metric("درجة المخاطرة", f"{risk_score}/100")
                    col_res3.metric("التذبذب السنوي", f"{volatility:.1f}%")
                    
                    with col_res4:
                        st.markdown(f"<div style='background-color:#1e1e1e; padding:10px; border-radius:10px; text-align:center; border:1px solid {rec_color};'>"
                                    f"<p style='margin:0; font-size:0.8em;'>التوصية الذكية</p>"
                                    f"<h4 style='margin:0; color:{rec_color};'>{recommendation}</h4></div>", unsafe_allow_html=True)

                    # الرسم البياني
                    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], name="السعر", line=dict(color='#00c853'))])
                    fig.update_layout(template="plotly_dark", title=f"تحرك السهم: {ticker}")
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"خطأ في جلب البيانات: {e}")
