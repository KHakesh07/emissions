import streamlit as st
from modules.sc1_emissions import display_scope1
from visualizations.scope_1Visual import display

def scope1_page():
    if "logged_in_user" not in st.session_state:
        st.error("Please login to access the dashboard.")
        return
    st.write("Scope 1 emissions refer to direct greenhouse gas (GHG) emissions from sources that an organization owns or controls. These emissions come from fuel combustion in company-owned vehicles, manufacturing processes, on-site energy generation, and equipment like boilers and furnaces. To calculate Scope 1 emissions, organizations measure fuel consumption and multiply it by an emission factor specific to the fuel type. The general formula is Scope 1 Emissions = Fuel Consumption × Emission Factor, where emission factors are provided by regulatory bodies or environmental agencies. Monitoring Scope 1 emissions is crucial for organizations to track their environmental impact, comply with regulations, and set sustainability goals. Reducing these emissions involves strategies like improving fuel efficiency, adopting cleaner technologies, switching to renewable energy sources, or optimizing operations. However, calculating Scope 1 emissions can be complex due to data collection challenges, fuel tracking issues, and variations in emission factors. While reporting these emissions helps improve environmental responsibility, some organizations may face difficulties in transitioning to low-carbon alternatives due to costs or infrastructure constraints. Despite these challenges, tracking Scope 1 emissions remains essential for organizations looking to reduce their carbon footprint and contribute to global climate change mitigation efforts.")
    display_scope1()
    display()
