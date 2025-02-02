import streamlit as st

st.set_page_config(page_title="Energy Building Model", layout="centered")

st.title("UBC Smart City")
st.markdown("## Energy Building Model")
st.write("")

# for information about the dashboard
with st.expander("Information about the dashboard"):
    st.write('''
        This dashboard provides an overview of energy consumption in UBC buildings, including thermal, water, and electricity usage.
- Energy Trends – Analyze energy consumption patterns over time.
- Weather Insights – Explore the relationship between energy usage and weather conditions.
- Building Heat Loss Model – Visualize heat loss trends based on building envelope, ventilation, equipment, and occupancy data, estimating how energy demand changes with visitor traffic.

This tool helps in understanding energy efficiency and identifying opportunities for improvement.
    ''')


