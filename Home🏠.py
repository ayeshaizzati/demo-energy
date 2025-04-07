import streamlit as st

st.set_page_config(page_title="Energy Building Model", layout="wide")

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

# Main content (unchanged)
col1, col2 = st.columns(2)
with col1:
    st.header("UBC Smart City")
    st.markdown("## Energy Building Model")
    st.write("")
    with st.expander("Information about the dashboard"):
        st.write('''
            This dashboard provides an overview of energy consumption in UBC buildings, including thermal, water, and electricity usage.
    - Energy Trends – Analyze energy consumption patterns over time.
    - Weather Insights – Explore the relationship between energy usage and weather conditions.
    - Building Heat Loss Model – Visualize heat loss trends based on building envelope, ventilation, equipment, and occupancy data, estimating how energy demand changes with visitor traffic.

    This tool helps in understanding energy efficiency and identifying opportunities for improvement.
        ''')
with col2:
    st.image("data/map.jpg")