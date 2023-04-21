#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Participants: Antonio Requena Fernández (100452268) & Alexandru Cristian Caragea (100431203)
Course: Computer Programming of Applications
Degree: Management & Technology
"""

#Table of contents:
#1. Read the 3 excel files
#2. Create the ecsel_database.db database
#3. Add the three files as tables to the newly created database

import pandas as pd
from sqlite3 import connect

countries=pd.read_excel('/Users/requena/Documents/Computer Programming of Applications/MVP/countries.xlsx', storage_options=None)
countries.head()
participants=pd.read_excel('/Users/requena/Documents/Computer Programming of Applications/MVP/participants.xlsx', storage_options=None)
participants.head()
projects=pd.read_excel('/Users/requena/Documents/Computer Programming of Applications/MVP/projects.xlsx', storage_options=None)
projects.head()


conn = connect('ecsel_database.db')

projects.to_sql("projects", conn, if_exists = 'replace')
participants.to_sql("participants", conn, if_exists = 'replace')
countries.to_sql("countries", conn, if_exists = 'replace')

view_projects = pd.read_sql('SELECT * FROM projects', conn)
view_participants = pd.read_sql('SELECT * FROM participants', conn)
view_countries = pd.read_sql('SELECT * FROM countries', conn)