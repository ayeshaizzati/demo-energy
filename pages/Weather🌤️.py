import streamlit as st
from data import load_data
import pandas as pd

st.set_page_config(layout="wide")
# Custom CSS for sidebar styling and larger image
st.markdown("""
    <style>
    /* Style the sidebar */
    [data-testid="stSidebar"] { /* Dark blue-gray background */
        padding: 20px 20px 40px 20px;  /* Increased bottom padding for more space */
    }
    /* Style navigation links */
    [data-testid="stSidebar"] .css-17lntkn a {
        color: #0055b7;  /* UBC darker blue */
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
        display: block;
        text-decoration: none;
    }
    [data-testid="stSidebar"] .css-17lntkn a:hover {
        background-color: #e9ecef;  /* Light hover effect */
        color: #003087;
    }
    /* Make sidebar image full-width and larger */
    [data-testid="stSidebar"] img {
        width: 100% !important;  /* Full sidebar width */
        height: 200px;  /* Set a specific height */
        object-fit: cover;  /* Crop to fit, no stretching */
        display: block;  /* Ensure proper rendering */
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("---")  # Divider for separation
    st.image("media/Logo1.png")  # Image will use CSS styling
df = load_data("./data/weather.csv")

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date', ascending=True).reset_index(drop=True)

# === HEADER ===
st.markdown("""
    <style>
        .forecast-title { font-size: 40px; font-weight: 700; margin-bottom: 0px; }
        .forecast-caption { color: gray; margin-top: 0px; margin-bottom: 30px; }

        .card-container {
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 20px;
            flex-wrap: nowrap;
            overflow-x: auto;
            padding-bottom: 20px;
        }

        .card {
            background-color: white;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            box-shadow: 4px 4px 20px rgba(0, 0, 0, 0.1);
            min-width: 200px;
            max-width: 200px;
            flex: 0 0 auto;
        }

        .weather-icon {
            font-size: 40px;
            margin: 10px 0;
        }

        .metric-label {
            font-size: 14px;
            color: #555;
            margin: 5px 0;
        }

        /* Scrollbar styles (optional) */
        .card-container::-webkit-scrollbar {
            height: 8px;
        }
        .card-container::-webkit-scrollbar-thumb {
            background: #ccc;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns([2, 1, 1])
with col1:  # Use the middle column for the date picker
    st.markdown('<div class="forecast-title">Vancouver, BC</div>', unsafe_allow_html=True)
    selected_date = st.date_input("Select start date", 
        min_value=df['date'].min(),
        max_value=df['date'].max(),
        value=df['date'].max())
selected_date = pd.to_datetime(selected_date)

date_mask = df['date'] == selected_date

if date_mask.any():
    start_idx = df[date_mask].index[0]
    end_idx = min(start_idx + 5, len(df))  # Show 4-day forecast
    forecast_days = df.iloc[start_idx:end_idx]
else:
    forecast_days = pd.DataFrame()

# === DISPLAY CARDS ===
if not forecast_days.empty:
    st.subheader("Weather Forecast")
    cols = st.columns(5)  # Create 4 columns for 4 cards
    for idx, row in enumerate(forecast_days.itertuples()):
        with cols[idx]:
            date_str = row.date.strftime('%B %d')
            temp = f"{row.avg_temperature:.1f}°C"
            wind = f"{row.avg_wind_speed:.0f} km"
            precip = f"{row.precipitation:.0f} mm"
            icon = "☀️" if row.avg_temperature > 18 else "⛈️"

            st.markdown(
                f"""
                <div style='
                    background: linear-gradient(145deg, #e0f7fa, #b2ebf2);
                    border-radius: 20px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    color: #000000;
                '>
                    <h4 style='margin-bottom: 0; color: #000000;'>{date_str}</h4>
                    <div style='font-size: 40px; margin: 10px 0;'>{icon}</div>
                    <p style='font-size: 20px; font-weight: bold; color: #000000;'>{temp}</p>
                    <p style='margin: 5px 0; color: #000000;'>🌬️ <b>{wind}</b> wind</p>
                    <p style='margin: 5px 0; color: #000000;'>💧 <b>{precip}</b> rain</p>
                </div>
                """,
                unsafe_allow_html=True
            )


else:
    st.warning("No data available for the selected date.")

