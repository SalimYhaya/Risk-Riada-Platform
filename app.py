import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. الإعدادات البصرية الفخمة (العودة للهوية الأولى مع لمسة عصرية)
st.set_page_config(page_title="منصة ريادة | الاستثمار الذكي", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #00c853; }
    .report-card { background-color: #1c2128; padding: 30px; border-radius: 15px; border-right: 5px solid #00c853; margin: 20px 0; }
    .edu-card { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #333; height: 100%; }
    h1, h2 { color: #00c853 !important; font-weight: 800; }
    html, body, [class*="st-"] { font-family: 'Segoe UI', Arial, sans-serif; }
    .source-btn { background-color: #333; color: #00c853; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# 2. البيانات الأساسية
ticker_data = {
    "أرامكو السعودية (2222)": "2222", "مصرف الراجحي (1120)": "1120",
    "سابك (2010)": "2010", "إس تي سي (7010)": "7010",
    "البنك الأهلي (1180)": "1180", "معادن (1211)": "1211",
    "كهرباء السعودية (5110)": "5110", "مجموعة تداول (1111)": "1111"
}

# 3. الشريط الجانبي (الهوية الأكاديمية الثابتة)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=110)
    st.markdown("### إشراف أكاديمي")
    st.success("د. حنين بنت عبد الرحمن المطيري")
    st.divider()
    st.write("🌐 **المصادر الرسمية المعتمدة:**")
    st.markdown("- [هيئة السوق المالية](https://cma.org.sa)")
    st.markdown("- [تداول السعودية](https://www.sauditadawul.com.sa)")
    st.divider()
    st.caption("منصة ريادة v5.0 - تحليل المخاطر المبني على البيانات")

# 4. واجهة المستخدم الرئيسية
st.markdown("<h1 style='text-align: center;'>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #8b949e;'>مركز التحليل الذكي والوعي المالي للسوق السعودي</p>", unsafe_allow_html=True)

# القسم الأول: التحكم والمدخلات
st.markdown("### 🔍 أداة التحليل الفوري")
col_a, col_b, col_c = st.columns([2, 1, 1])
with col_a:
    selection = st.selectbox("اختر الشركة المستهدفة:", list(ticker_data.keys()) + ["إدخال رمز يدوي..."])
with col_b:
    period = st.selectbox("الفترة الزمنية:", ["6 أشهر", "سنة", "سنتين"], index=1)
with col_c:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 تحليل الآن", use_container_width=True)

ticker = ticker_data[selection] if selection != "إدخال رمز يدوي..." else st.text_input("الرمز (4 أرقام):")

# 5. منطق المعالجة والظهور الديناميكي
if analyze_btn:
    if ticker:
        with st.spinner('جاري استدعاء البيانات من تداول وتحليل المخاطر...'):
            full_ticker = f"{ticker}.SR"
            period_code = {"6 أشهر": "6mo", "سنة": "1y", "سنتين": "2y"}[period]
            df = yf.download(full_ticker, period=period_code, progress=False)
            
            if not df.empty:
                # الحسابات
                price = df['Close'].iloc[-1]
                vol = df['Close'].pct_change().std() * (252**0.5) * 100
                risk = min(int(vol * 2.5), 100)
                
                # النتائج الرئيسية
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("السعر الحالي", f"{price:.2f} ريال")
                m2.metric("مؤشر المخاطرة", f"{risk}/100")
                m3.metric("مستوى التذبذب", f"{vol:.1f}%")

                # الرسم البياني
                fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], line=dict(color='#00c853', width=2))])
                fig.update_layout(template="plotly_dark", height=350, title=f"تحرك السهم خلال {period}")
                st.plotly_chart(fig, use_container_width=True)

                # --- التحديث الجوهري: التقرير الذكي بدلاً من الشات بوت التقليدي ---
                st.markdown("### 🤖 تقرير خبير ريادة (AI Insight)")
                
                # تحديد الحالة للتوصية
                status = "آمن نسبياً" if risk < 45 else "عالي المخاطرة" if risk > 70 else "متوسط المخاطرة"
                color = "#00c853" if risk < 45 else "#ff4b4b" if risk > 70 else "#ffa500"
                
                st.markdown(f"""
                <div class='report-card'>
                    <h4>التحليل الفني والأساسي للرمز {ticker}:</h4>
                    <p>بناءً على البيانات التاريخية لفترة <b>{period}</b>، يظهر السهم حالة <b><span style='color:{color}'>{status}</span></b>.</p>
                    <ul>
                        <li><b>إدارة المخاطر:</b> التذبذب السعري الحالي ({vol:.1f}%) يتطلب استراتيجية استثمارية حذرة وفقاً لمعايير <b>هيئة السوق المالية</b>.</li>
                        <li><b>التوصية:</b> { 'ينصح بالتعزيز في المحفظة للمستثمر طويل الأجل.' if risk < 45 else 'ينصح بجني الأرباح أو الانتظار خارج السهم حالياً.' if risk > 70 else 'السهم مناسب للمضاربة اليومية بحذر.' }</li>
                        <li><b>مصادر موثوقة:</b> يمكنك مراجعة القوائم المالية الرسمية عبر موقع <a class='source-btn' href='https://www.sauditadawul.com.sa' target='_blank'>تداول السعودية</a> لضمان دقة قرارك.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# 6. القسم التعليمي (أكاديمية ريادة) - متاح دائماً في الأسفل
st.divider()
st.markdown("### 📚 أكاديمية ريادة للوعي الاستثماري")
e1, e2, e3 = st.columns(3)

with e1:
    st.markdown("""<div class='edu-card'>
    <h4>📈 ما هي المخاطرة؟</h4>
    <p>هي احتمالية انحراف العائد الفعلي عن العائد المتوقع. في منصتنا، نستخدم "الانحراف المعياري" لقياس هذا الاحتمال بدقة.</p>
    </div>""", unsafe_allow_html=True)

with e2:
    st.markdown("""<div class='edu-card'>
    <h4>⚖️ تنويع المحفظة</h4>
    <p>وفقاً لمبادئ الاستثمار الآمن، لا تضع أكثر من 15% من رأس مالك في سهم واحد يتجاوز مؤشر مخاطرته 60.</p>
    </div>""", unsafe_allow_html=True)

with e3:
    st.markdown("""<div class='edu-card'>
    <h4>🔗 مصادر التعلم</h4>
    <p>تفضل بزيارة مركز الوعي الاستثماري التابع لهيئة السوق المالية <a href='https://investsmart.org.sa/' target='_blank'>من هنا</a>.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#555;'>تم التطوير لدعم البحث العلمي والوعي المالي بالتعاون مع د. حنين المطيري</p>", unsafe_allow_html=True)
