import streamlit as st
import numpy as np
import joblib

import streamlit.components.v1 as components

st.markdown("<h1 style='color:green;'>Welcome to My Smart Sprinkler App</h1>", unsafe_allow_html=True)
st.markdown("<p>Water Wisely, Grow Better 🌱</p>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .my-text {
        color: blue;
        font-size: 24px;
        font-weight: bold;
    }
    .my-box {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='my-box'>The Smart Sprinkler System is an AI-powered irrigation management solution" \
" designed to help farmers and gardeners optimize water usage and enhance crop health." \
" Using real-time soil moisture sensor data," \
" the system predicts which sprinklers need to be activated, ensuring precise watering for each plot.</div>", unsafe_allow_html=True)


st.markdown("""
    <style>
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)



#Load the trained model
model = joblib.load("Farm_Irrigation_System.pkl")

st.title("Smart Sprinkler System")
st.subheader("Enter scaled sensor values (0 to 1) to predict sprinkler status")

#Collect sensor inputs (scaled values)
sensor_values = []
for i in range(20):
    val = st.slider(f"Sensor {i}",min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    sensor_values.append(val)

#Predict button
if st.button("Predict Sprinklers"):
    input_array = np.array(sensor_values).reshape(1, -1)
    prediction = model.predict(input_array)[0]

    st.markdown("###Prediction:")
    for i, status in enumerate(prediction):
        st.write(f"Sprinkler {i} (parcel_{i}): {'ON' if status == 1 else 'OFF'}")