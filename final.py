import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image

from PIL import Image
import streamlit as st


# Adding the logo of the application
logo = Image.open('logo.png')

# In order to center the logo, the following process will be applied:
container = st.beta_container()
with container:
    st.title("My centered title")

# Add CSS styling to center the container
st.markdown(
    f"""
    <style>
    .element-container:nth-child(3) {{
        display: flex;
        justify-content: center;
    }}
    .element-container:nth-child(3) > div {{
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
    
    
# In order to center the title of the application, a similar process will be applied:
container = st.beta_container()
with container:
    st.title("My centered title")

# Add CSS styling to center the container
st.markdown(
    f"""
    <style>
    .element-container:nth-child(3) {{
        display: flex;
        justify-content: center;
    }}
    .element-container:nth-child(3) .stTitle {{
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)



# Select country
countries = ['ES', 'FR', 'DE']
ct = {'ES': 'Spain', 'DE': 'Germany', 'FR':'France'}
country = st.selectbox('Select country', countries)
st.write(f'You selected: {country}-{ct[country]}')

# SQL queries
conn = sqlite3.connect('ecsel_database.db')
#df_grants = pd.read_sql(f"SELECT year, grants FROM grants WHERE country = '{country}' ", conn)
#df_grants = df_grants.set_index('year')
df_participants = pd.read_sql(f"SELECT * FROM participants WHERE country = '{country}' ", conn)
#df_coordinators = pd.read_sql(f"SELECT * FROM coordinators WHERE country = '{country}' ", conn)
conn.close()

# participants
st.subheader(f'Participants in {ct[country]}')
st.dataframe(df_participants)
