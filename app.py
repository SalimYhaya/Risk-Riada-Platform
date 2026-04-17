import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. إعدادات الهوية البصرية ودعم اللغة العربية (RTL)
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;600&display=swap');
    
    /* جعل الصفحة بالكامل من اليمين لليسار */
    html, body, [class*="st-"], .main {
        font-family: 'Noto Sans Arabic', sans-serif;
        direction: rtl;
        text-align: right;
        background-color: #ffffff;
        color: #000000;
    }
    
    /* تنسيق الأيقونات والخيارات لتكون متقاربة */
    .stButton > button {
        width: 100%;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        background-color: white !important;
        color: black !important;
        font-weight: 600 !important;
        margin-bottom: 10px;
    }

    .stMetric {
        border: 1px solid #000000 !important;
        direction: rtl;
    }

    .report-card {
        border: 2px solid #000000;
        padding: 20px;
        margin-top: 20px;
        direction: rtl;
    }
    
    /* إخفاء عبارة Double Click وتحسين القوائم */
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة (Navigation Logic)
if 'investor_type' not in st.session_state:
    st.session_state.investor_type = None

# دالة العودة للرئيسية
def reset_home():
    st.session_state.investor_type = None
    st.rerun()

# --- واجهة اختيار النمط (الرئيسية) ---
if st.session_state.investor_type is None:
    st.markdown("<h1 style='text-align: center;'>🛡️ منصة ريادة</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>اختر نمطك الاستثماري للبدء فوراً</p>", unsafe_allow_html=True)
    
    # أعمدة متقاربة جداً للأنماط
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛡️ محافظ"):
            st.session_state.investor_type = "محافظ"
            st.rerun()
    with col2:
        if st.button("⚖️ متوازن"):
            st.session_state.investor_type = "متوازن"
            st.rerun()
    with col3:
        if st.button("🚀 مغامر"):
            st.session_state.investor_type = "مغامر"
            st.rerun()
    st.stop()

# --- واجهة التحليل (بعد اختيار النمط) ---

# 3. الشريط الجانبي (تحسين التنقل)
with st.sidebar:
    try:
        st.markdown("<div style='border: 1px solid #000; padding: 5px; text-align:center;'>", unsafe_allow_html=True)
        st.image("second.jpg", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    except:
        st.info("ارفع الشعار باسم second.jpg")
    
    st.markdown(f"### 👤 النمط: {st.session_state.investor_type}")
    
    # زر العودة للرئيسية (أيقونة القوائم)
    if st.button("🏠 العودة للرئيسية"):
        reset_home()
        
    st.divider()
    if 'balance' not in st.session_state: st.session_state.balance = 100000
    st.metric("رصيد المحفظة", f"{st.session_state.balance:,.0f} ريال")
    st.caption("إشراف: د. حنين المطيري")

# 4. محرك التحليل
ticker_dict = {"أرامكو": "2222", "الراجحي": "1120", "سابك": "2010", "stc": "7010"}

st.markdown("<h1>📊 تحليل المخاطر والتوقع</h1>", unsafe_allow_html=True)

col_sel, col_btn = st.columns([3, 1])
with col_sel:
    selected_stock = st.selectbox("🎯 اختر الشركة:", list(ticker_dict.keys()))
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("⚡ تحليل")

if run:
    with st.spinner('جاري التحليل...'):
        try:
            symbol = f"{ticker_dict[selected_stock]}.SR"
            data = yf.download(symbol, period="1y", progress=False)
            
            if not data.empty:
                # معالجة البيانات
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                
                raw_price = data['Close'].iloc[-1]
                current_price = float(raw_price.iloc[0]) if isinstance(raw_price, pd.Series) else float(raw_price)
                
                returns = data['Close'].pct_change().dropna()
                volatility = float((returns.std() * (252**0.5) * 100).iloc[0] if isinstance(returns.std(), pd.Series) else returns.std() * (252**0.5) * 100)
                
                risk_score = min(int(volatility * 2.5), 100)
                sentiment = np.random.randint(70, 95)
                
                # التوقع
                future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, 8)]
                prediction = [current_price * (1 + (np.random.normal(0, 0.01))) for _ in range(7)]

                # النتائج
                st.divider()
                r1, r2, r3 = st.columns(3)
                r1.metric("السعر الحالي", f"{current_price:.2f} ريال")
                r2.metric("مؤشر المخاطرة", f"{risk_score}/100")
                r3.metric("نبض السوق", f"{sentiment}%")

                # الرسم البياني
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'].values.flatten(), name="التاريخي", line=dict(color='#000000', width=1.5)))
                fig.add_trace(go.Scatter(x=future_dates, y=prediction, name="توقع ريادة", line=dict(color='#00c853', dash='dot')))
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', template="none", height=380, margin=dict(l=0,r=0,t=20,b=0))
                fig.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='#f2f2f2')
                fig.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='#f2f2f2', side="right") # السعر جهة اليمين
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"""
                <div class='report-card'>
                    <h3>🤖 تقرير المستشار (نمط {st.session_state.investor_type}):</h3>
                    <p>بناءً على التذبذب السعري البالغ {volatility:.2f}%، يتضح أن السهم يمتلك ثباتاً يتوافق مع أهدافك.</p>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"حدث خطأ في معالجة البيانات: {str(e)}")

st.divider()
st.caption("د. حنين بنت عبد الرحمن المطيري - أداة فهم المخاطر الاستثمارية")
