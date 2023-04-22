import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image


# Function to be used to download the files as csv files
def to_csv(data_frame):
    return data_frame.to_csv().encode('utf-8')


# 1. Adding the logo of the application
logo = Image.open('logo.png')

# In order to center the logo, the following process will be applied:
container = st.beta_container()

with container:
    col1, col2, col3 = st.beta_columns(3)
    col2.image(logo, width=250)
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


# 5. Show the total amount of grants received per partner in the selected country in descending order
conn = sqlite3.connect('ecsel_database.db')
# Duda: El count era totalpartners?
# Hay que hacer where role = participants? o solo abajo role = coordinator? No me queda muy claro en el enunciado del trabajo
df_participants = pd.read_sql(f"SELECT shortName, name, activityType, organizationURL, SUM(ecContribution) AS ReceivedGrants, COUNT(name) AS TotalPartners FROM participants WHERE country = '{country_acronym}' GROUP BY shortName, name, activityType, organizationURL ORDER BY ReceivedGrants DESC", conn)
conn.close()

# Display it:
st.subheader(f'Participants in {countries_dictionary[country_acronym]}')
# Style the dataframe beforehand
df_participants_stylized = df_participants.style.set_properties(**{'background-color': '#fff0f4', 'color': '#000000'})
st.dataframe(df_participants_stylized)

csv_df_participants = to_csv(df_participants)

st.download_button(label = f'Download participants data from {countries_dictionary[country_acronym]}',
                   file_name = f'participants_from_{countries_dictionary[country_acronym]}.csv',
                   data = csv_df_participants,
                   mime = 'text/csv')



# 6. The system shall connect to the database and generate a new project dataframe with the project
#coordinators from the selected country (from the organizations table in the database). This
#dataset should filter only project coordinators and include the following fields: shortName, name,
#activityType, projectAcronym? -- El nombre de la file no coincide con ninguna tabla de la database, y el nombre de las columnas son iguales que antes?

# Hay que hacer where role = coordinator, entiendo -- pero el nombre de la tabla no es como dice en el enunciado del trabajo hmm
conn = sqlite3.connect('ecsel_database.db')
# Duda: El count era totalpartners?
df_participants_coordinators = pd.read_sql(f"SELECT shortName, name, activityType, projectAcronym FROM participants WHERE country = '{country_acronym}' AND role = 'coordinator' ORDER BY shortName ASC", conn)
conn.close()

# Display it:
st.subheader(f'Coordinators in {countries_dictionary[country_acronym]}')
st.dataframe(df_participants_coordinators)

csv_df_participants_coordinators = to_csv(df_participants_coordinators)

st.download_button(label = f'Download coordinators data from {countries_dictionary[country_acronym]}',
                   file_name = f'participants_from_{countries_dictionary[country_acronym]}.csv',
                   data = csv_df_participants_coordinators,
                   mime = 'text/csv')
