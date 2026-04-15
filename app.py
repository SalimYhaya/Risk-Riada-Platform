import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الهوية البصرية (العودة للألوان الفخمة والخطوط الكبيرة)
st.set_page_config(page_title="ريادة لمخاطر الاستثمار", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    /* تحسين الخلفية والألوان العامة */
    .main { background-color: #0e1117; color: #e0e0e0; }
    
    /* تكبير وتحسين الخطوط */
    html, body, [class*="st-"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 18px; /* حجم خط مريح للقراءة */
    }
    
    h1 { font-size: 3rem !important; color: #00c853 !important; font-weight: 800 !important; }
    h2 { font-size: 2rem !important; color: #00c853 !important; }
    h3 { font-size: 1.5rem !important; color: #ffffff !important; }
    
    /* تحسين شكل بطاقات النتائج */
    .stMetric { 
        background-color: #1c2128; 
        padding: 25px !important; 
        border-radius: 15px !important; 
        border: 1px solid #30363d !important;
    }
    
    /* زر التحليل */
    .stButton>button {
        background-color: #00c853 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 15px 30px !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
    }
    
    /* التنويه الجانبي */
    .sidebar .sidebar-content { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# 2. البيانات والشركات
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

ticker_options = list(ticker_dict.keys())
ticker_options.append("أدخل رمز شركة أخرى يدوياً...")

# 3. الشريط الجانبي (أيقونة الباحثة والاسم بوضوح)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=120) 
    
    st.markdown("<h2 style='text-align: center; color: white !important;'>إشراف أكاديمي</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.4rem; color: #00c853;'><b>سعادة الدكتورة<br>حنين بنت عبد الرحمن المطيري</b></p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='font-size: 0.9rem; color: #8b949e;'>مشروع بحثي تجريبي لاختبار قدرات الذكاء الاصطناعي في قياس مخاطر الاستثمار.</p>", unsafe_allow_html=True)

# 4. واجهة المنصة الرئيسية
st.markdown("<h1 style='text-align: center;'>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>استشراف ذكي للمخاطر المالية في السوق السعودي</h3>", unsafe_allow_html=True)
st.divider()

# 5. منطقة التحكم
col_sel, col_empty = st.columns([2, 1])
with col_sel:
    selected_option = st.selectbox("🎯 اختر الشركة المستهدفة:", ticker_options)

if selected_option == "أدخل رمز شركة أخرى يدوياً...":
    manual_ticker = st.text_input("✍️ أدخل الرمز (4 أرقام):", placeholder="مثال: 4003")
    ticker = manual_ticker.strip()
else:
    ticker = ticker_dict[selected_option]

st.markdown("<br>", unsafe_allow_html=True)
start_analysis = st.button("🔍 تشغيل محرك تحليل المخاطر")

# 6. المعالجة والنتائج
if start_analysis:
    if not ticker or not ticker.isdigit() or len(ticker) != 4:
        st.error("❌ الرجاء إدخال رمز صحيح (4 أرقام).")
    else:
        with st.spinner('جاري الاتصال بقواعد البيانات وتحليل المخاطر...'):
            try:
                full_ticker = f"{ticker}.SR"
                data = yf.download(full_ticker, period="1y", progress=False)
                
                if data.empty:
                    st.warning("⚠️ لم نتمكن من العثور على بيانات لهذه الشركة حالياً.")
                else:
                    data['Returns'] = data['Close'].pct_change()
                    volatility = data['Returns'].std() * (252**0.5) * 100
                    risk_score = min(int(volatility * 2.5), 100)
                    
                    if risk_score > 70:
                        risk_status, color = "مرتفعة جداً", "#ff4b4b"
                    elif risk_score > 40:
                        risk_status, color = "متوسطة", "#ffa500"
                    else:
                        risk_status, color = "منخفضة", "#00c853"

                    # عرض النتائج بشكل ضخم وواضح
                    st.markdown(f"<h2>📊 نتائج التحليل لشركة: {selected_option.split('(')[0]}</h2>", unsafe_allow_html=True)
                    m1, m2, m3 = st.columns(3)
                    
                    m1.metric("مؤشر المخاطرة", f"{risk_score}/100")
                    m2.metric("تذبذب السهم السنوي", f"{volatility:.1f}%")
                    with m3:
                         st.markdown(f"<div class='stMetric' style='text-align: center;'><p style='font-size:1.2rem; margin:0;'>حالة المخاطرة</p><h2 style='color: {color} !important; margin:0;'>{risk_status}</h2></div>", unsafe_allow_html=True)

                    # الرسم البياني
                    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], line=dict(color='#00c853', width=3))])
                    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"حدث خطأ فني: {e}")
else:
    st.markdown("<p style='text-align: center; color: #8b949e;'><br>اختر شركة من القائمة أعلاه لبدء عملية النمذجة</p>", unsafe_allow_html=True)
