import streamlit as st
import serial
import time

# Function to read AQI from Arduino
def get_aqi_reading():
    try:
        with serial.Serial('COM_PORT', 9600, timeout=1) as ser:  # Replace 'COM_PORT' with your Arduino port
            time.sleep(2)  # Wait for the connection to establish
            aqi_value = ser.readline().decode('utf-8').strip()  # Read a line from the serial
            return float(aqi_value)  # Convert to float
    except Exception as e:
        st.error(f"Error reading from Arduino: {e}")
        return None

# Title of the application
st.title("Air Quality Index (AQI) Monitor")

# Sidebar for settings
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 10, 5)

# Main content
st.header("Current AQI Level")
aqi_value = get_aqi_reading()
if aqi_value is not None:
    st.metric(label="AQI", value=aqi_value)

    # Display AQI category
    if aqi_value <= 50:
        category = "Good"
        color = "green"
    elif aqi_value <= 100:
        category = "Moderate"
        color = "yellow"
    elif aqi_value <= 150:
        category = "Unhealthy for Sensitive Groups"
        color = "orange"
    elif aqi_value <= 200:
        category = "Unhealthy"
        color = "red"
    elif aqi_value <= 300:
        category = "Very Unhealthy"
        color = "purple"
    else:
        category = "Hazardous"
        color = "maroon"

    st.markdown(f"<h2 style='color: {color};'>{category}</h2>", unsafe_allow_html=True)

# Instructions
st.sidebar.subheader("Instructions")
st.sidebar.write("1. Place the sensor outside the vehicle.")
st.sidebar.write("2. Adjust the refresh rate to see updated AQI levels.")
st.sidebar.write("3. Monitor the AQI levels for safety.")

# Footer
st.sidebar.write("Developed by [Your Name]")
