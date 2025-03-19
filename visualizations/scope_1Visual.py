import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import json
from streamlit_extras.dataframe_explorer import dataframe_explorer 

def fetch_data():
    """Fetches data from Scope1 table and processes JSON columns."""
    conn = sqlite3.connect("data/emissions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, event, fuels, consumptions, emissions, total_emission, Timestamp FROM Scope1")
    data = cursor.fetchall()
    conn.close()

    # Process JSON fields
    processed_data = []
    for row in data:
        id_, event, fuels_json, consumptions_json, emissions_json, total_emission, timestamp = row
        fuels = json.loads(fuels_json)  # Convert JSON string to list
        consumptions = json.loads(consumptions_json)
        emissions = json.loads(emissions_json)

        for fuel, consumption, emission in zip(fuels, consumptions, emissions):
            processed_data.append([id_, event, fuel, consumption, emission, total_emission, timestamp])

    return processed_data

def display():
    st.title("Scope-1 Emissions Data")

    # Fetch and prepare data
    data = fetch_data()
    df = pd.DataFrame(data, columns=["Id", "Event", "Fuel Type", "Consumption (kWh)", "Emission (kg CO₂)", "Total Emission (kg CO₂)", "Timestamp"])

    # Interactive data explorer
    dataframe = dataframe_explorer(df)
    st.dataframe(dataframe, use_container_width=True)

    # Toggle visualization
    st.write(" ")
    visualize = st.toggle("Visualize the data using Pie chart?")

    if visualize:
        fig = px.pie(df, names="Event", values="Total Emission (kg CO₂)",
                     title="Emission Distribution by Event", hole=0.3)
    else:
        fig = px.line(df, x="Event", y="Total Emission (kg CO₂)", 
                      markers=True, title="Emission Trend by Event")

    st.plotly_chart(fig, use_container_width=True)

    # Descriptive analysis
    st.subheader("Descriptive Analysis")
    des = st.selectbox("Select the column for analysis:", ["Consumption (kWh)", "Emission (kg CO₂)"])

    conn = sqlite3.connect("data/emissions.db")
    cur1 = conn.cursor()
    cur1.execute("SELECT Timestamp FROM Scope1 ORDER BY emissions DESC LIMIT 1")
    max_emission = cur1.fetchone()
    conn.close()

    max_emission_day = max_emission[0] if max_emission else "N/A"

    total_val = round(df[des].sum(), 3)
    avg_val = round(df[des].mean(), 3)
    max_val = round(df[des].max(), 3)
    min_val = round(df[des].min(), 3)
    count_val = df[des].count()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f'Total {des}', value=total_val, border=True)
    with col2:
        st.metric(label=f'Average {des}', value=avg_val, border=True)
    with col3:
        st.metric(label=f'Highest Recorded {des}', value=max_val, border=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label=f'Lowest Recorded {des}', value=min_val, border=True)
    with col5:
        st.metric(label=f'Number of {des} Records', value=count_val, border=True)
    with col6:
        st.metric(label=f"Highest {des} Recorded On", value=max_emission_day, border=True)

    # Select plot type
    plot_type = st.selectbox("Select the plot type:", ["Pie Chart", "Scatter", "Bar Plot"])

    if plot_type == "Pie Chart":
        fig = px.pie(df, values=des, names="Fuel Type", title=f"{des} Breakdown", hole=0.3)
    elif plot_type == "Scatter":
        fig = px.scatter(df, x="Fuel Type", y=des, color="Emission (kg CO₂)",
                         title=f"{des} Distribution", template="plotly_dark")
    elif plot_type == "Bar Plot":
        fig = px.bar(df, x="Fuel Type", y=des, color="Fuel Type", title=f"{des} Bar Chart")

    st.plotly_chart(fig, use_container_width=True)

