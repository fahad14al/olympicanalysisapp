import numpy as np


def medal_tally(df):
    # Remove duplicates
    medal_tally = df.drop_duplicates(subset=['Team', 'Games', 'NOC', 'City', 'Sport', 'Event', 'Medal'])

    # Group by country and sum medals
    medal_tally = medal_tally.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']] \
        .sort_values('Gold', ascending=False).reset_index()

    # Add total column
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    if 'region' in df.columns:
        country = np.unique(df['region'].dropna().values).tolist()
        country.sort()
        country.insert(0, 'overall')
    else:
        country = ['overall']

    return years, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'Games', 'NOC', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'overall' and country == 'overall':
        temp_df = medal_df
    elif year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']] \
            .sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']] \
            .sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'] \
        .value_counts() \
        .reset_index(name='count') \
        .rename(columns={'index': 'Year'}) \
        .sort_values('Year')

    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)

    return nations_over_time
