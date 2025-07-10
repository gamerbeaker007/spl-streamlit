import pandas as pd

from src.api import spl
from src.statics_enums import rarity_mapping, edition_mapping
from src.util import card_util

cp_per_bcx = [
    [5, 125, 625],  # Common (1), Rare (2), Epic (3), Legendary (4) for Regular, Gold, Black
    [20, 500, 2500],
    [100, 2500, 12500],
    [500, 12500, 62500]
]

CP_MULTIPLIERS = {
    'gladius': {
        'Regular': 6,
        'Gold': 12
    },
    'untamed': {
        'Regular': 2,
        'Gold': 4
    },
    'untamed_promo': {
        'Regular': 6,
        'Gold': 12
    },
    'alpha': {
        'Regular': 6,
        'Gold': 12
    },
    'beta': {
        'Regular': 3,
        'Gold': 6
    },
    'beta_promo': {
        'Regular': 6,
        'Gold': 12
    }

}


def preprocess_data(data):
    df = get_all_distributions_df(data)
    df = make_columns_as_int(df)
    df = add_rarity_names(df)
    df = add_edition_names(df)
    df = add_bcx(df)
    df = add_cp(df)
    return df


def get_all_distributions_df(df):
    # Prepare and process data (same as in Dash code)
    all_distributions = []
    for index, row in df.iterrows():
        for dist in row['distribution']:
            dist['name'] = row['name']
            dist['rarity'] = row['rarity']
            dist['tier'] = row['tier']
            all_distributions.append(dist)

    df = pd.DataFrame(all_distributions)
    return df


def make_columns_as_int(df):
    df['num_cards'] = df['num_cards'].astype(int)
    df['num_burned'] = df['num_burned'].astype(int)
    df['unbound_cards'] = df['unbound_cards'].astype(int)
    return df


def add_rarity_names(df):
    df['rarity_name'] = df['rarity'].map(rarity_mapping)
    return df


def add_edition_names(df):
    df['edition_name'] = df['edition'].map(edition_mapping)
    return df


def add_bcx(df):
    settings = spl.get_settings()
    df['bcx'] = df.apply(lambda r: card_util.determine(r, settings, 'total_xp'), axis=1)
    df['burned_bcx'] = df.apply(lambda r: card_util.determine(r, settings, 'total_burned_xp'), axis=1)
    return df


def get_multiplier(row, foil_type):
    # Check for specific editions and tiers first
    if row['edition'] >= 7 or row['tier'] > 4:  # from Chaos legion its default
        return 1
    elif row['edition'] == 6:  # Gladius units
        return CP_MULTIPLIERS['gladius'][foil_type]
    elif row['edition'] == 4 or row['tier'] == 4:  # Untamed or untamed rewards
        return CP_MULTIPLIERS['untamed'][foil_type]
    elif row['tier'] == 3:  # Special treatment for untamed promos
        return CP_MULTIPLIERS['untamed_promo'][foil_type]
    elif row['edition'] == 0 or (row['edition'] == 2 and row['card_detail_id'] < 100):  # Alpha
        return CP_MULTIPLIERS['alpha'][foil_type]
    elif row['edition'] == 2 and row['card_detail_id'] < 206:  # Beta promos
        return CP_MULTIPLIERS['beta_promo'][foil_type]
    else:  # Beta
        return CP_MULTIPLIERS['beta'][foil_type]


def calculate_cp(row):
    # Determine the foil type (Regular, Gold, Black)
    foil_type = 'Regular' if row['foil'] == 0 else ('Gold' if row['foil'] == 1 else 'Black')

    # Map rarity to index: 1=Common, 2=Rare, 3=Epic, 4=Legendary
    rarity_index = row['rarity'] - 1  # Adjust for 1-based index in `rarity`
    # Get the CP per BCX based on rarity and foil type
    cp = cp_per_bcx[rarity_index][['Regular', 'Gold', 'Black'].index(foil_type)]
    # Get the appropriate multiplier based on the edition and tier
    multiplier = get_multiplier(row, foil_type)

    # Calculate the total CP
    total_cp = cp * row['bcx'] * multiplier
    return total_cp


def add_cp(df):
    df['cp'] = df.apply(calculate_cp, axis=1)
    return df
