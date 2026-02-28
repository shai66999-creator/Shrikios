import streamlit as st
import streamlit.components.v1 as components

# הגדרה בסיסית ביותר ללא עיצובים מורכבים
st.set_page_config(page_title="Shay Terminal")

st.header("⚡ מסוף המסחר של שי")

# קלט סימול
ticker = st.text_input("הכנס סימול (למשל TSLA):", "TSLA").upper()

if ticker:
    # גרף בסיסי - הוספתי רווחים כדי למנוע התנגשות עם שגיאות
    st.write(f"---")
    st.subheader(f"📈 גרף {ticker} (MA 150)")
    tv_url = f"https://s.tradingview.com/widgetembed/?symbol={ticker}&interval=D&theme=dark&style=1&studies=SMA%40tv-basicstudies&language=he_IL"
    components.iframe(tv_url, height=400)

    st.write(f"---")
    
    # מחשבון פשוט - ללא עמודות (Columns) כדי למנוע שגיאות תצוגה
    st.subheader("🔢 מחשבון אסטרטגיה")
    
    price_now = st.number_input("מחיר המניה כרגע:", value=0.0, step=0.01)
    ma150_val = st.number_input("מחיר הממוצע 150 מהגרף:", value=0.0, step=0.01)

    if ma150_val > 0:
        # חישוב סטופ לוס 2% מתחת לממוצע
        stop_loss = ma150_val * 0.98
        st.error(f"📍 סטופ לוס (2% מתחת לממוצע): {stop_loss:.2f}")

        st.write(f"---")
        
        # מחשבון כמות מניות פשוט
        st.subheader("💰 כמות לקנייה")
        risk_amount = st.number_input("כמה דולרים להסתכן בעסקה?", value=50.0)
        
        risk_per_share = abs(price_now - stop_loss)
        if risk_per_share > 0:
            shares = int(risk_amount / risk_per_share)
            st.success(f"✅ המלצה: קנה {shares} מניות")
            st.info(f"עלות כוללת: ${shares * price_now:,.2f}")

st.caption("אסטרטגיית ממוצע 150 - שי שריקי")
