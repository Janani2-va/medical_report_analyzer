import streamlit as st
st.title("Medical Report Analyzer")
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils import extract_text, extract_values, analyze_report

# 🔧 Page Config
st.set_page_config(page_title="AI Medical Analyzer", layout="centered")

# 🎯 Title
st.title("🧠 AI Medical Report Analyzer")
st.markdown("Upload a lab report to analyze key health parameters")

# 📤 Upload File
uploaded_file = st.file_uploader("Upload Medical Report", type=["jpg", "png", "jpeg"])

if uploaded_file:

    # Convert image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    st.image(img, caption="Uploaded Report", use_column_width=True)

    # 🔍 OCR
    text = extract_text(img)

    with st.expander("📄 View Extracted Text"):
        st.text(text)

    # 🧠 Extract + Analyze
    data = extract_values(text)
    results = analyze_report(data)

    st.subheader("📊 Analysis Results")

    if not results:
        st.warning("No medical parameters detected")
    else:
        for key, result in results.items():

            # Special case for BP display
            if key == "Blood Pressure":
                sys, dia = data["bp"]
                display_text = f"{sys}/{dia} → {result}"
            else:
                display_text = f"{data[key.lower()]} → {result}"

            # 🎨 Color Coding
            if "High" in result or "Low" in result:
                st.error(f"{key}: {display_text}")
            elif "Borderline" in result or "Pre" in result:
                st.warning(f"{key}: {display_text}")
            else:
                st.success(f"{key}: {display_text}")

        # 📊 Simple Chart
        st.subheader("📈 Parameter Overview")

        labels = []
        values = []

        for key in data:
            if key != "bp":
                labels.append(key.upper())
                values.append(data[key])

        if values:
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            ax.set_ylabel("Values")
            ax.set_title("Health Parameters")
            st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("⚠️ This is a prototype and not a medical diagnostic tool")
