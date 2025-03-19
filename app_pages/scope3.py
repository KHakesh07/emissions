import streamlit as st
from modules.material import show_material_calculator
from modules.transport import show_transport_calculator
from modules.food import show_food_calculator
from visualizations.material_visualization import visualize
from visualizations.transportation_visualization import transport_visual
from visualizations.food_visualization import food_visual
import sqlite3
import pandas as pd
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer
from visualizations.logistics import logist_vis

def scope3_page():
    if "logged_in_user" not in st.session_state:
        st.error("Please login first!")
        return
    st.write("Scope 3 emissions refer to indirect greenhouse gas (GHG) emissions that occur in a company’s value chain but are not directly controlled by the company. Unlike Scope 1 (direct emissions from owned sources) and Scope 2 (indirect emissions from purchased energy), Scope 3 includes emissions from supply chain activities such as raw material extraction, transportation, product use, waste disposal, and even employee commuting. Measuring Scope 3 emissions is essential for organizations aiming for comprehensive carbon accounting, as these emissions often constitute the largest share of a company’s total carbon footprint. Calculating Scope 3 emissions typically involves collecting data on various activities across the supply chain and applying emission factors from databases such as the Greenhouse Gas Protocol, EPA, or DEFRA. Organizations use activity-based data (e.g., liters of fuel consumed, kilometers traveled, or weight of goods transported) or spend-based data (financial expenditure on goods/services multiplied by emission factors) to estimate emissions. While calculating Scope 3 helps businesses improve sustainability, identify carbon hotspots, and meet regulatory and investor expectations, it also presents challenges. The complexity of tracking indirect emissions, reliance on supplier data, and data accuracy issues make Scope 3 calculations difficult. Additionally, not all emissions sources are equally relevant or material to a company’s operations. Despite these challenges, businesses calculate Scope 3 emissions to enhance sustainability reporting, comply with regulatory requirements, reduce supply chain risks, and improve operational efficiencies. Companies can reduce Scope 3 emissions by working with suppliers to adopt low-carbon materials, optimizing logistics, promoting circular economy practices, and encouraging sustainable customer behaviors. While some organizations may hesitate to measure Scope 3 due to the effort and cost involved, the long-term benefits—such as regulatory compliance, cost savings, and improved brand reputation—often outweigh the drawbacks. In summary, Scope 3 emissions are a critical part of carbon accounting, providing businesses with insights into their broader environmental impact. By systematically measuring and addressing Scope 3 emissions, companies can drive meaningful sustainability improvements while preparing for a future where carbon transparency and accountability are increasingly important.
")
    st.subheader("Scope 3 Emission Calculator")
    # Calculations Section: Tabs for each calculator
    calc_tab1, calc_tab2, calc_tab3 = st.tabs([
        "Material Calculator", "Transport Calculator", "Food Calculator"
    ])
    with calc_tab1:
        show_material_calculator()
    with calc_tab2:
        show_transport_calculator()
    with calc_tab3:
        show_food_calculator()

    st.header("Emission Analysis")
    # Emission Analysis Section: Tabs for visualizations
    vis_tab1, vis_tab2, vis_tab3, vis_tab4 = st.tabs([
        "Transportation","logistics", "Materials", "Foods and Vegetables"
    ],)
    with vis_tab1:
        transport_visual("TransportEmissions")
    with vis_tab2:
        logist_vis()
    with vis_tab3:
        conn = sqlite3.connect("data/emissions.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Materials")
        data1 = cur.fetchall()
        conn.close()
        st.subheader("Data:")
        df = pd.DataFrame(data1, columns=["id","event", "Category", "Weight", "Quantity", "Emission","Timestamp"])
        dataframe = dataframe_explorer(df)
        st.dataframe(dataframe, use_container_width=True)
        fig = px.pie(df, names='event', values="Emission", color="Weight", title="Emissions Breakdown", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

        category = st.selectbox("Select a category", ["Trophies", "Banners", "Momentoes", "Kit"], key="Hake")
        visualize(category)
    with vis_tab4:
        food_visual()
