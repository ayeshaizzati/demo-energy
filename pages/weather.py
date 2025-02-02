import streamlit as st
from data import load_data
import pandas as pd
from datetime import timedelta

df = load_data("./data/weather.csv")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date', ascending=True).reset_index(drop=True)

# Set page title and headers
st.title("Smart City")
st.header("Vancouver Weather")
st.caption("The data is retrieved from [station], [distance] from UBC Vancouver")

# Date selection
selected_date = st.date_input("Select start date", 
                             min_value=df['date'].min(),
                             max_value=df['date'].max(),
                             value=df['date'].max())

# Convert selected_date to pandas datetime
selected_date = pd.to_datetime(selected_date)

# Find the index of the selected date in the dataframe
date_mask = df['date'] == selected_date

if date_mask.any():
    start_idx = df[date_mask].index[0]
    end_idx = min(start_idx + 7, len(df))  # Show selected day + 7 days
    forecast_days = df.iloc[start_idx:end_idx]
else:
    forecast_days = pd.DataFrame()

# Function to display weather metrics
def display_weather_metrics(days_df):
    if len(days_df) > 4:
        days_df = days_df.iloc[:4]
    if days_df.empty:
        st.warning("No data available for the selected date range")
        return
    
    # Create date headers
    st.write("### Weather Forecast")
    cols = st.columns(len(days_df))
    for idx, col in enumerate(cols):
        date_str = days_df.iloc[idx]['date'].strftime('%b %d')
        col.subheader(date_str)
    
    # Temperature
    st.write("#### Temperature (°C)")
    cols = st.columns(len(days_df))
    for idx, col in enumerate(cols):
        temp = days_df.iloc[idx]['avg_temperature']
        col.metric("", f"{temp:.1f}°C")
    
    # Humidity
    st.write("#### Humidity (%)")
    cols = st.columns(len(days_df))
    for idx, col in enumerate(cols):
        humidity = days_df.iloc[idx]['avg_relative_humidity']
        col.metric("", f"{humidity:.1f}%")
    
    # Wind Speed
    st.write("#### Wind Speed (km/h)")
    cols = st.columns(len(days_df))
    for idx, col in enumerate(cols):
        wind = days_df.iloc[idx]['avg_wind_speed']
        col.metric("", f"{wind:.1f} km/h")
    
    # Precipitation
    st.write("#### Precipitation (mm)")
    cols = st.columns(len(days_df))
    for idx, col in enumerate(cols):
        precip = days_df.iloc[idx]['precipitation']
        col.metric("", f"{precip:.1f} mm")

# Display the weather metrics
display_weather_metrics(forecast_days)