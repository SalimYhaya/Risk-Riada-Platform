import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الهوية البصرية المتطورة
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; white-space: pre-wrap; background-color: #1e1e1e; 
        border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #00c853 !important; font-weight: bold; }
    .stMetric { background-color: #1c2128; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
    .recommendation-box { padding: 20px; border-radius: 15px; text-align: center; border: 2px solid; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; background-color: #262730; border: 1px solid #333; }
    html, body, [class*="st-"] { font-family: 'Segoe UI', Arial, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. قاعدة بيانات الشركات
ticker_data = {
    "أرامكو السعودية (2222)": "2222", "مصرف الراجحي (1120)": "1120",
    "سابك (2010)": "2010", "إس تي سي - stc (7010)": "7010",
    "الأهلي السعودي (1180)": "1180", "معادن (1211)": "1211"
}

# 3. الشريط الجانبي الثابت (الهوية)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=100)
    st.markdown("<h3 style='text-align: center;'>إشراف أكاديمي</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00c853;'><b>د. حنين بنت عبد الرحمن المطيري</b></p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### عن ريادة")
    st.caption("منصة تعليمية تحليلية تهدف لرفع الوعي بمخاطر الاستثمار في السوق السعودي باستخدام التقنيات الذكية.")

# 4. بناء الألسنة (Tabs) لتبسيط تجربة المستخدم
tab1, tab2, tab3 = st.tabs(["📊 لوحة التحليل", "🤖 المستشار الذكي (AI)", "📚 أكاديمية التعلم"])

# --- التبويب الأول: لوحة التحليل ---
with tab1:
    st.markdown("<h2 style='text-align: center; color: #00c853;'>التحليل المتقدم للمخاطر</h2>", unsafe_allow_html=True)
    
    col_sel, col_per = st.columns([2, 1])
    with col_sel:
        selection = st.selectbox("🎯 اختر الشركة:", list(ticker_data.keys()) + ["أدخل رمزاً مخصصاً..."])
    with col_per:
        period_label = st.select_slider("📅 الفترة:", options=["6 أشهر", "سنة", "سنتين"], value="سنة")
    
    period_map = {"6 أشهر": "6mo", "سنة": "1y", "سنتين": "2y"}
    ticker = ticker_data[selection] if selection != "أدخل رمزاً مخصصاً..." else st.text_input("الرمز (4 أرقام):").strip()

    if st.button("🚀 بدء التحليل الذكي"):
        if ticker:
            with st.spinner('جاري معالجة البيانات...'):
                df = yf.download(f"{ticker}.SR", period=period_map[period_label], progress=False)
                if not df.empty:
                    curr_price = float(df['Close'].iloc[-1])
                    df['Returns'] = df['Close'].pct_change()
                    volatility = df['Returns'].std() * (252**0.5) * 100
                    risk_score = min(int(volatility * 2.5), 100)
                    
                    # مؤشر RSI
                    delta = df['Close'].diff(); up = delta.clip(lower=0); down = -1 * delta.clip(upper=0)
                    ema_up = up.ewm(com=13, adjust=False).mean(); ema_down = down.ewm(com=13, adjust=False).mean()
                    rsi = 100 - (100 / (1 + (ema_up / (ema_down + 1e-10)).iloc[-1]))

                    # التوصية
                    if risk_score < 40 and rsi < 70: rec, color = "شراء استثماري", "#00c853"
                    elif risk_score > 65 or rsi > 80: rec, color = "تجنب / بيع", "#ff4b4b"
                    else: rec, color = "مراقبة / انتظار", "#ffa500"

                    # العرض
                    c1, c2 = st.columns(2)
                    with c1: st.metric("السعر الحالي", f"{curr_price:.2f} ريال")
                    with c2: st.markdown(f"<div class='recommendation-box' style='border-color: {color}; color: {color};'><h3>{rec}</h3></div>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    c3, c4, c5 = st.columns(3)
                    c3.metric("درجة المخاطرة", f"{risk_score}/100")
                    c4.metric("التذبذب", f"{volatility:.1f}%")
                    c5.metric("قوة الاتجاه (RSI)", f"{rsi:.1f}")

                    fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], line=dict(color='#00c853'))])
                    fig.update_layout(template="plotly_dark", title="مسار السهم التاريخي", height=400)
                    st.plotly_chart(fig, use_container_width=True)

# --- التبويب الثاني: الشات بوت ---
with tab2:
    st.markdown("<h2 style='text-align: center; color: #00c853;'>خبير ريادة الذكي</h2>", unsafe_allow_html=True)
    st.write("اسألني عن الاستثمار في السوق السعودي، أو كيف أفهم نتائج التحليل.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("كيف أحمي استثماري من المخاطر؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = "بناءً على تساؤلك، أنصحك دائماً بتوزيع محفظتك الاستثمارية (Diversification) وعدم وضع السيولة في سهم واحد مرتفع المخاطرة. في منصة ريادة، نعتبر أي سهم يتجاوز تقييمه 70/100 هو سهم عالي المخاطرة يحتاج حذراً شديداً."
            if "أرامكو" in prompt: response = "سهم أرامكو يُصنف غالباً ضمن الأسهم قليلة التذبذب وذات العوائد المستقرة، وهو مناسب للاستثمار طويل الأجل."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- التبويب الثالث: الأكاديمية ---
with tab3:
    st.markdown("<h2 style='text-align: center; color: #00c853;'>أكاديمية ريادة للوعي المالي</h2>", unsafe_allow_html=True)
    
    col_edu1, col_edu2 = st.columns(2)
    with col_edu1:
        with st.expander("❓ ما هي مخاطر التذبذب؟"):
            st.write("التذبذب يقيس مدى سرعة وقوة تغير سعر السهم. السهم الذي يقفز ويهبط بعنف هو سهم 'عالي التذبذب'، وبالتالي مخاطرته مرتفعة.")
        with st.expander("📈 كيف أقرأ مؤشر RSI؟"):
            st.write("مؤشر القوة النسبية (RSI) يتراوح من 0 إلى 100. فوق 70 يعني السهم 'مشبع شراء' وقد ينخفض سعره. تحت 30 يعني 'مشبع بيع' وقد يرتفع سعره.")
    
    with col_edu2:
        with st.expander("🇸🇦 دليل المبتدئ في تداول"):
            st.write("السوق السعودي (تداول) هو الأكبر في المنطقة. ابدأ دائماً بأسهم العوائد (القيادية) قبل الدخول في أسهم المضاربة.")
        with st.expander("🛡️ استراتيجية تقليل المخاطر"):
            st.write("1. التويع القطاعي. 2. الاستثمار على دفعات. 3. متابعة مؤشر المخاطرة في منصة ريادة بانتظام.")

    st.image("https://images.unsplash.com/photo-1611974717482-98252c00ed31?auto=format&fit=crop&q=80&w=1000", caption="التحليل المالي هو لغة الأرقام")
