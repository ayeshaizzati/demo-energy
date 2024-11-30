import numpy as np
import pandas as pd

def generate_data():

    years = range(2000, 2025)

    data = {
        "Year": years,
        "Water Consumption (m³)": np.random.randint(1000, 5000, len(years)),  # Random water usage
        "Electricity Consumption (kWh)": np.random.randint(5000, 20000, len(years)),  # Random electricity usage
        "Thermal Power Consumption (kW)": np.random.randint(2000, 10000, len(years)),  # Random thermal power usage
    }

    df_consumption = pd.DataFrame(data)

    return df_consumption