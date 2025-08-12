import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.title("מדידת אורך מקווים בתוכנית 📐")

uploaded_file = st.file_uploader("העלה תוכנית (תמונה או PDF)", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="התוכנית שלך", use_column_width=True)

    st.subheader("קביעת קנה מידה")
    pixel_length = st.number_input("אורך בקווים (פיקסלים)", min_value=1.0)
    real_length = st.number_input("אורך אמיתי (מטרים)", min_value=0.01)
    if pixel_length and real_length:
        scale = real_length / pixel_length
        st.success(f"קנה מידה: {scale:.4f} מטר לפיקסל")

        st.subheader("שרטט קווים למדידה")
        st.markdown("⚠️ בגרסה בסיסית זו, אין ציור אינטראקטיבי. נדרש פיתוח נוסף עם canvas או JS.")

        lines = st.text_area("הזן קואורדינטות של קווים (x1,y1,x2,y2) בשורות נפרדות")
        total_pixels = 0
        if lines:
            for line in lines.strip().split("\n"):
                try:
                    x1, y1, x2, y2 = map(int, line.strip().split(","))
                    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    total_pixels += length
                except:
                    st.error(f"שורה לא תקינה: {line}")

            total_meters = total_pixels * scale
            st.success(f"אורך כולל: {total_meters:.2f} מטר")
