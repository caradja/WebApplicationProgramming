import streamlit as st
import pandas as pd

st.write("My First Streamlit Web App")
df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
st.write(df)

import streamlit as st
import pandas as pd

st.write("My First Streamlit Web App")
df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
st.write(df)

conn = sqlite3.connect('ecsel_database.db')
cur = conn.cursor()
cur.execute('SELECT Country FROM Countries')
df = pd.DataFrame(cur.fetchall(), columns = ['COUNTRYNAME'])
