import plotly.graph_objects as go
import streamlit as st

from src.statics_enums import rarity_colors, rarity_order

group_columns = ['edition', 'edition_name', 'rarity', 'rarity_name']


def add_rarity_distribution_graph(df, title, print_unbounded=False):
    df = df.groupby(group_columns).agg({
        'num_cards': 'sum',
        'num_burned': 'sum',
        'unbound_cards': 'sum',
    }).reset_index()

    # List to hold all bars
    bars = []

    for edition in df['edition_name'].unique():
        edition_df = df[df['edition_name'] == edition]

        for rarity in rarity_order:
            rarity_df = edition_df[edition_df['rarity_name'] == rarity]

            bars.append(
                go.Bar(
                    x=rarity_df['edition_name'],
                    y=rarity_df['num_cards'],
                    name=f'{rarity} (Cards)',
                    marker=dict(color=rarity_colors[rarity]),
                    legendgroup=rarity,
                    showlegend=(edition == df['edition_name'].unique()[0]),
                    xperiodalignment="middle"
                )
            )

            if print_unbounded:
                unbound_df = rarity_df[rarity_df['unbound_cards'] > 0]
                if not unbound_df.empty:
                    bars.append(
                        go.Bar(
                            x=unbound_df['edition_name'],
                            y=unbound_df['unbound_cards'],
                            name=f'{rarity} (Unbound Cards)',
                            marker=dict(color=rarity_colors[rarity], opacity=0.5),  # Different opacity for distinction
                            legendgroup=f'unbounded {rarity}',
                            xperiodalignment="middle"
                        )
                    )

    # Plot the chart with both types of bars
    st.plotly_chart(go.Figure(
        data=bars,
        layout=go.Layout(
            title=title,
            xaxis={'title': 'Edition'},
            yaxis={'title': 'Number of Cards'},
        )
    ))
