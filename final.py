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

# 4. Show the user the country that has been selected
st.write(f'You have chosen {countries_dictionary[country_acronym]}')


# 5. Show the total amount of grants received per partner in the selected country
conn = sqlite3.connect('ecsel_database.db')
# Duda: El count era totalpartners?
df_participants = pd.read_sql(f"SELECT shortName, name, activityType, organizationURL, SUM(ecContribution) AS ReceivedGrants, COUNT(name) AS TotalPartners FROM participants WHERE country = '{country_acronym}' GROUP BY shortName, name, activityType, organizationURL", conn)

"""
received_grants = unified[unified['country_acronym'] == acronym].groupby(
    ['shortName', 'name', 'activityType', 'organizationURL']).agg({'ecContribution': 'sum', 'name': 'count'})
received_grants = received_grants.rename(columns={'ecContribution': 'sum_ecContribution'})
received_grants = received_grants.rename(columns={'name': 'count'})
received_grants
"""
    
conn.close()

# participants
st.subheader(f'Participants in {countries_dictionary[country_acronym]}')
st.dataframe(df_participants)
