import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الهوية البصرية (العودة للألوان الأصلية والخطوط الواضحة)
st.set_page_config(page_title="منصة ريادة للمخاطر", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333; }
    .header-text { text-align: center; color: #00c853; font-weight: bold; font-size: 2.5rem; }
    .recommendation-box { padding: 20px; border-radius: 15px; text-align: center; margin-top: 10px; border-width: 2px; border-style: solid; }
    html, body, [class*="st-"] { font-family: 'Arial', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. قاعدة بيانات الشركات
ticker_data = {
    "أرامكو السعودية (2222)": "2222",
    "مصرف الراجحي (1120)": "1120",
    "سابك (2010)": "2010",
    "إس تي سي - stc (7010)": "7010",
    "الأهلي السعودي (1180)": "1180",
    "معادن (1211)": "1211",
    "كهرباء السعودية (5110)": "5110",
    "مجموعة تداول (1111)": "1111",
    "جرير (4190)": "4190",
    "المراعي (2280)": "2280"
}

# 3. الشريط الجانبي (الإشراف الأكاديمي)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=110)
    st.markdown("<h3 style='text-align: center;'>إشراف أكاديمي</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00c853; font-weight: bold; font-size: 1.1rem;'>سعادة الدكتورة<br>حنين بنت عبد الرحمن المطيري</p>", unsafe_allow_html=True)
    st.divider()
    st.info("📊 **مهمة المنصة:** قياس وتحليل مخاطر الأوراق المالية باستخدام تقنيات تعلم الآلة والتحليل الكمي.")

# 4. العنوان الرئيسي
st.markdown("<h1 class='header-text'>🛡️ منصة ريادة لمخاطر الاستثمار</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>التحليل الذكي للأمان المالي في السوق السعودي</p>", unsafe_allow_html=True)
st.divider()

# 5. منطقة التحكم واختيار الشركة
col_sel, col_btn = st.columns([3, 1])
with col_sel:
    selection = st.selectbox("🎯 اختر الشركة للتحليل:", list(ticker_data.keys()) + ["أدخل رمزاً مخصصاً..."])

# تحديد الرمز (Ticker)
if selection == "أدخل رمزاً مخصصاً...":
    ticker_input = st.text_input("أدخل الرمز (4 أرقام):")
    ticker = ticker_input.strip()
else:
    ticker = ticker_data[selection]

st.markdown("<br>", unsafe_allow_html=True)
start_analysis = st.button("🚀 تشغيل المحرك التحليلي")

# 6. منطق المعالجة والنتائج (إصلاح الخطأ Ambiguous Truth Value)
if start_analysis:
    if ticker:
        with st.spinner('جاري سحب البيانات اللحظية وتحليل المخاطر...'):
            try:
                full_ticker = f"{ticker}.SR"
                # استخدام yfinance لجلب البيانات
                stock_obj = yf.Ticker(full_ticker)
                df = stock_obj.history(period="1y")
                
                # الإصلاح هنا: التحقق باستخدام df.empty
                if df.empty:
                    st.error("❌ عذراً، لم نتمكن من العثور على بيانات لهذه الشركة. تأكد من الرمز.")
                else:
                    # حسابات السعر والمخاطرة
                    current_price = float(df['Close'].iloc[-1])
                    df['Returns'] = df['Close'].pct_change()
                    volatility = df['Returns'].std() * (252**0.5) * 100
                    risk_score = min(int(volatility * 2.5), 100)
                    
                    # مؤشر RSI بسيط لاتخاذ القرار
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0)
                    down = -1 * delta.clip(upper=0)
                    ema_up = up.ewm(com=13, adjust=False).mean()
                    ema_down = down.ewm(com=13, adjust=False).mean()
                    rs = ema_up / ema_down
                    rsi = 100 - (100 / (1 + rs.iloc[-1]))

                    # منطق التوصية الذكية
                    if risk_score < 40 and rsi < 70:
                        rec, color = "توصية: شراء استثماري", "#00c853"
                    elif risk_score > 65 or rsi > 80:
                        rec, color = "توصية: تجنب / بيع", "#ff4b4b"
                    else:
                        rec, color = "توصية: مراقبة / انتظار", "#ffa500"

                    # عرض النتائج (الواجهة المحسنة)
                    st.markdown(f"### 📊 نتائج التحليل لـ: {selection.split('(')[0]}")
                    
                    # الصف الأول: السعر والتوصية
                    res_c1, res_c2 = st.columns([1, 1])
                    with res_c1:
                        st.metric("السعر الحالي للسهم", f"{current_price:.2f} ريال")
                    with res_c2:
                        st.markdown(f"<div class='recommendation-box' style='border-color: {color};'>"
                                    f"<h2 style='color: {color}; margin: 0;'>{rec}</h2>"
                                    f"</div>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # الصف الثاني: تفاصيل المخاطرة
                    res_c3, res_c4, res_c5 = st.columns(3)
                    res_c3.metric("مؤشر المخاطرة", f"{risk_score}/100")
                    res_c4.metric("تذبذب السهم السنوي", f"{volatility:.1f}%")
                    res_c5.metric("قوة الاتجاه (RSI)", f"{rsi:.1f}")

                    # الرسم البياني
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='سعر الإغلاق', line=dict(color='#00c853', width=2.5)))
                    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=10, r=10, t=50, b=10),
                                      title="الأداء السعري خلال العام الأخير", xaxis_title="التاريخ", yaxis_title="السعر (ريال)")
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"حدث خطأ فني أثناء التحليل: {e}")
