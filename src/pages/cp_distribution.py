import pandas as pd
import streamlit as st
import plotly.express as px

from src.statics_enums import rarity_order, edition_mapping, foil_mapping, foil_order

group_columns = ['edition', 'edition_name', 'rarity', 'rarity_name']


def add_chart_edition_foil(df):
    # Mapping foil values to their labels
    df['foil_label'] = df['foil'].map(foil_mapping)

    # Third chart: CP per Edition and Foil
    df['foil_label'] = pd.Categorical(df['foil_label'], categories=foil_order, ordered=True)

    cp_per_foil = df.groupby(["edition_name", "foil_label"]).agg(
        cp=('cp', 'sum'),
        bcx=('bcx', 'sum'),
        num_cards=('num_cards', 'sum')
    ).reset_index()

    # Create the figure for the chart
    fig3 = px.bar(cp_per_foil, x="edition_name", y="cp", color="foil_label", barmode="group",
                  title="CP per Edition and Foil")

    # Display the chart in Streamlit
    st.plotly_chart(fig3)


def add_chart_edition_total_cp(df):
    # Apply the edition mapping to sort
    df['edition_name'] = df['edition'].map(edition_mapping)
    df['edition_name'] = pd.Categorical(df['edition_name'], categories=edition_mapping.values(), ordered=True)

    # Apply rarity order to the dataframe for sorting
    df['rarity_name'] = pd.Categorical(df['rarity_name'], categories=rarity_order, ordered=True)

    # First chart: summarize CP per edition_name
    cp_per_edition = df.groupby("edition_name", observed=False)["cp"].sum().reset_index()
    fig1 = px.bar(cp_per_edition, x="edition_name", y="cp", title="Total CP per Edition")
    st.plotly_chart(fig1)


def add_chart_edition_rarity(df):
    # Second chart: CP per edition_name and grouped by rarity
    cp_per_edition_rarity = df.groupby(["edition_name", "rarity_name"], observed=False)["cp"].sum().reset_index()
    fig2 = px.bar(cp_per_edition_rarity, x="edition_name", y="cp", color="rarity_name", barmode="group",
                  title="CP per Edition and Rarity")
    st.plotly_chart(fig2)


def get_page(df):


    # Display charts in Streamlit
    st.title('Splinterlands CP Analysis')
    add_chart_edition_total_cp(df)
    add_chart_edition_rarity(df)
    add_chart_edition_foil(df)

    with st.expander("DATA", expanded=False):
        st.dataframe(df)
