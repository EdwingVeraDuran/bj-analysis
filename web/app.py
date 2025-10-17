import streamlit as st

home_page = st.Page("home.py", title="Home", icon=":material/home:")
create_sim_page = st.Page("create_sim.py", title="Create Sim", icon=":material/add_circle:")
view_sim_page = st.Page("view_sims.py", title="View Sims", icon=":material/list_alt:")
config_page = st.Page("config.py", title="Settings", icon=":material/settings:")

pg = st.navigation([home_page, create_sim_page, view_sim_page, config_page])
st.set_page_config(
    page_title="BJ Sim",
    page_icon="🃏",
)
pg.run()
