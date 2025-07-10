import importlib
import sys

import streamlit as st
from st_pages import get_nav_from_toml, add_page_title

from src.api import spl
from src.pages import card_distribution, detailed_distribution, burned_distribution, cp_distribution
from src.util import data_util

# Optional: Reload modules during development
def reload_all():
    """Reload all src modules (for hot-reloading in development)."""
    for name in list(sys.modules):
        if name.startswith("src"):
            importlib.reload(sys.modules[name])


reload_all()  # Only needed during dev


st.set_page_config(page_title="Splinterlands Card Distribution", layout="wide")

# Fetch data
data = spl.get_card_details()
df = data_util.preprocess_data(data)

nav = get_nav_from_toml('.streamlit/pages.toml')

pg = st.navigation(nav)

add_page_title(pg)

# Dynamically call the page-specific function based on the selected page
if pg.title == "Card Distribution":
    card_distribution.get_page(df)
elif pg.title == "Detailed Distribution":
    detailed_distribution.get_page(df)
elif pg.title == "Burned BCX":
    burned_distribution.get_page(df)
elif pg.title == "CP Distribution":
    cp_distribution.get_page(df)

pg.run()
