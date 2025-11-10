import streamlit as st
import joblib
import numpy as np

# Load the saved model
model = joblib.load("crop_yield_model.pkl")

st.set_page_config(page_title="Crop Yield & Fertilizer Recommender", page_icon="🌾")
st.title("🌾 Crop Yield Prediction & Fertilizer Recommendation System")
st.write("Enter the details below to estimate crop yield and get fertilizer advice:")

# Input fields
region = st.selectbox("Region (0–3)", [0, 1, 2, 3])
soil = st.selectbox("Soil Type (0–5)", [0, 1, 2, 3, 4, 5])
crop = st.selectbox("Crop Type (0–5)", [0, 1, 2, 3, 4, 5])
rainfall = st.number_input("Rainfall (mm)", 0.0, 1000.0, 500.0)
temp = st.number_input("Temperature (°C)", 10.0, 45.0, 25.0)
fertilizer = st.selectbox("Fertilizer Used (0=No, 1=Yes)", [0, 1])
irrigation = st.selectbox("Irrigation Used (0=No, 1=Yes)", [0, 1])
weather = st.selectbox("Weather Condition (0–2)", [0, 1, 2])
days = st.number_input("Days to Harvest", 50, 200, 100)

# Prediction + recommendation
if st.button("Predict"):
    features = np.array([[region, soil, crop, rainfall, temp, fertilizer, irrigation, weather, days]])
    predicted_yield = model.predict(features)[0]

    # Fertilizer logic
    if (predicted_yield < 4) and (fertilizer == 0):
        rec = "🧪 Use nitrogen-rich fertilizer to improve yield."
    elif (4 <= predicted_yield <= 6) and (fertilizer == 1):
        rec = "🌾 Maintain current fertilizer use; soil performing well."
    elif predicted_yield > 6:
        rec = "🌱 Soil fertility sufficient — consider reducing fertilizer usage."
    else:
        rec = "⚙️ Review crop and soil conditions."

    st.success(f"Predicted Crop Yield: {predicted_yield:.2f} tons/hectare")
    st.info(rec)
