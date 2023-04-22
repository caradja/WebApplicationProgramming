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
    col1, col2, col3 = st.beta_columns(3)
    col2.image(logo, width=200)
    col1.empty()
    col3.empty()

# CSS is needed in this case, otherwise the logo will be centered but will also appear really big
# This solution allows us to preserve the original ratio of the image while also centering it
container.markdown(
    f"""
    <style>
    .element-container:nth-child(3) {{
        display: flex;
        justify-content: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
    

# The title of the app
st.title("Partner search app")





# Select country
countries = pd.read_sql(f"SELECT Acronym FROM countries WHERE country = '{country}' ", conn)
print(countries)
#['ES', 'FR', 'DE']
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
