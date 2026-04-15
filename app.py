import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الهوية البصرية (الستايل الاحترافي)
st.set_page_config(page_title="ريادة لمخاطر الاستثمار", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. العنوان الجانبي (الإشراف)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50) # أيقونة رمزية
st.sidebar.write("### إشراف")
st.sidebar.info("د. حنين بنت عبد الرحمن المطيري")
st.sidebar.divider()
st.sidebar.write("⚠️ **غرض التجربة:** بحث علمي وبرمجي فقط")

# 3. الهيدر الرئيسي
st.title("🛡️ منصة ريادة لمخاطر الاستثمار")
st.subheader("تحليل ذكي للسوق السعودي (TASI) باستخدام تقنيات النمذجة المالية")

# 4. منطقة المدخلات
col_input, col_info = st.columns([1, 2])
with col_input:
    ticker = st.text_input("أدخل رمز الشركة (مثلاً 2222 لأرامكو):", value="2222")
    start_analysis = st.button("تحليل المخاطر الآن")

# 5. منطق المعالجة (عند الضغط على الزر)
if start_analysis:
    with st.spinner('جاري تحليل البيانات التاريخية ونمذجة المخاطر...'):
        try:
            full_ticker = f"{ticker}.SR"
            # جلب البيانات
            data = yf.download(full_ticker, period="1y")
            
            if data.empty:
                st.error("عذراً، لم يتم العثور على بيانات لهذه الشركة. تأكد من الرمز.")
            else:
                # حساب العوائد والتذبذب
                data['Returns'] = data['Close'].pct_change()
                volatility = data['Returns'].std() * (252**0.5) * 100
                
                # حساب درجة المخاطرة (معادلة تجريبية)
                risk_score = min(int(volatility * 2.5), 100)
                
                # عرض النتائج
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("درجة المخاطرة العامة", f"{risk_score}/100")
                m2.metric("مستوى التذبذب السنوي", f"{volatility:.2f}%")
                m3.metric("حالة المخاطرة", "مرتفعة" if risk_score > 60 else "متوسطة" if risk_score > 30 else "منخفضة")

                # رسم بياني تفاعلي
                fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], line=dict(color='#00c853'))])
                fig.update_layout(title=f"أداء سهم {ticker} خلال العام الأخير", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")

else:
    st.info("الرجاء إدخال رمز الشركة والضغط على زر التحليل للبدء.")