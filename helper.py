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


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'] \
        .value_counts() \
        .reset_index(name='count') \
        .rename(columns={'index': 'Year'}) \
        .sort_values('Year')

    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)

    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Step 1: Count top medal winners
    top_athletes = temp_df["Name"].value_counts().reset_index()
    top_athletes.columns = ['Name', 'Medal_Count']  # rename columns properly

    # Step 2: Merge with original df to get sport & region
    merged = top_athletes.merge(df, on='Name', how='left')[['Name', 'Medal_Count', 'Sport', 'region']].drop_duplicates(
        'Name')

    return merged.head(15)


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'Games', 'NOC', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == "country"]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'Games', 'NOC', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=["Medal"])

    temp_df = temp_df[temp_df['region'] == country]

    # Step 1: Count top medal winners
    top_athletes = temp_df["Name"].value_counts().reset_index()
    top_athletes.columns = ['Name', 'Medal_Count']  # rename columns properly

    # Step 2: Merge with original df to get sport & region
    merged = top_athletes.merge(df, on='Name', how='left')[['Name', 'Medal_Count', 'Sport', ]].drop_duplicates('Name')

    return merged.head(15)


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        athlete_df = athlete_df[athlete_df['Sport'] == sport]

    return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final