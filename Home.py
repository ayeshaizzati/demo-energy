import streamlit as st

st.set_page_config(page_title="Home", layout="centered")

# Load custom CSS from external file
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Sidebar content
with st.sidebar:
    st.image("media/UBCSCLogo.png")

# Main content (unchanged)
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; line-height: 1.1; padding: 0; margin: 10;'>
    <div style='font-size: 1.5rem; margin-bottom: 15px;'>UBC Smart City</div>
    <div style='font-size: 2.5rem; font-weight: bold; margin-bottom: 50px;'>Energy Building Database</div>
</div>
""", unsafe_allow_html=True)


st.write("")
with st.expander("Information about the dashboard"):
    st.write('''
This dashboard provides an overview of energy consumption in UBC buildings, including thermal, water, and electricity usage.
- Energy Trends – Analyze energy consumption patterns over time.
- Weather Insights – Explore the relationship between energy usage and weather conditions.
- Building Heat Loss Model – Visualize heat loss trends based on building envelope, ventilation, equipment, and occupancy data, estimating how energy demand changes with visitor traffic.

This tool helps in understanding energy efficiency and identifying opportunities for improvement.
    ''')


