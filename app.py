import streamlit as st
import folium
from streamlit_folium import st_folium
from src import consumption_patterns

google_maps_api_key = "AIzaSyCe9CIjgjUMp-Wdxb95plgkp1ywtG81a5g"

st.set_page_config(layout="wide")

st.title('UBC Smart City Data Dashboard!')

user_input = st.text_input("Enter parameters:")
st.write("Energy waste:", user_input + "000")

ubc_latitude = 49.2606
ubc_longitude = -123.2460

# initialization of the map
map = folium.Map(location=[ubc_latitude, ubc_longitude], zoom_start=15, tiles="CartoDB Positron")

# buildings with coordinates and dummy energy usages
buildings = [
    {"name": "ICICS", "lat": 49.2615, "lon": -123.2484, "energy_use": "500 kWh"}, 
    {"name": "Sauder", "lat": 49.2643, "lon": -123.2533, "energy_use": "750 kWh"},
    {"name": "UBC Library", "lat": 49.2676, "lon": -123.2520, "energy_use": "300 kWh"},
    {"name": "Brock North", "lat": 49.2623, "lon": -123.2545, "energy_use": "500 kWh"}
]

# Add buildings to map with markers
for building in buildings:
    folium.Marker(
        location=[building["lat"], building["lon"]],
        popup=f"{building['name']} - Energy Use: {building['energy_use']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)

st.markdown(
    """
    <style>
        .map_div {
            height: 80vh;  /* Adjusted height for the map */
            width: 100%;   /* Full width */
            border: 2px solid #4CAF50;  /* Add a green border */
            border-radius: 10px;        /* Round corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);  /* Shadow effect */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# map_html = f"""
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Google Maps</title>
#     <script src="https://maps.googleapis.com/maps/api/js?key={google_maps_api_key}&callback=initMap" async defer></script>
#     <style>
#         #map {{
#             height: 500px;  /* Set the height of the map */
#             width: 100%;    /* Set the width of the map */
#         }}
#     </style>
#     <script>
#         function initMap() {{
#             var ubc = {{ lat: 49.2606, lng: -123.2460 }};  // UBC coordinates
#             var map = new google.maps.Map(document.getElementById('map'), {{
#                 zoom: 15,
#                 center: ubc
#             }});
#             var marker = new google.maps.Marker({{
#                 position: ubc,
#                 map: map,
#                 title: 'UBC'
#             }});
#         }}
#     </script>
# </head>
# <body>
#     <div id="map"></div>
# </body>
# </html>
# """

# st.components.v1.html(map_html, height=550)


with st.container():
    st.subheader("UBC Energy Usage Map")
    st_folium(map, width=1200, height=600)



df_consumption = consumption_patterns.generate_data()

# Initialize session state for toggles
if "visibility" not in st.session_state:
    st.session_state.visibility = {
        "Water Consumption (m³)": True,
        "Electricity Consumption (kWh)": True,
        "Thermal Power Consumption (kW)": True
    }


columns = ["Water Consumption (m³)", "Electricity Consumption (kWh)", "Thermal Power Consumption (kW)"]
buttons = st.columns(len(columns))

for i, col in enumerate(columns):
    if buttons[i].button(f"Toggle {col}"):
        st.session_state.visibility[col] = not st.session_state.visibility[col]

columns_to_plot = ["Year"]  
for col in columns:
    if st.session_state.visibility[col]:
        columns_to_plot.append(col)

if len(columns_to_plot) > 1:
    st.line_chart(df_consumption[columns_to_plot].set_index("Year"))
else:
    st.write("Please toggle at least one column to display data.")
