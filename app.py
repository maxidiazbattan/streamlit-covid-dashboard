import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.offline as offline
import plotly.graph_objs as go
from urllib.request import urlretrieve

import streamlit as st 


def load_data():
    # OWID covid Dataset URL:
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

    # Retrive .CSV file from OWID
    urlretrieve(url, 'owid-covid-data.csv')

    # Read the file with pandas
    data = pd.read_csv('owid-covid-data.csv')

    return data

data = load_data()

st.sidebar.header ('User input')

# Side bar input 
def get_input():

    conts = ['Africa','Asia', 'Europe', 'North America', 'South America']
    continent = st.sidebar.selectbox('Choose a continent', conts)

    return continent

continent = get_input()

# Side bar topics
def get_topic():

    tpcs = ['Stringencies Indexes', 'Evolution of cases', 'Evolution of deaths','Evolution of inmunity']
    topics = st.sidebar.selectbox('Choose a topic', tpcs)

    return topics

topic = get_topic()


def data_preprocessing (data):

    df = data.copy()
    # Changing the format of the date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Setting the date column as the index of the dataframe
    df.set_index('date', inplace = True)
    # Creating 3 columns with the year, month, and day respectively
    df['day'] = df.index.day
    df['month'] = df.index.month
    df['year'] = df.index.year

    if continent:
        df = df[df['continent'] == continent]

        # Unifying units of measure
        df['total_tests_per_million'] = df['total_tests_per_thousand'] * 1000
        df['new_tests_per_million'] = df['new_tests_per_thousand'] * 1000
        df['hospital_beds_per_million'] = df['hospital_beds_per_thousand'] * 1000
        df['total_vaccinations_per_million'] = df['total_vaccinations_per_hundred'] * 10000
        df['people_vaccinated_per_million'] = df['people_vaccinated_per_hundred'] * 10000
        df['people_fully_vaccinated_per_million'] = df['people_fully_vaccinated_per_hundred'] * 10000
        df['total_boosters_per_million'] = df['total_boosters_per_hundred'] * 10000

        # Droping columns with all NA values
        df = df.drop(['icu_patients_per_million', 'hosp_patients_per_million', 'weekly_icu_admissions_per_million', 'weekly_hosp_admissions_per_million'], axis=1)

    return df

df = data_preprocessing(data)


def main():
    
    html_temp = """
    <div style="background-color:tomato;padding:10px;border-radius: 5px;">
    <h3 style="color:white;text-align:center;">Covid 19 Dashboard</h3>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    if topic == 'Stringencies Indexes':
        fig = px.line (data_frame = df, x = df.index, y = 'stringency_index', color = 'location', 
        color_discrete_sequence=px.colors.qualitative.Plotly, line_dash = 'location', 
        labels = {'stringency_index': 'Stringency index', 'date':'Date'}, title = 'Covid Stringency index')

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(hovertemplate=None)
        fig.update_layout(margin=dict(t=100, b=0, l=70, r=40),
                            #hovermode="x unified", 
                          xaxis_title=' ', yaxis_title=" ",
                          plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
                          title_font=dict(size=25, color='#a5a7ab', family="Lato, sans-serif"),
                          font=dict(color='#8a8d93'))
        st.plotly_chart(fig)
    
    if topic == 'Evolution of cases':
        fig = px.area (data_frame = df, x = df.index, y = df['new_cases_per_million'].rolling(7).mean(),
        color = 'location', labels = {'date': 'Date', 'new_cases_per_million': 'New cases per million'}, 
        title = 'Covid new cases per million per week', color_discrete_sequence=px.colors.qualitative.Plotly)

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False,categoryorder='total ascending', ticksuffix=' ', showline=False)
        fig.update_traces(hovertemplate=None)
        fig.update_layout(margin=dict(t=100, b=0, l=70, r=40), 
                                xaxis_title=' ', yaxis_title=" ",
                                plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
                                title_font=dict(size=25, color='#a5a7ab', family="Lato, sans-serif"),
                                font=dict(color='#8a8d93'))
        st.plotly_chart(fig)

    if topic == 'Evolution of deaths':
        
        fig = px.area (data_frame = df, x = df.index, y = df['new_deaths_per_million'].rolling(7).mean(), color = 'location', 
               color_discrete_sequence=px.colors.qualitative.Plotly,
               labels = {'date': 'Date', 'new_deaths_per_million': 'New deaths per million'}, title = 'Covid new deaths per million per week')

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, categoryorder='total ascending', ticksuffix=' ', showline=False)
        fig.update_traces(hovertemplate=None)
        fig.update_layout(margin=dict(t=100, b=0, l=70, r=40), 
                          xaxis_title=' ', yaxis_title=" ",
                          plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
                          title_font=dict(size=25, color='#a5a7ab', family="Lato, sans-serif"),
                          font=dict(color='#8a8d93'))
        st.plotly_chart(fig)

    if topic == 'Evolution of inmunity':
        dfi = df.groupby(by='location')['people_fully_vaccinated_per_million'].mean().reset_index()[:10]
        fig = px.histogram(data_frame = dfi, y = 'location', x = 'people_fully_vaccinated_per_million', color = 'location',
             color_discrete_sequence=px.colors.qualitative.Plotly, 
             labels = {'location': 'Country', 'people_fully_vaccinated_per_million': 'People fully vaccinated'},
             title = 'People fully vaccinated by country ')

        fig.update_yaxes(showgrid=False, ticksuffix=' ', showline=False, categoryorder='total ascending')
        fig.update_xaxes(visible=False)

        fig.update_layout(margin=dict(t=100, b=10, l=70, r=40),showlegend=False,
                        hovermode="y unified", 
                        yaxis_title=" ", 
                        plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
                        title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
                        font=dict(color='#8a8d93'),
                        hoverlabel=dict(bgcolor="#c6ccd8", font_size=13, font_family="Lato, sans-serif"))
        st.plotly_chart(fig)

if __name__=='__main__':
    main()
