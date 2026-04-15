import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الهوية البصرية (Professional Dark Mode)
st.set_page_config(page_title="ريادة لمخاطر الاستثمار", layout="wide", page_icon="🛡️")

# تخصيص التصميم عبر CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; transition: transform 0.3s; }
    .stMetric:hover { transform: scale(1.05); border-color: #00c853; }
    .sidebar .sidebar-content { background-image: linear-gradient(180deg, #1e1e1e 0%, #0e1117 100%); }
    h1, h2, h3 { color: #00c853 !important; }
    .stSelectbox label, .stTextInput label { color: #fff !important; font-weight: bold; }
    div[data-testid="stExpander"] { background-color: #1e1e1e; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة المحددة للشركات السعودية (Top 10)
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

# إضافة خيار الإدخال اليدوي
ticker_options = list(ticker_dict.keys())
ticker_options.append("أدخل رمز شركة أخرى يدوياً...")

# 3. الشريط الجانبي (الإشراف الأكاديمي - أيقونة أنثوية)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    # رابط صورة أيقونة أنثوية احترافية (طبيبة/باحثة)
    col_avatar_1, col_avatar_2, col_avatar_3 = st.columns([1, 2, 1])
    with col_avatar_2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=100) # أيقونة أنثوية
    
    st.markdown("<h3 style='text-align: center; color: white !important;'>إشراف أكاديمي</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #00c853;'><b>سعادة الدكتورة<br>حنين بنت عبد الرحمن المطيري</b></p>", unsafe_allow_html=True)
    st.divider()
    st.warning("⚠️ **غرض التجربة:** هذه المنصة هي مشروع بحثي برمجى وتجريبي فقط لاختبار قدرات النمذجة المالية الذكية.")
    st.info("💡 **كيف تعمل؟** نقوم بتحليل التذبذب السعري ومعاملات المخاطرة بناءً على بيانات تاريخية للسهم خلال عام كامل.")

# 4. الهيدر الرئيسي للمنصة
st.markdown("<h1 style='text-align: center;'>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white !important;'>الذكاء الاصطناعي في خدمة المستثمر السعودي</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>تحليل متقدم واستشراف لمخاطر الأوراق المالية في السوق السعودي (تداول) بناءً على النماذج الكمية.</p>", unsafe_allow_html=True)
st.divider()

# 5. منطقة اختيار الشركة (قائمة منسدلة + إدخال يدوي)
col_sel, col_empty = st.columns([2, 1])
with col_sel:
    selected_option = st.selectbox("اختر الشركة لتحليل مخاطرها:", ticker_options)

# منطق تحديد الرمز النهائي (Ticker)
if selected_option == "أدخل رمز شركة أخرى يدوياً...":
    manual_ticker = st.text_input("أدخل رمز الشركة المكون من 4 أرقام (مثلاً 4003):", placeholder="أدخل الرمز هنا")
    ticker = manual_ticker.strip()
else:
    ticker = ticker_dict[selected_option]

start_analysis = st.button("🚀 ابدأ تحليل المخاطر الآن")

# 6. منطق المعالجة (عند الضغط على الزر)
if start_analysis:
    if not ticker or not ticker.isdigit() or len(ticker) != 4:
        st.error("❌ الرجاء إدخال رمز شركة سعودي صحيح مكون من 4 أرقام.")
    else:
        with st.spinner('جاري سحب البيانات اللحظية وتحليل الأنماط التاريخية للمخاطر...'):
            try:
                full_ticker = f"{ticker}.SR"
                # جلب البيانات لآخر سنة
                data = yf.download(full_ticker, period="1y", progress=False)
                
                if data.empty:
                    st.error("عذراً، لم يتم العثور على بيانات لهذه الشركة. تأكد من الرمز.")
                else:
                    # حساب العوائد اليومية
                    data['Returns'] = data['Close'].pct_change()
                    
                    # حساب التذبذب السنوي (Volatility)
                    volatility = data['Returns'].std() * (252**0.5) * 100
                    
                    # حساب درجة المخاطرة (معادلة تجريبية مبدئية)
                    risk_score = min(int(volatility * 2.5), 100)
                    
                    # تحديد حالة المخاطرة بناءً على الدرجة
                    if risk_score > 70:
                        risk_status = "مرتفعة جداً"
                        risk_color = "#FF4B4B" # أحمر
                    elif risk_score > 40:
                        risk_status = "متوسطة"
                        risk_color = "#FFA500" # برتقالي
                    else:
                        risk_status = "منخفضة"
                        risk_color = "#00c853" # أخضر

                    # عرض النتائج في بطاقات (Metrics)
                    st.divider()
                    st.markdown(f"<h2>النتائج التحليلية لرمز الشركة: {ticker}</h2>", unsafe_allow_html=True)
                    m1, m2, m3 = st.columns(3)
                    
                    with m1:
                        st.metric("درجة المخاطرة العامة", f"{risk_score}/100", help="درجة تقديرية للمخاطرة بناءً على تذبذب السهم.")
                    with m2:
                        st.metric("مستوى التذبذب السنوي", f"{volatility:.2f}%", help="قياس لمدى تقلب سعر السهم عن متوسطه التاريخي.")
                    with m3:
                        st.markdown(f"<div class='stMetric' style='text-align: center;'><p style='font-size:1.1em;'>حالة المخاطرة المقدرة</p><h2 style='color: {risk_color} !important; font-weight: bold;'>{risk_status}</h2></div>", unsafe_allow_html=True)

                    # رسم بياني تفاعلي (Plotly)
                    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], line=dict(color='#00c853', width=2))])
                    fig.update_layout(
                        title=f"الأداء التاريخي لسعر سهم {ticker} خلال العام الأخير",
                        xaxis_title="التاريخ",
                        yaxis_title="سعر الإغلاق (ريال)",
                        template="plotly_dark",
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # تنويه إخلاء المسؤولية
                    with st.expander("📝 إخلاء مسؤولية"):
                        st.markdown("""
                        البيائج والمعلومات المعروضة هي نتيجة نمذجة برمجية مبنية على بيانات تاريخية للسهم. 
                        لا تعتبر هذه النتائج نصيحة استثمارية أو دعوة للشراء أو البيع. 
                        السوق المالي السعودي (تداول) يتأثر بعوامل متعددة لا يمكن التنبؤ بها جميعاً، والمنصة تخلي مسؤوليتها عن أي قرارات تتخذ بناءً على هذه المخرجات.
                        """)
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("💡 الرجاء اختيار الشركة من القائمة أو إدخال رمزها، ثم اضغط على زر التحليل للبدء.")
