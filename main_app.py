##### Importing all the required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

#### Setting title and sidebar title
st.title("Covid-19 Visualization of Nepal")
st.sidebar.title("Overview")

#### Loading the dataset
df = pd.read_csv('final.csv')
time_series = pd.read_csv('time_series.csv')
st.write(" **Map Visualization** ")

map = folium.Map(location = [28,85], zoom_start = 6.5, tiles = 'openstreetmap')
for lat, long, value, name in zip(df['Latitude'], df['Longitude'],df['Total Cases'],df['District']):
    folium.CircleMarker([lat,long],radius = value*0.02, 
    popup = ('<strong>State</strong>:' + str(name).capitalize() + '<br>''<strong>Total Cases</strong>:' + str(value)),
    color = 'cyan', fill_color = 'red', fill_opacity = 0.7).add_to(map)
folium_static(map)

##### Select the district
st.sidebar.write(" Coronavirus disease (COVID-19) is an infectious disease caused by the SARS-CoV-2 virus. Most people infected with the virus will experience mild to moderate respiratory illness and recover without requiring special treatment. However, some will become seriously ill and require medical attention. Older people and those with underlying medical conditions like cardiovascular disease, diabetes, chronic respiratory disease, or cancer are more likely to develop serious illness. Anyone can get sick with COVID-19 and become seriously ill or die at any age. The best way to prevent and slow down transmission is to be well informed about the disease and how the virus spreads. Protect yourself and others from infection by staying at least 1 metre apart from others, wearing a properly fitted mask, and washing your hands or using an alcohol-based rub frequently. Get vaccinated when it’s your turn and follow local guidance.")
select = st.sidebar.selectbox("Select a District",df['District'])

#### Get the state selected in the selectbox
district_data = df[df['District'] == select]

def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
        'Status':['Total Cases', 'Active Cases', 'Recovereds','Deaths','Readmitteds'],
        'Number of cases':(dataset.iloc[0]['Total Cases'],
        dataset.iloc[0]['Active Cases'], 
        dataset.iloc[0]['Recovereds'],
        dataset.iloc[0]['Deaths'],
        dataset.iloc[0]['Readmitteds']
        )})
    return total_dataframe

district_total = get_total_dataframe(district_data)

st.markdown("**District level analysis**")
    # if not st.checkbox('Hide Graph', False, key=1):
district_total_graph = px.bar(
district_total, 
x='Status',
y='Number of cases',
labels={'Number of cases':'Number of cases in %s' % (select)},
color='Status')
st.plotly_chart(district_total_graph)

st.markdown(" **Pie Chart visualization** ")
piechart = px.pie(df,
values = "Active Cases", 
names = "District", 
hover_data = ["Total Cases"], 
width = 700)
piechart.update_traces(textposition = 'inside', textinfo = "label+percent")  
st.plotly_chart(piechart)  

st.markdown(" **Bar Graph Visualization** ")
fig = go.Figure()
fig.add_traces(go.Bar(x = df["District"], y = df["Total Cases"]))
fig.update_layout(title = "Nepal Covid-19 Visualization", 
xaxis = dict(title = "District"), yaxis = dict(title = "Total Cases"))
st.plotly_chart(fig)

st.markdown(" **Scatter Plot Visualization** ")
fig = go.Figure()
fig.add_trace(go.Scatter(x = time_series["Date"], y = time_series["Total Cases"], mode = "lines", name = "Total Cases", line = dict(color = "blue", width =3)))
fig.add_trace(go.Scatter(x = time_series["Date"], y = time_series["Active Cases"], mode = "lines", name = "Active Cases", line = dict(color = "green", width = 2.5)))
fig.add_trace(go.Scatter(x = time_series["Date"], y = time_series["Recovered Cases"], mode = "lines", name = "Recovered Cases", line = dict(color = "maroon", width = 2.5)))
fig.add_trace(go.Scatter(x = time_series["Date"], y = time_series["Deaths"], mode = "lines", name = "Deaths", line = dict(color = "yellow", width = 2.5)))  
fig.update_layout(title = "Nepal Covid-19 Visualization")
st.plotly_chart(fig)


