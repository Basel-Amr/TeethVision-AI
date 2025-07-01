# records_dashboard.py
import streamlit as st
import pandas as pd
from utils_db import get_records_by_patient, get_records_by_date, get_all_patient_names
from datetime import datetime
import os

st.title("📂 Patient Prediction Records")
st.markdown("Search and view classification results stored in the database.")

# ----------------- Tabs for Search Options -----------------
tab1, tab2 = st.tabs(["🔍 Search by Patient", "🗕 Search by Date"])

# ----------------- TAB 1: BY PATIENT -----------------
with tab1:
    names = get_all_patient_names()
    selected_name = st.selectbox("Choose a patient:", names)

    if selected_name:
        records = get_records_by_patient(selected_name)
        if records:
            df = pd.DataFrame(records, columns=["Image Path", "Predicted Class", "Confidence", "Timestamp"])
            df["Confidence"] = df["Confidence"].apply(lambda x: f"{x:.2f}%")

            st.success(f"Found {len(df)} record(s) for {selected_name}:")

            # Class filter with unique key
            selected_classes = st.multiselect(
                "Filter by predicted class:",
                df["Predicted Class"].unique(),
                default=df["Predicted Class"].unique(),
                key="patient_class_filter"
            )
            df = df[df["Predicted Class"].isin(selected_classes)]

            # Display table
            st.dataframe(df, use_container_width=True)

            # Show image preview
            for _, row in df.iterrows():
                if os.path.exists(row["Image Path"]):
                    st.image(row["Image Path"], caption=f"{row['Predicted Class']} - {row['Timestamp']}", width=200)

            # Export to CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Export as CSV", data=csv, file_name=f"{selected_name}_records.csv", mime="text/csv")
        else:
            st.warning("No records found for this patient.")

# ----------------- TAB 2: BY DATE -----------------
with tab2:
    date = st.date_input("Select date:", datetime.today())
    if date:
        date_str = date.strftime("%Y-%m-%d")
        records = get_records_by_date(date_str)
        if records:
            df = pd.DataFrame(records, columns=["Patient Name", "Image Path", "Predicted Class", "Confidence", "Timestamp"])
            df["Confidence"] = df["Confidence"].apply(lambda x: f"{x:.2f}%")

            st.success(f"Found {len(df)} record(s) on {date_str}:")

            # Class filter with unique key
            selected_classes = st.multiselect(
                "Filter by predicted class:",
                df["Predicted Class"].unique(),
                default=df["Predicted Class"].unique(),
                key="date_class_filter"
            )
            df = df[df["Predicted Class"].isin(selected_classes)]

            # Display table
            st.dataframe(df, use_container_width=True)

            # Show image preview
            for _, row in df.iterrows():
                if os.path.exists(row["Image Path"]):
                    st.image(row["Image Path"], caption=f"{row['Patient Name']} - {row['Predicted Class']} - {row['Timestamp']}", width=200)

            # Export to CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Export as CSV", data=csv, file_name=f"records_{date_str}.csv", mime="text/csv")
        else:
            st.warning(f"No records found on {date_str}.")
