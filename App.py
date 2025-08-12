import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
from streamlit_drawable_canvas import st_canvas
import math
import io

st.set_page_config(page_title="מדידת קווים לפי קנה מידה", layout="wide")
st.title("📐 מדידת קווים לפי קנה מידה מתוך תמונה או PDF")

uploaded_file = st.file_uploader("📎 העלה תמונה או PDF", type=["jpg", "png", "pdf"])
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = pdf_doc.load_page(0)
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes("png")))
    else:
        image = Image.open(uploaded_file)

    st.image(image, caption="תצוגה מקדימה", use_column_width=True)

    st.markdown("### 🧭 שלב 1: צייר קו קנה מידה")
    canvas_scale = st_canvas(
        background_image=image,
        height=image.height,
        width=image.width,
        drawing_mode="line",
        stroke_color="#FF0000",
        stroke_width=3,
        key="scale"
    )

    real_length = st.number_input("✏️ הזן את האורך האמיתי של הקו שציירת (במטרים)", min_value=0.0, step=0.1)
    scale = None
    if canvas_scale.json_data and real_length:
        objects = canvas_scale.json_data["objects"]
        if objects:
            line = objects[0]
            x1, y1 = line["left"], line["top"]
            x2, y2 = x1 + line["width"], y1 + line["height"]
            pixel_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if pixel_length > 0:
                scale = real_length / pixel_length
                st.success(f"קנה המידה חושב: {scale:.3f} מטר לפיקסל")

    if scale:
        st.markdown("### 📏 שלב 2: צייר קווים שברצונך למדוד")
        canvas_measure = st_canvas(
            background_image=image,
            height=image.height,
            width=image.width,
            drawing_mode="line",
            stroke_color="#0000FF",
            stroke_width=3,
            key="measure"
        )

        if canvas_measure.json_data:
            st.markdown("### 📊 תוצאות המדידה")
            for i, obj in enumerate(canvas_measure.json_data["objects"]):
                x1, y1 = obj["left"], obj["top"]
                x2, y2 = x1 + obj["width"], y1 + obj["height"]
                pixel_len = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                real_len = pixel_len * scale
                st.write(f"🔹 קו {i+1}: {real_len:.2f} מטר")
