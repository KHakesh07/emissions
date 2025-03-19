import sqlite3
import pandas as pd
import ast
import streamlit as st
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Connect to the database and fetch all data
def fetch_Total_data():
    conn = sqlite3.connect("data/emissions.db")
    query = "SELECT * FROM MasterEmissions;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Convert string representations of lists into actual lists
def convert_to_list(value):
    try:
        if isinstance(value, str) and value.startswith("["):
            return ast.literal_eval(value)
        return value
    except:
        return value

# Process the data
def process_data(df):
    processed_data = []
    event_cumulative = {}

    for _, row in df.iterrows():
        SourceTable, Category, Event, Description, Quantity, Weight, Emission, Timestamp = row
        
        # Convert lists
        Description = convert_to_list(Description)
        Quantity = convert_to_list(Quantity)
        Emission = convert_to_list(Emission)

        # If Description is a list, split into multiple rows
        if isinstance(Description, list):
            for desc, qty, emi in zip(Description, Quantity, Emission):
                processed_data.append([Event, desc, qty, emi])
        else:
            processed_data.append([Event, Description, Quantity, Emission])
    
    # Convert to DataFrame
    transformed_df = pd.DataFrame(processed_data, columns=["Event", "Description", "Quantity", "Emission"])

    # Compute cumulative emissions per event
    for event in transformed_df["Event"].unique():
        event_cumulative[event] = transformed_df[transformed_df["Event"] == event]["Emission"].sum()

    # Add cumulative emissions column
    transformed_df["Cumulative Emission"] = transformed_df["Event"].map(event_cumulative)

    # Assign unique row numbers
    transformed_df.insert(0, "ID", range(1, len(transformed_df) + 1))

    return transformed_df

# Visualization in Streamlit
def vis():
    st.title("Emissions Dashboard")

    df = fetch_Total_data()
    transformed_df = process_data(df)
    st.write("Processed Emission Data")
    st.dataframe(transformed_df)

    # Emission Breakdown by Event
    fig1 = px.bar(transformed_df, x="Event", y="Emission", color="Description", title="Emissions by Event")
    st.plotly_chart(fig1, use_container_width=True)

    # Pie Chart for total emissions per event
    fig2 = px.pie(transformed_df, values="Cumulative Emission", names="Event", title="Total Emission Contribution by Event")
    st.plotly_chart(fig2, use_container_width=True)

vis()
