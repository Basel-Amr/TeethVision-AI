# app.py
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
from config import MODEL_DIR, CLASS_NAMES, MODEL_PATHS
from utils import preprocess_image, predict_image, render_confidence_bar
from utils_db import add_or_get_patient, save_prediction, get_all_patient_names
from pages.leaderboard import render_leaderboard
import os
import uuid
from datetime import datetime

st.set_page_config(page_title="Teeth Classifier AI", layout="centered")

# CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
# st.sidebar.image("static/logo.jpeg", width=140)
st.sidebar.title("🧑‍💼 Model Selection")
model_name = st.sidebar.selectbox("Choose a model:", list(MODEL_PATHS.keys()), index=1)

# Patient Info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧑 Patient Info")
all_names = get_all_patient_names()
selected_name = st.sidebar.text_input("Enter patient name:", value="")
if selected_name and selected_name not in all_names:
    st.sidebar.info("New patient will be added.")

# Main App
st.title(" 💉 Teeth Classifier AI Lab")
st.markdown("Upload a dental X-ray image and let our models classify the tooth type.")

uploaded_file = st.file_uploader("Upload a dental image (JPG/PNG):", type=["jpg", "png", "jpeg"])
if uploaded_file and selected_name:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)
    img_array = preprocess_image(image)

    model_path = os.path.join(MODEL_DIR, MODEL_PATHS[model_name])
    if not os.path.exists(model_path):
        st.error("Model file not found!")
    else:
        probs, inf_time = predict_image(model_path, img_array)
        pred_class = CLASS_NAMES[int(probs.argmax())]
        confidence = probs.max() * 100
        st.markdown(render_confidence_bar(pred_class, confidence, inf_time), unsafe_allow_html=True)

        # Plot
        df = pd.DataFrame({"Class": CLASS_NAMES, "Probability": probs}).sort_values("Probability", ascending=False)
        fig = px.bar(df, x="Class", y="Probability", color="Class", template="plotly_dark", text_auto=".2f")
        fig.update_layout(title="🔢 Class Probabilities", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

        # Save image and prediction to DB
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{selected_name}_{timestamp}.jpg"
        save_path = os.path.join("static/uploads", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        image.save(save_path)

        patient_id = add_or_get_patient(selected_name)
        save_prediction(patient_id, save_path, pred_class, confidence)
        st.success("✅ Prediction saved to database.")

# Footer
st.markdown("""
<hr>
<div style='text-align: center;'>
    <p>🚀 Built by <strong>Basel Amr Barakat</strong></p>
    <p>
        <a href='https://www.linkedin.com/in/baselamrbarakat' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='25' style='vertical-align:middle;'/> LinkedIn
        </a>
        &nbsp;&nbsp;&nbsp;
        <a href='https://github.com/Basel-Amr' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/25/25231.png' width='25' style='vertical-align:middle;'/> GitHub
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
