import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image

# 1. Adding the logo of the application
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
    

# 2. Adding the title of the app
st.title("Partner search app")



# 3. Selecting the country acronym

conn = sqlite3.connect('ecsel_database.db')

# Will be used to generate a dictionary
countries = pd.read_sql(f"SELECT * FROM countries", conn)

conn.close()

# The dictionary mentioned above
countries_dictionary = countries.set_index('Acronym')['Country'].to_dict()

# The acronyms will be shown alphabetically to the user in a drop-down menu
country_acronym = st.selectbox('Choose a country', sorted(countries_dictionary.keys()))

# Show the country that has been selected
st.write(f'You have chosen {countries_dictionary[country_acronym]}')



# SQL queries
conn = sqlite3.connect('ecsel_database.db')
#df_grants = pd.read_sql(f"SELECT year, grants FROM grants WHERE country = '{country}' ", conn)
#df_grants = df_grants.set_index('year')
df_participants = pd.read_sql(f"SELECT * FROM participants WHERE country = '{country}' ", conn)
#df_coordinators = pd.read_sql(f"SELECT * FROM coordinators WHERE country = '{country}' ", conn)
conn.close()

# participants
st.subheader(f'Participants in {countries_dictionary[country]}')
st.dataframe(df_participants)
