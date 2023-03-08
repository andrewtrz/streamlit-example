from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

"""
R+D Spend in the USA
"""


# Set API endpoint and parameters
url = 'https://stats.oecd.org/sdmx-json/data/RDTE_USA/all/all'
params = {'startTime': '1981', 'endTime': '2020'}

# Send request to API and convert response to Pandas DataFrame
response = requests.get(url, params=params).json()
data = response['dataSets'][0]['series']
rd_data = pd.DataFrame(data).transpose()

# Extract relevant columns and reset index
rd_data = rd_data.reset_index()
rd_data[['Sector', 'Year']] = rd_data['index'].str.split('.', expand=True)
rd_data = rd_data[['Year', 'Sector', '0']]

# Rename columns
rd_data.columns = ['Year', 'Sector', 'R&D']

# Convert R&D spending to numeric data type
rd_data['R&D'] = pd.to_numeric(rd_data['R&D'], errors='coerce')

# Create sidebar widgets
year_range = st.sidebar.slider('Select a year range', min_value=rd_data['Year'].min(), max_value=rd_data['Year'].max(), value=(rd_data['Year'].min(), rd_data['Year'].max()))
sector = st.sidebar.selectbox('Select a sector', ['Total', 'Government', 'Business', 'Higher Education', 'Non-profit'])

# Filter data based on sidebar widgets
rd_data_filtered = rd_data[(rd_data['Year'] >= str(year_range[0])) & (rd_data['Year'] <= str(year_range[1]))]
if sector != 'Total':
    rd_data_filtered = rd_data_filtered[rd_data_filtered['Sector'] == sector]

# Create plot
fig = px.line(rd_data_filtered, x='Year', y='R&D', color='Sector')

# Display plot and title
st.plotly_chart(fig)
st.title('R&D Spending in the USA (OECD Data)')


