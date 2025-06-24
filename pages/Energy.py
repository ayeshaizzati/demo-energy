

import streamlit as st
import folium
from streamlit_folium import st_folium
from data import load_data
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Energy Building Database", layout="centered")

# Load custom CSS from external file
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.image("media/UBCSCLogo.png")  # Image will use CSS styling

# Loading csv data
df_consumption = load_data("./data/building_consumption.csv")
df_buildings = load_data("./data/buildings.csv")


# Page title and header

st.markdown("""
<div style='text-align: center; line-height: 1.1; padding: 0; margin: 10;'>
    <div style='font-size: 1.5rem; margin-bottom: 15px;'>UBC Smart City</div>
    <div style='font-size: 2.5rem; font-weight: bold; margin-bottom: 50px;'>Energy Building Model</div>
</div>
""", unsafe_allow_html=True)

# Initialization of the map
ubc_latitude = 49.2606
ubc_longitude = -123.2460
map = folium.Map(location=[ubc_latitude, ubc_longitude], zoom_start=15, tiles="CartoDB Positron")

# Dictionary mapping building names to their respective images
building_images = {
    "Pond North": "pond-north.jpeg",
    "Pond East": "pond-east.jpg",
    "Orchard Commons": "orchard.jpeg",
    "The Nest": "nest.jpeg",
    "Irving K. Barber": "ikb.jpg",
    "Asian Centre": "asian.jpeg",
    "Arts Building": "arts.jpeg",
    "Aquatic Centre": "aquatic.jpeg",
    "Alumni Centre": "alumni.jpeg"
}

def display_charts(building):
    st.markdown(f"## {building}")
    building_info = df_buildings[df_buildings["Buildings"] == building].iloc[0]
    
    # Display building image if available
    if building in building_images:
        st.image(f"media/{building_images[building]}", caption=building, use_column_width=True, 
                 output_format="JPEG")
    
    st.write(building_info['Description'])
    building_data = df_consumption[df_consumption["Building"] == building]
    
    st.markdown("### Thermal Metrics")

    fig = px.line(
        building_data, x="Date", y="Thrm_Energy",
        title="Thermal Energy Consumption Over Time",
        labels={"Date": "Date", "Thrm_Energy": "Thermal Energy (kWh)"},
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        building_data, x="Date", y="Thrm_Power",
        title="Thermal Power Usage Over Time",
        labels={"Date": "Date", "Thrm_Power": "Thermal Power (kW)"},
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Efficiency Metrics")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            building_data, x="Date", y="Elec_EUI",
            title="Electricity Efficiency",
            labels={"Date": "Date", "Elec_EUI": "Electricity Efficiency (kWh/m²)"},
            template="plotly_white"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            building_data, x="Date", y="Thrm_EUI",
            title="Thermal Efficiency",
            labels={"Date": "Date", "Thrm_EUI": "Thermal Efficiency (kWh/m²)"},
            template="plotly_white"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig = px.bar(
            building_data, x="Date", y="Wtr_WUI",
            title="Water Efficiency",
            labels={"Date": "Date", "Wtr_WUI": "Water Efficiency (L/m²)"},
            template="plotly_white"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.bar(
            building_data, x="Date", y="Total_EUI_excwtr",
            title="Overall Efficiency (Excl. Water)",
            labels={"Date": "Date", "Total_EUI_excwtr": "Overall Efficiency (kWh/m²)"},
            template="plotly_white"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Water Consumption")
    fig = px.area(
        building_data, x="Date", y="Wtr_Cns",
        title="Water Consumption Over Time",
        labels={"Date": "Date", "Wtr_Cns": "Water Consumption (L)"},
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Simulated Occupancy")
    fig = px.area(
        building_data, x="Date", y="Occupancy",
        title="Simulated Occupancy Over Time",
        labels={"Date": "Date", "Occupancy": "Occupancy (People)"},
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Simulate occupancy values using a normal distribution
np.random.seed(123) 
df_consumption['Occupancy'] = np.clip(
    np.random.normal(loc=50, scale=15, size=len(df_consumption)),
    a_min=0, a_max=None
)

# Add buildings to map with markers and improved popups
for index, row in df_buildings.iterrows():
    popup_content = f"<b>{row['Buildings']}</b>"
    if row['Buildings'] in building_images:
        popup_content += f"<br><img src='media/{building_images[row['Buildings']]}' width='150'>"
    
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_content, max_width=200),
        tooltip=row['Buildings'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)

# Gallery section to display all building images
with st.expander("Building Gallery"):
    cols = st.columns(3)
    for i, (building, image) in enumerate(building_images.items()):
        with cols[i % 3]:
            st.image(f"media/{image}", caption=building, use_column_width=True)

with st.container(height=400, border=False):
    # width = None => full width
    st_folium(map, width=None, height=400)

# Dropdown
with st.container():
    st.markdown("### Building Details")
    selected_buildings = st.multiselect(
        "Select building(s) to view details or compare:",
        options=[row["Buildings"] for index, row in df_buildings.iterrows()],
        default=None,
    )

    if len(selected_buildings) == 1:
        # Show details for selected buildings
        if selected_buildings:
            for building in selected_buildings:
                display_charts(building)
    elif len(selected_buildings) == 2:
        # comparison
        col1, col2 = st.columns(2)
        with col1:
            display_charts(selected_buildings[0])
        with col2:
            display_charts(selected_buildings[1])