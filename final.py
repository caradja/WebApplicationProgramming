import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image


# Function to be used to download the files as csv files
def to_csv(data_frame):
    return data_frame.to_csv().encode('utf-8')

# Download button class
class Button:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name
       
    def display_button(self):
        st.download_button(label = f'Download participants data from {countries_dictionary[country]}',
                   file_name = f'{self.file_name}_{countries_dictionary[country]}.csv',
                   data = self.data,
                   mime = 'text/csv')
        
        
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
st.markdown(f"<h1 style = 'color:#307be8;'>Partner search app</h1>", unsafe_allow_html = True)
        

confidentiality_agreement = st.checkbox("I understand that the session is confidential & I am not to share data with unauthorized people")

# The content will not be visible to the user unless they agree with the confidentiality agreement
if confidentiality_agreement:
    
    # 3. Selecting the country acronym
    conn = sqlite3.connect('ecsel_database.db')

    # Will be used to generate a dictionary
    countries = pd.read_sql(f"SELECT * FROM countries", conn)

    # Will be used to display the unique activity types to the user
    participants = pd.read_sql(f"SELECT * FROM participants", conn)

    conn.close()


    # Filters will appear in an expander so that it does not occupy too much space on the screen
    with st.beta_expander("Filters"):
        # The dictionary mentioned above
        countries_dictionary = countries.set_index('Country')['Acronym'].to_dict()
        # The acronyms will be shown alphabetically to the user in a drop-down menu
        country = st.selectbox('Choose a country', sorted(countries_dictionary.keys()))

        # The activities
        activity_type_column = participants["activityType"]
        # The unique activities
        activity_type = st.radio('Choose an activity type', activity_type_column.unique())


    # 4. Show the user the country and activity that have been selected
    st.write(f'You have chosen {country} and {activity_type}')


    # 5. Show the total amount of grants received per partner in the selected country in descending order
    conn = sqlite3.connect('ecsel_database.db')
    # Duda: El count era totalpartners?
    # Hay que hacer where role = participants? o solo abajo role = coordinator? No me queda muy claro en el enunciado del trabajo

    df_participants = pd.read_sql(f"""SELECT p.shortName, p.name, p.activityType, p.organizationURL, SUM(p.ecContribution) AS ReceivedGrants, COUNT(p.name) AS TotalParticipations
                                        FROM participants AS p
                                        JOIN countries AS c
                                        ON c.Acronym = p.country
                                        WHERE c.Country = '{country}' AND p.activityType = '{activity_type}'
                                        GROUP BY p.shortName, p.name, p.activityType, p.organizationURL
                                        ORDER BY ReceivedGrants DESC""", conn)

    conn.close()

    # Display it:
    st.subheader(f'Participants in {country}')
    # Style the dataframe beforehand
    df_participants_stylized = df_participants.style.set_properties(**{'background-color': '#f2f9ff', 'color': '#000000'})
    st.dataframe(df_participants_stylized)

    csv_df_participants = to_csv(df_participants)

    first_button = Button(data = csv_df_participants, file_name = f'participants_from')
    first_button.display_button()



    # 6. The system shall connect to the database and generate a new project dataframe with the project
    #coordinators from the selected country (from the organizations table in the database). This
    #dataset should filter only project coordinators and include the following fields: shortName, name,
    #activityType, projectAcronym? -- El nombre de la file no coincide con ninguna tabla de la database, y el nombre de las columnas son iguales que antes?

    # Hay que hacer where role = coordinator, entiendo -- pero el nombre de la tabla no es como dice en el enunciado del trabajo hmm
    conn = sqlite3.connect('ecsel_database.db')
    # Duda: El count era totalpartners?
    df_participants_coordinators = pd.read_sql(f"""SELECT p.shortName, p.name, p.activityType, p.projectAcronym
                                                    FROM participants AS p
                                                    JOIN countries AS c
                                                    ON c.Acronym = p.country
                                                    WHERE c.Country = '{country}' AND p.role = 'coordinator' AND p.activityType = '{activity_type}'
                                                    ORDER BY p.shortName ASC""", conn)
    conn.close()

    # Display it:
    st.subheader(f'Coordinators in {country}')
    # Style the dataframe beforehand
    df_participants_coordinators_stylized = df_participants_coordinators.style.set_properties(**{'background-color': '#f2f9ff', 'color': '#000000'})
    st.dataframe(df_participants_coordinators_stylized)

    csv_df_participants_coordinators = to_csv(df_participants_coordinators)

    second_button = Button(data = csv_df_participants_coordinators, file_name = f'coordinators_from')
    second_button.display_button()
    
    
    # The side bar after all data is extracted
    with st.sidebar:
        st.write("Participants related graphs")
        
        if len(df_participants) > 0:
            corr_coef = np.corrcoef(df_participants["ReceivedGrants"], df_participants["TotalParticipations"])[0][1]
            st.write(f"Correlation coefficient: {corr_coef:.2f}")

            # Generate a scatterplot between the ReceivedGrants and TotalParticipations of Participants (NOT LOG SCALE)
            fig, ax = plt.subplots()
            ax.scatter(df_participants["ReceivedGrants"], df_participants["TotalParticipations"])
            ax.set_xlabel("Received Grants")
            ax.set_ylabel("Total Participations")
            ax.set_title("Received Grants vs. Total Participations")
            #Display the graph
            st.pyplot(fig)
            
            # Generate a violin boxplot to see the underlying distribution of the data as well
            
            fig2, ax2 = plt.subplots()
            sns.violinplot(data = df_participants, x = 'ReceivedGrants')
            ax2.set_xlim(0, None)
            ax2.set_title("Violinplot for Received Grants")
            st.pyplot(fig2)
            
            fig3, ax3 = plt.subplots()
            sns.violinplot(data = df_participants, x = 'TotalParticipations', color = 'red')
            ax3.set_xlim(0, None)
            ax3.set_title("Violinplot for Total Participations")
            st.pyplot(fig3)
