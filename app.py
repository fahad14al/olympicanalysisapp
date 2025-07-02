import preprocessor, helper
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Olympic Analysis App", layout="wide")

df = preprocessor.preprocess()

st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Dynamic title
    if selected_year == 'overall' and selected_country == 'overall':
        title = 'Overall Medal Tally'
    elif selected_year == 'overall':
        title = f'Medal Tally of {selected_country}'
    elif selected_country == 'overall':
        title = f'Medal Tally in {selected_year} Olympics'
    else:
        title = f'{selected_country} Performance in {selected_year} Olympics'

    st.title(title)
    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistic')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Nations')
        st.title(nations)

    with col3:
        st.header('Athletes')
        st.title(editions)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations Over the year')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events Over the year')
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title('Athletes Over the year')
    st.plotly_chart(fig)

    st.title("No of Events Over Time (Every Sport)")

    x = df.drop_duplicates(['Year', 'Sport', 'Event'])

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(25, 25))  # adjust size as needed

    # Create the heatmap on the ax
    sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True,
        ax=ax
    )

    # Display the plot in Streamlit
    st.pyplot(fig)
