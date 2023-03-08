from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px

"""
R+D Spend in the USA
"""

# Load R&D spending data
rd_data = pd.read_csv('path/to/rd_data.csv')

# Create sidebar widgets
year_range = st.sidebar.slider('Select a year range', min_value=rd_data['Year'].min(), max_value=rd_data['Year'].max(), value=(rd_data['Year'].min(), rd_data['Year'].max()))
sector = st.sidebar.selectbox('Select a sector', ['Total', 'Government', 'Business', 'Higher Education', 'Nonprofit'])

# Filter data based on sidebar widgets
rd_data_filtered = rd_data[(rd_data['Year'] >= year_range[0]) & (rd_data['Year'] <= year_range[1])]
if sector != 'Total':
    rd_data_filtered = rd_data_filtered[rd_data_filtered['Sector'] == sector]

# Create plot
fig = px.line(rd_data_filtered, x='Year', y='R&D', color='Sector')

# Display plot and title
st.plotly_chart(fig)
st.title('R&D Spending in the USA')

