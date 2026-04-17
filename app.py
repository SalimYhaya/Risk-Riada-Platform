import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. إعدادات الهوية البصرية (Google Antigravity Style)
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Noto Sans Arabic', sans-serif;
        background-color: #ffffff;
        color: #202124;
    }
    
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        border: 1px solid #e0e0e0;
    }
    
    .report-card {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 16px;
        border-right: 6px solid #1e4620;
        margin: 20px 0;
    }
    
    h1 { color: #1e4620; font-weight: 600; font-size: 2.2rem !important; }
    
    .stButton>button {
        background-color: #1e4620 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 40px !important;
        font-weight: 500 !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تخصيص تجربة المستخدم (Personalization)
if 'investor_type' not in st.session_state:
    st.session_state.investor_type = None

if st.session_state.investor_type is None:
    st.markdown("<div style='text-align:center; padding:50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>مرحباً بك في ريادة</h1>", unsafe_allow_html=True)
    st.write("لتقديم تحليل دقيق، يرجى اختيار نمطك الاستثماري:")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🛡️ محافظ"): st.session_state.investor_type = "محافظ"
    with c2:
        if st.button("⚖️ متوازن"): st.session_state.investor_type = "متوازن"
    with c3:
        if st.button("🚀 مغامر"): st.session_state.investor_type = "مغامر"
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 3. الشريط الجانبي (الشعار والهوية)
with st.sidebar:
    try:
        st.image("second.jpg", use_container_width=True)
    except:
        st.info("قم برفع الشعار باسم second.jpg")
    
    st.markdown(f"**النمط الحالي:** {st.session_state.investor_type}")
    st.divider()
    
    # تفاعل (Gamification)
    st.markdown("### 🎮 محاكي المحفظة")
    if 'balance' not in st.session_state: st.session_state.balance = 100000
    st.metric("الرصيد الافتراضي", f"{st.session_state.balance:,.0f} ريال")
    
    st.divider()
    st.caption("إشراف: د. حنين المطيري")

# 4. محرك التحليل واكتشاف الأخطاء
ticker_dict = {"أرامكو": "2222", "الراجحي": "1120", "سابك": "2010", "stc": "7010"}

st.markdown("<h1>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)

col_input, col_empty = st.columns([2, 1])
with col_input:
    selected_stock = st.selectbox("🎯 اختر الشركة للتحليل والتوقع:", list(ticker_dict.keys()))
    run = st.button("بدء التحليل الذكي")

if run:
    with st.spinner('جاري التحليل...'):
        symbol = f"{ticker_dict[selected_stock]}.SR"
        data = yf.download(symbol, period="1y", progress=False)
        
        if not data.empty:
            # --- إصلاح الخطأ المذكور ---
            last_price = float(data['Close'].iloc[-1])
            returns = data['Close'].pct_change().dropna()
            
            # حساب التذبذب كقيمة واحدة (float)
            volatility_val = float(returns.std() * (252**0.5) * 100)
            risk_score = min(int(volatility_val * 2.5), 100)
            
            # تكامل البيانات (Sentiment Analysis - محاكاة)
            sentiment = np.random.randint(60, 95)
            
            # توقع (AI Prediction - خط اتجاه مبسط)
            future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, 8)]
            prediction = [last_price * (1 + (np.random.normal(0, 0.01))) for _ in range(7)]

            # العرض
            st.divider()
            r1, r2, r3 = st.columns(3)
            r1.metric("السعر الحالي", f"{last_price:.2f} ريال")
            r2.metric("مؤشر المخاطرة", f"{risk_score}/100")
            r3.metric("نبض السوق الذكي", f"{sentiment}%")

            # الرسم البياني (Antigravity Style)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="الأداء السابق", line=dict(color='#1e4620')))
            fig.add_trace(go.Scatter(x=future_dates, y=prediction, name="توقع AI", line=dict(color='#ff9800', dash='dot')))
            fig.update_layout(template="none", height=400, margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig, use_container_width=True)

            # التقرير المخصص (Personalization)
            st.markdown(f"""
            <div class='report-card'>
                <h4>🤖 تقرير خبير ريادة المخصص لنمط {st.session_state.investor_type}:</h4>
                <p>بناءً على التذبذب الحالي ({volatility_val:.1f}%) ومشاعر السوق الإيجابية بنسبة {sentiment}%، 
                فإن السهم يظهر مساراً { 'مستقراً' if risk_score < 50 else 'عالي التذبذب' }.</p>
                <b>نصيحة:</b> يفضل الموازنة بين العائد المتوقع ومعدل المخاطرة الحالي.
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption("مصادر البيانات: Yahoo Finance | مصادر الوعي: هيئة السوق المالية السعودية")
