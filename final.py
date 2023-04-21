"""import streamlit as st
import pandas as pd
from sqlite3 import connect

st.write("My First Streamlit Web App")
df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
st.write(df)

conn = sqlite3.connect('ecsel_database.db')
cur = conn.cursor()
cur.execute('SELECT Country FROM Countries')
df = pd.DataFrame(cur.fetchall(), columns = ['COUNTRYNAME'])"""


import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image

# Load the logo image from file
logo = Image.open('logo.jpg')

# Resize the logo image to a width of 150 pixels
resized_logo = logo.resize((150, 150))

# Create a container and center it
container = st.beta_container()
container.image(resized_logo, use_column_width=True, caption='Logo')

# Display the title
st.title("Partner search")


# Select country
countries = ['ES', 'FR', 'DE']
ct = {'ES': 'Spain', 'DE': 'Germany', 'FR':'France'}
country = st.selectbox('Select country',countries)
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
