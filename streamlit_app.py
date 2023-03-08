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
url = 'https://stats.oecd.org/SDMX-JSON/data/MSTI_PUB/G_PPP+G_NC+G_XGDP+G_PPPCT+G_GRO+G_XPOP+G_CVXGDP+G_BRXGDP+TP_RS+TP_RSGRO+TP_RSXLF+TP_RSXEM+TP_TT+TP_TTGRO+TP_TTXLF+TP_TTXEM+G_FBXGDP+G_FGXGDP+G_XFB+G_XFG+G_XFON+G_XFA+G_XEB+G_XEH+G_XEG+G_XEI+TH_RS+TH_WRS+TH_WRXRS+BH_RS+BH_WRS+BH_WRXRS+GH_RS+GH_WRS+GH_WRXRS+HH_RS+HH_WRS+HH_WRXRS+B_PPP+B_NC+B_XGDP+B_PPPCT+B_GRO+B_XVA+BP_RS+BP_RSGRO+BP_RSXRS+BP_RSXEI+BP_TT+BP_TTGRO+BP_TTXTT+BP_TTXEI+B_FBCT+B_FBGRO+B_FBXVA+B_XFB+B_XFG+B_XFON+B_XFA+B_DRUG+B_XDRUG+B_COMP+B_XCOMP+B_AERO+B_XAERO+B_SERV+B_XSERV+H_PPP+H_NC+H_XGDP+H_PPPCT+H_GRO+H_XFB+HP_RS+HP_RSGRO+HP_RSXRS+HP_TT+HP_TTGRO+GV_PPP+GV_NC+GV_XGDP+GV_PPPCT+GV_GRO+GV_XFB+GP_RS+GP_RSGRO+GP_RSXRS+GP_TT+GP_TTGRO+C_PPP+C_NC+C_PPPCT+C_DFXTT+C_CVXTT+C_ECOPPP+C_ECOXCV+C_HEAPPP+C_HEAXCV+C_EDUPPP+C_EDUXCV+C_SPAPPP+C_SPAXCV+C_NORPPP+C_NORXCV+C_GUFPPP+C_GUFXCV+P_TRIAD+P_PCT+P_XTRIAD+P_ICTPCT+P_BIOPCT+TD_XDRUG+TD_IDRUG+TD_EDRUG+TD_BDRUG+TD_XCOMP+TD_ICOMP+TD_ECOMP+TD_BCOMP+TD_XAERO+TD_IAERO+TD_EAERO+TD_BAERO+ECON+PI+PPP-C+GDP+GDP_PPP+VA+VA_PPP+TOTPOP+ALF+TOTEMP+INDEMP.AUS+AUT+BEL+CAN+CHL+COL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LTU+LVA+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EU27_2020+OECD+NMEC+ARG+CHN+ROU+RUS+SGP+ZAF+TWN/all?startTime=2014&endTime=2022&dimensionAtObservation=allDimensions'
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


