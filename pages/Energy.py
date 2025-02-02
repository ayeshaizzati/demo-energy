import streamlit as st
import folium
from streamlit_folium import st_folium
from data import load_data
import plotly.express as px

st.set_page_config(page_title="Energy Building Model", layout="centered")

#loading csv data
df_consumption = load_data("./data/building_consumption.csv")
df_buildings = load_data("./data/buildings.csv")

st.title("UBC Smart City")
st.markdown("## Energy Building Model")

# initialization of the map
ubc_latitude = 49.2606
ubc_longitude = -123.2460
map = folium.Map(location=[ubc_latitude, ubc_longitude], zoom_start=15, tiles="CartoDB Positron")



# Add buildings to map with markers
for index, row in df_buildings.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"{row['Buildings']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)

with st.container(height = 800, border = False):
    st_folium(map, width = 700, height =800)

#dropdown
with st.container():
    st.markdown("### Building Details")
    selected_buildings = st.multiselect(
        "Select building(s) to view details or compare:",
        options=[row["Buildings"] for index, row in df_buildings.iterrows()],
        default=None,
    )

    # Show details for selected buildings
    if selected_buildings:
        for building in selected_buildings:
            st.markdown(f"## {building}")
            
            building_info = df_buildings[df_buildings["Buildings"] == building].iloc[0]
            st.write(building_info['Description'])
            building_data = df_consumption[df_consumption["Building"] == building]
            
            # Create charts
            st.markdown("### Thermal Metrics")
            
            fig = px.line(building_data, x="Date", y="Thrm_Energy", 
                        title="Thermal Energy Consumption Over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            fig = px.line(building_data, x="Date", y="Thrm_Power", 
                        title="Thermal Power Usage Over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Efficiency Metrics")
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(building_data, x="Date", y="Elec_EUI", 
                           title="Electricity Efficiency")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(building_data, x="Date", y="Thrm_EUI", 
                           title="Thermal Efficiency")
                st.plotly_chart(fig, use_container_width=True)
            col3, col4 = st.columns(2)
            with col3:
                fig = px.bar(building_data, x="Date", y="Wtr_WUI", 
                           title="Water Efficiency")
                st.plotly_chart(fig, use_container_width=True)
            with col4:
                fig = px.bar(building_data, x="Date", y="Total_EUI_excwtr", 
                           title="Overall Efficiency (Excl. Water)")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Water Consumption")
            fig = px.area(building_data, x="Date", y="Wtr_Cns", 
                        title="Water Consumption Over Time")
            st.plotly_chart(fig, use_container_width=True)


