conn = sqlite3.connect('ecsel_database.db')
cur = conn.cursor()

#creation of a new dataframe with the countries' information. 
cur.execute('SELECT Country, Acronym FROM Countries')
df = pd.DataFrame(cur.fetchall(), columns = ['Countries', 'Acronym'])


import streamlit as st
import pandas as pd
from PIL import Image

#selection of the column with the country names.
countries_column = df['Countries']
countries = []

#Title and image
image=Image.open('KDT JU logo full1.jpg')
st.image(image)
st.title('Partner search tool')

#Selectbox with list of countries (association with the acronym)
for i in countries_column:
  countries.append(i)
country_selected = st.selectbox('Country name', countries)

#location of the country selected within the created list. 
for i in range(len(countries)):
  if countries[i]==country_selected:
    position=i

#creation of a new dataframe with the acronyms. 
acronym_column = df['Acronym']
acronym=[]
for i in acronym_column:
  acronym.append(i)

#selection of the acronym in the same position as the country selected before. 
my_acronym=acronym[position]

st.write('You selected:', country_selected,',',my_acronym)

#Graph creation with information about the country selected. 
st.header('Yearly EC contribution in {} (€)'.format(country_selected))
cur.execute('''SELECT SUM(ecContribution), year 
               FROM Participants 
               JOIN Projects ON Participants.projectID=Projects.projectID 
               WHERE country = '{}' 
               GROUP BY year'''.format(my_acronym))

#creation of a dataframe with all the information extract from the above query. 
df_contribution_per_year=pd.DataFrame(cur.fetchall(), columns=['ecContribution', 'year'])

#if statement to display or not the graph. 
if len(df_contribution_per_year.index)==0:
  st.write('Sorry, there is no information')
else:
  #the years will be set as the index of the graph. 
  st.bar_chart(df_contribution_per_year.set_index('year'))

#DATAFRAME OF PARTICIPANTS OF THE COUNTRY SELECTED. 
st.header('Participants of {}'.format(country_selected))
cur.execute("SELECT country, shortName, name, activityType, SUM(ecContribution), organizationURL, COUNT(organizationURL) FROM Participants WHERE role = 'participant' AND country = '{}' GROUP BY organizationURL ORDER BY SUM(ecContribution)DESC".format(my_acronym))
df_participants1 = pd.DataFrame(cur.fetchall(), columns= ['country', 'shortName', 'name', 'activityType', 'Sum','organizationURL', 'count_project'])  

#appplying background color to df
# Set CSS properties for the elements in dataframe
df_participants = df_participants1.style.set_properties(**{'background-color': '#e1f3ff',
                                                           'color': 'black',
                                                           'border-color': 'white'})

#creation of the download button. 
@st.cache
#creation of a function to convert the existing dataframes to csv format. 
def convert(df):
  return df.to_csv().encode('utf-8')

#participants dataframe is converted to csv using the previous function. 
file_participants=convert(df_participants1)

#if statement to show or not the table (depending on whether it is empty or not. 
if len(df_participants.index)==0: 
  st.write('Sorry, there is no information')
else:
  st.dataframe(df_participants)
  st.download_button(
  label='Download participants data from {} as CSV'.format(country_selected), 
  data=file_participants, 
  file_name='participants_{}.csv'.format(country_selected), 
  mime='text/csv'
)
  


#DATAFRAME OF COORDINATORS OF THE CHOSEN COUNTRY. 
st.header('Coordinators of {}'.format(country_selected))

#Query to extract the information of the coordinators of the chosen country. 
cur.execute("SELECT shortName, name, ActivityType, projectAcronym FROM participants WHERE role='coordinator' AND country='{}'ORDER BY shortName".format(my_acronym))
df_coordinators = pd.DataFrame(cur.fetchall(), columns= ['Short Name', 'Name', 'Activity Type', 'Project Acronym']) 

##Keyword function incorporation
def acronym_function(x):
    d = {'MATQu': 'computing, technology, qubit', 'HELoS': 'initiative, medical, device, technology', 
     'AFarCloud': 'farming, labour, health, order, project', 'ASTONISH': 'application, imaging, technology', 
     'EXIST': 'image, sensor, imaging, pixel, high, filter, spectral', 'CSA-Industry4.E': 'liase, stakeholder, project', 
     'DENSE': 'system, weather, environment', 'Productive4.0': 'project, industry, solution', 
     'ENABLE-S3': 'system, test, validation', 'MANTIS': 'mantis, maintenance, system', 
     'POSITION-II': 'position, technology, platform', 'Moore4Medical': 'medical, application, technology, platform', 
     'TRANSACT': 'safety, critical, system, service, transact, cloud', 'InSecTT': 'thing, intelligent, secure, system', 
     'InForMed': 'pilot, line, fabrication', 'SCOTT': 'wireless, solution, end, domain, user', 
     'MegaMaRt2': 'productivity, industrial, runtime', 'DELPHI4LED': 'industry, product, market, multi, model, development, tool, compact', 
     '3Ccar': 'project, complexity, semiconductor, innovation', 'PRYSTINE': 'system, fail, operational, fusion', 
     'RobustSENSE': 'system, condition, robustsense', 'EuroPAT-MASIP': '', 'NewControl': 'platform, perception, control, safety', 
     'IMOCO4.E': 'machine, layer, control', 'FRACTAL': 'computing, node, cognitive', 
     'SECREDAS': 'title, security, cross, domain, reliable, dependable, multi, methodology, reference, architecture, component, autonomous, system, high, privacy, protection, functional, safety, operational, performance', 'AutoDrive': 'driving, european, system, autodrive, situation, safe', 
     'NextPerception': 'smart, system, health, wellbeing, solution, project, automotive, intelligence, monitoring', 
     'StorAIge': 'technology, high, performance, power, solution, application', 'REACTION': 'sic, line, power, smart', 
     'AI4DI': 'industry, ai, system', 'Arrowhead Tools': 'digitalisation, automation, tool, engineering', 
     'WInSiC4AP': 'technology, application, tier1', 'iRel40': 'reliability, system, application', 'R3-PowerUP': 'mm, pilot, line, smart, power', 
     'Energy ECS': 'energy, technology, new', 'PROGRESSUS': 'smart, grid, infrastructure, power, station, energy', 
     'BEYOND5': 'radio, technology, soi, pilot', 'YESvGaN': 'yesvgan, low, cost, power, transistor, technology, vertical', 
     'ADACORSA': 'drone, technology, system', 'CONNECT': 'power, energy, grid, order, local', 'GaN4AP': 'gan, power, device', 
     'DAIS': 'new, component, project', 'ArchitectECA2030': 'validation, eca, vehicle, residual, risk', 
     'CHARM': 'manufacturing, industry, technology, sensor', 'COMP4DRONES': 'drone, ecosystem, comp4drone, architecture, application, compositional, platform', 
     'AI-TWILIGHT': 'lighting, product, digital, twin, ai', 'IoSense': 'manufacturing, market, line, sensor', 
     'PIN3S': 'semiconductor, technology, equipment, material', 'AI4CSM': 'mobility, automotive, industry, transition, digital, vehicle',
     'SILENSE': 'smart, acoustic, technology', 'Power2Power': 'power2power, innovation, power, smart, energy, application, key', 
     'MADEin4': 'metrology, productivity, industry, booster, major, challenge', 'FITOPTIVIS': 'objective, low, optimisation', 
     'SC3': 'semiconductor, supply, domain', 'ANDANTE': 'hardware, capability, application', 
     'COSMOS': 'project, ecsel, lighthouse, stakeholder', 'TAKEMI5': 'project, metrology, process, tool', 
     'OSIRIS': 'sic, power, substrate', 'PRIME': 'project, power, technology, design, block, system, iot', 
     'ID2PPAC': 'project, technology, nm, node, device', 'TAPES3': 'project, metrology, device', 
     'TAKE5': 'project, nm, technology, process', 'PowerBase': 'pilot, line, project', 'SeNaTe': 'nm, technology, process', 
     'ADMONT': 'pilot, line, technology, process, smart', 'MICROPRINCE': 'pilot, line, functional, component, technology', 
     'WAKeMeUP': 'project, memory, application, technology', 'APPLAUSE': 'advanced, packaging, manufacturing', 
     'SafeCOP': 'system, wireless, certification', 'TRANSFORM': 'energy, technology, process, new', 
     'SWARMs': 'offshore, vehicle, auvs, rovs', 'WAYTOGO FAST': 'project, technology, fdsoi, nm', 
     'AMASS': 'system, assurance, certification', 'AIDOaRt': 'continuous, development, software', 
     'CPS4EU': 'cps, technology, strategic, industry, european, large', 'IT2': 'project, technology, equipment, system', 
     'VALU3S': 'manufacturer, system, domain, v&v, method, tool', 'iDev40': 'development, process, manufacturing, digital, technology', 
     '5G_GaN2': 'technology, mm, wave', 'AQUAS': 'complexity, system, world, safety, security, performance, industrial', 
     'HiEFFICIENT': 'partner, high, level, system', 'HELIAUS': 'perception, system, thermal', 
     'SemI40': 'electronic, manufacturing, semi40, industry, partner, system', 'EnSO': 'energy, objective, smart', 
     'I-MECH': 'mech, system, motion, speed, control', 'HiPERFORM': 'high, semiconductor, power', 
     '3DAM': 'project, new, metrology, semiconductor, technology', 'VIZTA': 'technology, sensor, source, range, key, smart, filter, integrated', 
     'UltimateGaN': 'power, application, gan, device, efficiency', 'BRAINE': 'edge, computing, braine', 
     'R2POWER300': 'manufacturing, line, mm, new, process, technology, smart, power', 'REFERENCE': 'european, rf, technology', 
     'TARANTO': 'project, high, system', 'TEMPO': 'neuromorphic, dnn, technology', 'OCEAN12': 'fdsoi, technology, low'}
    return d[x]

#creation of a new column in the just-created dataframe. 
df_coordinators['Keywords'] = df_coordinators['Project Acronym'].apply(acronym_function)
##Style of df
df_coordinators_new = df_coordinators.style.set_properties(**{'background-color': '#BFD7ED',
                                                          'color': 'black',
                                                          'border-color': 'white'})

#DOWNLOAD BUTTON COORDINATORS. 
#The new dataframe is converted into CSV format using the previously created function. 
file_coordinators=convert(df_coordinators)

#if statement to show or not the coordinators' dataframe (depending on whether it is empty or not). 
if len(df_coordinators_new.index)==0: 
  st.write('Sorry, there is no information')
else:
    st.dataframe(df_coordinators_new)
    st.download_button(
  label='Download coordinators data from {} as CSV'.format(country_selected), 
  data=file_coordinators, 
  file_name='coordinators_{}.csv'.format(country_selected), 
  mime='text/csv'
)
