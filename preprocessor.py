import pandas as pd


def preprocess():
    # Load the CSVs here (if not already done)
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')

    # Use only needed columns to avoid merge issues
    region_df = region_df[['NOC', 'region']]

    # Filter Summer Olympics only
    df = df[df['Season'] == 'Summer']

    # Merge region data safely
    df = df.merge(region_df, on='NOC', how='left')

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # One-hot encode Medal columns (Gold, Silver, Bronze)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
