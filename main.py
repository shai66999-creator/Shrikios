import streamlit as st
import streamlit.components.v1 as components

# הגדרת דף רחבה למקצוענים
st.set_page_config(page_title="Shay's Pro Terminal", layout="wide")

st.title("⚡ מסוף המסחר של שי")

# קלט סימול
ticker = st.text_input("הכנס סימול (למשל TSLA, IREN, NVDA):", "TSLA").upper()

if ticker:
    # הגרף המקצועי עם ממוצע 150 מובנה - הגרסה היציבה ביותר
    st.markdown(f"### 📈 גרף אסטרטגיה עבור {ticker} (MA 150 מובנה)")
    tv_url = f"https://s.tradingview.com/widgetembed/?symbol={ticker}&interval=D&theme=dark&style=1&studies=SMA%40tv-basicstudies&language=he_IL"
    components.iframe(tv_url, height=550)

    st.markdown("---")
    
    # מחשבון השורה התחתונה
    st.subheader(f"🔢 חישוב נקודות כניסה ויציאה")
    st.info("קח את המחיר והממוצע מהגרף למעלה ורשום אותם כאן:")
    
    col1, col2 = st.columns(2)
    with col1:
        price_now = st.number_input("מחיר המניה כרגע:", value=0.0, step=0.01)
    with col2:
        ma150_val = st.number_input("מחיר הממוצע 150 (SMA בגרף):", value=0.0, step=0.01)

    if ma150_val > 0:
        # חישוב סטופ לוס 2% מתחת לממוצע
        stop_loss = ma150_val * 0.98
        
        st.success(f"✅ **שורה תחתונה למסחר:**")
        st.write(f"הסטופ לוס המדויק (2% מתחת לממוצע) הוא: **{stop_loss:.2f}**")

        st.markdown("---")
        
        # מחשבון גודל פוזיציה
        st.subheader("💰 כמה מניות לקנות?")
        risk_amount = st.number_input("כמה דולרים אתה מוכן להפסיד בעסקה? (למשל 100):", value=50.0)
        
        if risk_amount > 0:
            # חישוב כמות מניות
            risk_per_share = abs(price_now - stop_loss)
            if risk_per_share > 0:
                shares_to_buy = int(risk_amount / risk_per_share)
                total_cost = shares_to_buy * price_now
                
                st.warning(f"💡 **המלצה:** כדי לסכן ${risk_amount}, עליך לקנות **{shares_to_buy}** מניות.")
                st.write(f"עלות העסקה הכוללת: **${total_cost:,.2f}**")

        # טבלת סיכום מהירה
        st.table({
            "פעולה": ["כניסה (לפי מחיר שוק)", "יציאה (Stop Loss)", "כמות מניות מומלצת"],
            "נתון": [f"${price_now:.2f}", f"${stop_loss:.2f}", f"{shares_to_buy}"]
        })

st.caption("נבנה עבור שי שריקי - אסטרטגיית ממוצע נע 150")
