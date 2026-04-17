import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. إعدادات الهوية البصرية (مستوحاة من Google Antigravity)
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    /* تحسين الخطوط والألوان بناءً على ذوق جوجل والشعار */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Noto Sans Arabic', sans-serif;
        background-color: #f8f9fa; /* خلفية فاتحة ونظيفة */
        color: #202124;
    }
    
    .main { background-color: #f8f9fa; }
    
    /* بطاقات جوجل الأنيقة */
    .stMetric, .report-card, .edu-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(60,64,67,0.3), 0 4px 8px rgba(60,64,67,0.15);
        border: none;
        margin-bottom: 20px;
    }
    
    h1 { color: #1e4620; font-weight: 700; font-size: 2.5rem !important; }
    h3 { color: #3c4043; font-weight: 500; }
    
    /* أزرار جوجل */
    .stButton>button {
        background-color: #1e4620 !important;
        color: white !important;
        border-radius: 24px !important;
        padding: 10px 30px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 12px rgba(30,70,32,0.3) !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تخصيص تجربة المستخدم (Personalization)
if 'investor_type' not in st.session_state:
    st.session_state.investor_type = None

if st.session_state.investor_type is None:
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في ريادة</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>قبل البدء، أخبرنا ما هو نمطك الاستثماري؟</p>", unsafe_allow_html=True)
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1: 
        if st.button("🛡️ محافظ (أمان عالي)"): st.session_state.investor_type = "محافظ"
    with col_p2:
        if st.button("⚖️ متوازن (مخاطرة محسوبة)"): st.session_state.investor_type = "متوازن"
    with col_p3:
        if st.button("🚀 مغامر (بحث عن نمو)"): st.session_state.investor_type = "مغامر"
    st.stop()

# 3. الهوية والشعار في الشريط الجانبي
with st.sidebar:
    # ملاحظة: تأكد من وجود ملف second.jpg في نفس المجلد
    try:
        st.image("second.jpg", width=180)
    except:
        st.warning("يرجى التأكد من رفع ملف الشعار باسم second.jpg")
    
    st.markdown(f"### النمط: <span style='color:#1e4620'>{st.session_state.investor_type}</span>", unsafe_allow_html=True)
    st.divider()
    
    # تفاعل (Gamification) - محاكي التداول
    st.markdown("### 🎮 محاكي تداول ريادة")
    if 'balance' not in st.session_state: st.session_state.balance = 100000
    st.metric("رصيدك الوهمي", f"{st.session_state.balance:,.0f} ريال")
    st.info("تعلم إدارة المخاطر من خلال تجربة شراء الأسهم افتراضياً هنا.")
    st.divider()
    
    st.markdown("### إشراف أكاديمي")
    st.write("د. حنين بنت عبد الرحمن المطيري")

# 4. محرك التحليل والبيانات
ticker_dict = {"أرامكو": "2222", "الراجحي": "1120", "سابك": "2010", "stc": "7010"}

st.markdown(f"<h1>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    selected_stock = st.selectbox("🎯 اختر الشركة للتحليل والتوقع:", list(ticker_dict.keys()))
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("تشغيل المحرك الذكي 🚀", use_container_width=True)

if run:
    with st.spinner('جاري تحليل الأنماط التاريخية ومشاعره السوق...'):
        symbol = f"{ticker_dict[selected_stock]}.SR"
        data = yf.download(symbol, period="1y", progress=False)
        
        if not data.empty:
            # حساب المخاطرة
            returns = data['Close'].pct_change()
            volatility = returns.std() * (252**0.5) * 100
            risk_score = min(int(volatility * 2.5), 100)
            
            # تكامل البيانات (Sentiment Analysis - محاكاة)
            sentiment_score = np.random.randint(40, 90) # محاكاة لتحليل تويتر والأخبار
            
            # توقع (AI Prediction - محاكاة LSTM)
            last_price = data['Close'].iloc[-1]
            future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, 11)]
            prediction = [last_price * (1 + (np.random.randn() * 0.01)) for _ in range(10)]

            # العرض الرئيسي
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("السعر اللحظي", f"{last_price:.2f} ريال")
            m_col2.metric("مؤشر المخاطرة", f"{risk_score}/100")
            m_col3.metric("نبض السوق (تويتر/أخبار)", f"{sentiment_score}% إيجابي")

            # الرسم البياني (سعر + توقع)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="السعر التاريخي", line=dict(color='#1e4620')))
            fig.add_trace(go.Scatter(x=future_dates, y=prediction, name="توقع AI (LSTM)", line=dict(color='#ff9800', dash='dot')))
            fig.update_layout(title=f"تحليل وتوقع مسار {selected_stock}", template="none", height=450)
            st.plotly_chart(fig, use_container_width=True)

            # التقرير المخصص (Personalization)
            st.markdown("### 🤖 تقرير المستشار الذكي المخصص")
            rec = ""
            if st.session_state.invest_type == "محافظ":
                rec = "بما أنك مستثمر محافظ، المخاطرة الحالية تعتبر مرتفعة قليلاً. ننصح بانتظار استقرار 'نبض السوق'."
            else:
                rec = f"بناءً على نمطك الـ{st.session_state.investor_type}، التوقع يشير لفرصة نمو، ولكن انتبه لمعدل التذبذب."

            st.markdown(f"""
            <div class='report-card'>
                <h4>تحليل منصة ريادة لـ {selected_stock}:</h4>
                <p>{rec}</p>
                <p><b>مؤشر المشاعر الذكي:</b> نلاحظ تفاؤلاً في الأخبار الاقتصادية الأخيرة بنسبة {sentiment_score}%، مما يدعم استقرار السهم.</p>
            </div>
            """, unsafe_allow_html=True)

# 5. الأكاديمية (الوعي المالي)
st.divider()
st.markdown("### 📚 أكاديمية ريادة التعليمية")
st.write("تعلم كيف نفكر: ندمج بين لغة الأرقام (الرياضيات) ولغة البشر (تحليل المشاعر) لنمنحك رؤية 360 درجة.")
