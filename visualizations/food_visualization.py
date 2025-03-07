import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def fetch_food_data(table):
    try:
        conn = sqlite3.connect("data/emissions.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT FoodItem, Quantity, Emission FROM {table}")
        data = cursor.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        return []

def food_visual():
    table = st.selectbox("Select The table: ", ["FoodEmissions", "FoodItems"])
    data = fetch_food_data(table)
    
    st.subheader("🍎 Food Emission Data")

    if data:
        df = pd.DataFrame(data, columns=["FoodItem", "Quantity", "Emission (kg CO₂)"])
        st.table(df)
        
        st.subheader("Descriptive Analysis")
        st.write(df.describe())

        st.subheader("Quantity of Food items:")
        fig = st.line_chart(df, x="Quantity", y="FoodItem",  color="FoodItem")
        
        # Calculate insights
        total_emission = df["Emission (kg CO₂)"].sum()
        avg_emission = df["Emission (kg CO₂)"].mean()
        max_emission = df["Emission (kg CO₂)"].max()

        # Display insights
        st.write(f"**Total Emissions:** {total_emission:.2f} kg CO₂")
        st.write(f"**Average Emission per Food Item:** {avg_emission:.2f} kg CO₂")
        st.write(f"**Maximum Emission Recorded:** {max_emission:.2f} kg CO₂")

        st.subheader("Emissions")
        cat = st.selectbox("Select option:", ["Scatter", "Bar plot", "Line Graph"])
        
        if cat == "Scatter":
            fig = px.scatter(df, x="Quantity", y="Emission (kg CO₂)", title="Emission Distribution", color='Emission (kg CO₂)', color_continuous_scale="Blues", template="plotly_dark", size_max=15)
            fig.update_traces(marker=dict(size=12, line=dict(width=1, color="black")), hovertemplate="<b>Quantity:</b> %{x} kg<br><b>CO₂ Emission:</b> %{y} kg")
            st.plotly_chart(fig, use_container_width=True)
        
        elif cat == "Bar plot":
            fig = px.bar(df, x="FoodItem", y="Emission (kg CO₂)", text="Emission (kg CO₂)", color="Emission (kg CO₂)", color_continuous_scale="blues", labels={"FoodItem": "Food Item", "Emission (kg CO₂)": "CO₂ Emission (kg)"}, title="Emission Distribution")
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="white", font=dict(size=14))
            st.plotly_chart(fig, use_container_width=True)
        elif cat == "Line Graph":
            fig = st.line_chart(df, x="Emission (kg CO₂)", y="FoodItem", color="FoodItem",  )
    else:
        st.write("No food emission records found.")