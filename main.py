import streamlit as st
import streamlit.components.v1 as components

# הגדרת דף רחבה למקצוענים
st.set_page_config(page_title="Shay's Pro Terminal", layout="wide")

st.title("⚡ מסוף המסחר המהיר של שי")

# חלק 1: קלט סימול
ticker = st.text_input("הכנס סימול (למשל TSLA, IREN, NVDA):", "TSLA").upper()

if ticker:
    # פיצ'ר הלוגו והמחיר החי
    st.markdown(f"### 🏷️ כרטיס מניה חי: {ticker}")
    ticker_widget = f"""
    <div style="height:160px;">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
    {{
      "symbol": "{ticker}",
      "width": "100%",
      "colorTheme": "dark",
      "isTransparent": false,
      "locale": "he_IL"
    }}
    </script>
    </div>
    """
    components.html(ticker_widget, height=170)

    # הגרף המקצועי עם ממוצע 150 מובנה
    st.markdown("### 📈 גרף אסטרטגיה (MA 150 מובנה)")
    tv_url = f"https://s.tradingview.com/widgetembed/?symbol={ticker}&interval=D&theme=dark&style=1&studies=SMA%40tv-basicstudies&language=he_IL"
    components.iframe(tv_url, height=550)

    st.markdown("---")
    
    # חלק 2: מחשבון השורה התחתונה
    st.subheader(f"🔢 חישוב נקודות כניסה ויציאה עבור {ticker}")
    st.info("קח את המספרים שמופיעים למעלה ורשום אותם כאן:")
    
    col1, col2 = st.columns(2)
    with col1:
        price_now = st.number_input("מחיר המניה כרגע (מהכרטיס למעלה):", value=0.0, step=0.01)
    with col2:
        ma150_val = st.number_input("מחיר הממוצע 150 (SMA בגרף):", value=0.0, step=0.01)

    if ma150_val > 0:
        # חישוב סטופ לוס 2% מתחת לממוצע
        stop_loss = ma150_val * 0.98
        
        st.success(f"✅ **שורה תחתונה למסחר:**")
        st.write(f"מחיר המניה היום הוא **{price_now:.2f}** והממוצע 150 הוא **{ma150_val:.2f}**.")
        st.error(f"במקרה ואתה נכנס לעסקה, המחיר שאתה יוצא (סטופ לוס) הוא: **{stop_loss:.2f}**.")

        st.markdown("---")
        
        # חלק 3: פיצ'ר חדש - מחשבון כמות מניות (Position Sizing)
        st.subheader("💰 מחשבון גודל פוזיציה")
        risk_amount = st.number_input("כמה דולרים אתה מוכן להפסיד בעסקה הזו? (למשל 100):", value=50.0)
        
        if risk_amount > 0:
            # חישוב: סיכון למניה אחת
            risk_per_share = ma150_val - stop_loss
            # חישוב: כמות מניות לקנייה
            shares_to_buy = int(risk_amount / risk_per_share)
            total_cost = shares_to_buy * ma150_val
            
            st.warning(f"💡 **המלצת כמות:** כדי לסכן ${risk_amount}, עליך לקנות **{shares_to_buy}** מניות.")
            st.write(f"עלות העסקה הכוללת: **${total_cost:,.2f}**")

        # טבלת פקודה מהירה
        st.table({
            "פעולה": ["כניסה (Limit)", "יציאה (Stop Loss)", "כמות מניות"],
            "נתון": [f"${ma150_val:.2f}", f"${stop_loss:.2f}", f"{shares_to_buy}"]
        })

st.caption("נבנה עבור שי שריקי - אסטרטגיית ממוצע נע 150")