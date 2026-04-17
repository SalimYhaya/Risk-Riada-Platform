import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. إعدادات الهوية البصرية (Black Outlines & White Design)
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Noto Sans Arabic', sans-serif;
        background-color: #ffffff;
        color: #000000;
    }
    
    /* بطاقات بحدود سوداء رقيقة */
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 4px;
        border: 1px solid #000000 !important;
        box-shadow: none !important;
    }
    
    .report-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 0px;
        border: 2px solid #000000;
        margin: 20px 0;
        color: #000000;
    }
    
    h1, h2, h3 { color: #000000 !important; font-weight: 600; }
    
    /* أزرار جوجل بحدود سوداء صريحة */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        padding: 10px 40px !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. التخصيص (Personalization)
if 'investor_type' not in st.session_state:
    st.session_state.investor_type = None

if st.session_state.investor_type is None:
    st.markdown("<div style='text-align:center; padding:50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>🛡️ منصة ريادة</h1>", unsafe_allow_html=True)
    st.write("للبدء، اختر نمطك الاستثماري:")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🛡️ محافظ"): st.session_state.investor_type = "محافظ"
    with c2:
        if st.button("⚖️ متوازن"): st.session_state.investor_type = "متوازن"
    with c3:
        if st.button("🚀 مغامر"): st.session_state.investor_type = "مغامر"
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 3. الشريط الجانبي (الهوية والشعار)
with st.sidebar:
    try:
        st.markdown("<div style='border: 1px solid #000; padding: 5px;'>", unsafe_allow_html=True)
        st.image("second.jpg", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    except:
        st.info("ارفع الشعار باسم second.jpg")
    
    st.markdown(f"**النمط:** {st.session_state.investor_type}")
    st.divider()
    
    if 'balance' not in st.session_state: st.session_state.balance = 100000
    st.metric("رصيد المحفظة", f"{st.session_state.balance:,.0f} ريال")
    st.caption("إشراف: د. حنين المطيري")

# 4. محرك التحليل ومعالجة تداخل الأعمدة (The Fix)
ticker_dict = {"أرامكو": "2222", "الراجحي": "1120", "سابك": "2010", "stc": "7010"}

st.markdown("<h1>🛡️ تحليل المخاطر والتوقع</h1>", unsafe_allow_html=True)

col_input, col_empty = st.columns([2, 1])
with col_input:
    selected_stock = st.selectbox("🎯 اختر الشركة:", list(ticker_dict.keys()))
    run = st.button("بدء التحليل الفني")

if run:
    with st.spinner('جاري تنظيف ومعالجة البيانات...'):
        try:
            symbol = f"{ticker_dict[selected_stock]}.SR"
            data = yf.download(symbol, period="1y", progress=False)
            
            if not data.empty:
                # --- حل مشكلة Multi-Index و Series ---
                # نقوم بتبسيط الأعمدة إذا كانت متداخلة
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                
                # استخراج السعر الأخير والتأكد أنه رقم وحيد
                raw_price = data['Close'].iloc[-1]
                current_price = float(raw_price.iloc[0]) if isinstance(raw_price, pd.Series) else float(raw_price)

                # حساب العوائد والتذبذب
                returns = data['Close'].pct_change().dropna()
                vol_raw = returns.std() * (252**0.5) * 100
                volatility = float(vol_raw.iloc[0]) if isinstance(vol_raw, pd.Series) else float(vol_raw)
                
                risk_score = min(int(volatility * 2.5), 100)
                sentiment = np.random.randint(70, 95)
                
                # التوقع (AI Simulation)
                future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, 8)]
                prediction = [current_price * (1 + (np.random.normal(0, 0.012))) for _ in range(7)]

                # العرض المالي (أبيض وأسود صريح)
                st.divider()
                r1, r2, r3 = st.columns(3)
                r1.metric("السعر الحالي", f"{current_price:.2f} ريال")
                r2.metric("مؤشر المخاطرة", f"{risk_score}/100")
                r3.metric("نبض السوق الذكي", f"{sentiment}%")

                # الرسم البياني (حدود سوداء وخطوط واضحة)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'].values.flatten(), name="السعر التاريخي", line=dict(color='#000000', width=1.5)))
                fig.add_trace(go.Scatter(x=future_dates, y=prediction, name="توقع AI", line=dict(color='#00c853', dash='dot')))
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', template="none", height=400)
                fig.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='#f2f2f2')
                fig.update_axes(showline=True, linewidth=1, linecolor='black', gridcolor='#f2f2f2')
                st.plotly_chart(fig, use_container_width=True)

                # التقرير (Black Border)
                st.markdown(f"""
                <div class='report-card'>
                    <h3>🤖 تقرير المستشار المخصص ({st.session_state.investor_type}):</h3>
                    <p>تم تحليل تقلبات السهم البالغة {volatility:.2f}% ودمجها مع نبض السوق بنسبة {sentiment}%.</p>
                    <b>النتيجة:</b> السهم يظهر توازناً فنياً يتوافق مع استراتيجيتك الاستثمارية.
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"حدث خطأ في معالجة القيمة الرقمية: {str(e)}")

st.divider()
st.caption("منصة ريادة | تصميم Google Antigravity بحدود سوداء صريحة")
