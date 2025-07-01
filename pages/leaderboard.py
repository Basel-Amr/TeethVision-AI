# pages/leaderboard.py
import streamlit as st
import pandas as pd
import os
import plotly.express as px
from config import MODEL_DIR

def render_leaderboard():
    st.subheader("📊 Model Leaderboard")
    try:
        df = pd.read_csv(os.path.join(MODEL_DIR, "model_comparison.csv"))
        fig = px.scatter(df, x="Model Size (MB)", y="Test Accuracy", color="Model",
                         size="Inference Time (s)", title="🏋 Accuracy vs. Size Tradeoff",
                         template="plotly_dark")
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig)
        st.dataframe(df)
    except:
        st.warning("Model comparison file not found.")

render_leaderboard()