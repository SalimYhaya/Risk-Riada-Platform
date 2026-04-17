import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الواجهة
st.set_page_config(page_title="منصة ريادة المطورة", layout="wide", page_icon="🛡️")

# 2. مراجع ومصادر موثوقة (Knowledge Base)
TRUSTED_SOURCES = {
    "هيئة السوق المالية": "https://cma.org.sa",
    "تداول السعودية": "https://www.sauditadawul.com.sa",
    "مركز الوعي المالي (مستثمر)": "https://www.monshaat.gov.sa"
}

# 3. تحسين التصميم (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1c2128; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    .recommendation-box { padding: 20px; border-radius: 15px; text-align: center; border: 2px solid; }
    .source-link { color: #00c853; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. محرك البيانات (Data Engine)
ticker_data = {
    "أرامكو السعودية (2222)": "2222", "مصرف الراجحي (1120)": "1120",
    "سابك (2010)": "2010", "إس تي سي - stc (7010)": "7010"
}

# 5. التبويبات (Tabs)
tab1, tab2, tab3 = st.tabs(["📊 التحليل المتقدم", "🤖 مستشار ريادة الذكي", "📚 المصادر والمراجع"])

# --- التبويب الأول: التحليل (نفس المنطق السابق مع تحسين السحب) ---
with tab1:
    col_sel, col_per = st.columns([2, 1])
    with col_sel: selection = st.selectbox("🎯 اختر الشركة:", list(ticker_data.keys()))
    with col_per: period_label = st.select_slider("📅 الفترة:", options=["6 أشهر", "سنة"])
    
    ticker = ticker_data[selection]
    if st.button("🚀 تحليل البيانات"):
        df = yf.download(f"{ticker}.SR", period="1y", progress=False)
        if not df.empty:
            # (نفس الحسابات السابقة للمخاطرة والسعر)
            curr_price = float(df['Close'].iloc[-1])
            vol = df['Close'].pct_change().std() * (252**0.5) * 100
            risk = min(int(vol * 2.5), 100)
            
            # حفظ النتائج في Session State ليراها الشات بوت
            st.session_state['last_analysis'] = {
                'name': selection, 'price': curr_price, 'risk': risk, 'vol': vol
            }
            
            st.metric("السعر الحالي", f"{curr_price:.2f} ريال")
            st.metric("درجة المخاطرة", f"{risk}/100")
            st.plotly_chart(go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], line=dict(color='#00c853'))]))

# --- التبويب الثاني: المستشار الذكي (الربط مع البيانات) ---
with tab2:
    st.markdown("### 🤖 خبير الاستثمار المعتمد على البيانات")
    
    # التحقق من وجود تحليل سابق ليعطي الشات بوت إجابات دقيقة
    analysis = st.session_state.get('last_analysis', None)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "مرحباً بك! أنا مستشارك الذكي. قم بتحليل سهم أولاً وسأعطيك تقريراً مفصلاً عنه."}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن المخاطر أو السهم المختار..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # منطق إجابة ذكي بناءً على السياق (Context-Aware)
            if analysis and ("هذا السهم" in prompt or "رأيك" in prompt or "تحليل" in prompt):
                response = f"""بناءً على أحدث بيانات **{analysis['name']}**:
                \n- السعر الحالي هو {analysis['price']:.2f} ريال.
                \n- درجة المخاطرة هي {analysis['risk']}/100.
                \n- نصيحتي: السهم حالياً يظهر تذبذباً بنسبة {analysis['vol']:.1f}%. إذا كنت مستثمراً متحفظاً، ابحث عن درجة مخاطرة أقل من 40."""
            elif "مخاطرة" in prompt:
                response = "المخاطرة في السوق السعودي تُقاس بمدى انحراف السعر عن متوسطه. نعتمد في 'ريادة' على معايير تقلبات الأسعار التاريخية المتوافقة مع نماذج إدارة المخاطر العالمية."
            else:
                response = "أعتذر، أحتاج منك تحليل سهم معين أولاً عبر تبويب (التحليل) لكي أتمكن من إعطائك إجابة دقيقة مرتبطة بالبيانات اللحظية."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- التبويب الثالث: المصادر والمراجع (الربط مع جهات موثوقة) ---
with tab3:
    st.markdown("## 📚 مراجع الاستثمار الآمن")
    st.write("للحصول على معلومات رسمية ودقيقة، ننصح بمتابعة المصادر التالية:")
    
    col_src1, col_src2 = st.columns(2)
    with col_src1:
        st.markdown(f"### 🏛️ جهات تنظيمية")
        for name, url in TRUSTED_SOURCES.items():
            st.markdown(f"- [{name}]({url})")
            
    with col_src2:
        st.markdown("### 📄 كتيبات توعوية (PDF)")
        st.write("1. دليل المستثمر الذكي - هيئة السوق المالية")
        st.write("2. لائحة سلوكيات السوق")
        st.write("3. مبادئ الاستثمار في الصناديق")

    st.divider()
    st.warning("⚠️ **تنبيه:** جميع تحليلات الشات بوت هي استرشادية بناءً على خوارزميات المنصة ولا تعد توصية مباشرة بالشراء أو البيع.")
