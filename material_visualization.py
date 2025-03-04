
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


def fetch_data(table):
    conn = sqlite3.connect("emissions.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    conn.close()
    return data

def visual(table):
    data = fetch_data(table)
            # Show stored data
    st.subheader("Stored Data")
    if data:
        if table == "PetWaterBottle":
            df =pd.DataFrame(data, columns=["Id","Quantity", "Emission (kg CO₂)"])
        elif table == "Kit":
            df = pd.DataFrame(data, columns=["Id","Quantity", "Weight (kg)", "Emission (kg CO₂)"])
        elif table == "Kitems":
            df = pd.DataFrame(data, columns=["Id","Quantity", "Weight (kg)", "Emission (kg CO₂)", "Category"])
        else:
            df = pd.DataFrame(data, columns=["Id","Weight (kg)", "Emission (kg CO₂)"])
        st.table(df)
        st.subheader("Descriptive Analysis")
        st.write(df.describe())
                # Calculate insights
        total_emission = df["Emission (kg CO₂)"].sum()
        avg_emission = df["Emission (kg CO₂)"].mean()
        max_emission = df["Emission (kg CO₂)"].max()

                # Display insights
        st.write(f"**Total Emissions:** {total_emission:.2f} kg CO₂")
        st.write(f"**Average Emission per Trophy:** {avg_emission:.2f} kg CO₂")
        st.write(f"**Maximum Emission Recorded:** {max_emission:.2f} kg CO₂")

        if table == "PetWaterBottle":
            cat = st.selectbox("select option:", ["Scatter", "Bar plot"])
            if cat == "Scatter":
                fig = px.scatter(df, x="Quantity", y="Emission (kg CO₂)", title=" Emission Distribution", color='Emission (kg CO₂)', color_continuous_scale="Blues", template="plotly_dark", size_max=15)
                fig.update_traces(marker=dict(size=12, line=dict(width=1, color="black")),hovertemplate="<b>Quantity:</b> %{x} kg<br><b>CO₂ Emission:</b> %{y} kg")
                st.plotly_chart(fig, use_container_width=True)

            elif cat == "Bar plot":
                fig = px.bar(df, x="Quantity", y="Emission (kg CO₂)", text="Emission (kg CO₂)", color="Emission (kg CO₂)", color_continuous_scale="blues", labels={"Quantity": "Quantity", "Emission (kg CO₂)": "CO₂ Emission (kg)"}, title="Emission Distribution")
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(fig, use_container_width=True)
        
        elif table == "Kit":
            cat = st.selectbox("select option:", ["Scatter", "Bar plot"])
            if cat == "Scatter":
                fig = px.scatter(df, x="Weight (kg)", y="Emission (kg CO₂)", color="Emission (kg CO₂)", size="Quantity", hover_data=["Quantity"], title="Weight vs Co2 Emission", labels={"Weight": "kit weight (kg)", "Emission (kg CO₂)": "(kg CO₂) Emission (kg)"}, color_continuous_scale="Blues")
                fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="black")))
                fig.update_layout(plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(fig, use_container_width=True)
            else:
                bar_fig = px.bar(df, x="Quantity", y="Emission (kg CO₂)",
                     text="Emission (kg CO₂)", color="Emission (kg CO₂)",
                     color_continuous_scale="Blues",
                     title="Quantity vs CO₂ Emission",
                     labels={"Quantity": "Kit Quantity",
                             "Emission": "CO₂ Emission (kg)"})
                bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
                bar_fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(bar_fig, use_container_width=True)

        elif table == "Kitems":
            cat = st.selectbox("select option:", ["Scatter", "Bar plot"])
            if cat == "Scatter":
                scatter_fig = px.scatter(df, x="Weight (kg)", y="Emission (kg CO₂)",
                             color="Category", size="Quantity",
                             hover_data=["Quantity", "Category"],
                             title="Weight vs CO₂ Emission",
                             labels={"Weight": "Kit Weight (kg)",
                                     "Emission": "CO₂ Emission (kg)"},
                             color_discrete_sequence=px.colors.qualitative.Set1)
                scatter_fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="black")))
                scatter_fig.update_layout(plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(scatter_fig, use_container_width=True)
            elif cat == "Bar plot":
                bar_fig = px.bar(df, x="Category", y="Emission (kg CO₂)",
                     text="Emission (kg CO₂)", color="Category",
                     title="Category-wise CO₂ Emission",
                     labels={"Category": "Kit Category", "Emission": "CO₂ Emission (kg)"}, color_discrete_sequence=px.colors.qualitative.Pastel)
                bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
                bar_fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(bar_fig, use_container_width=True)
                # Generate Matplotlib plot
        else:
            cat = st.selectbox("select option:", ["Scatter", "Bar plot"])
            if cat == "Scatter":
                fig = px.scatter(df, x="Weight (kg)", y="Emission (kg CO₂)", title=" Emission Distribution", color='Emission (kg CO₂)', color_continuous_scale="Blues", template="plotly_dark", size_max=15)
                fig.update_traces(marker=dict(size=12, line=dict(width=1, color="black")),hovertemplate="<b>Weight:</b> %{x} kg<br><b>CO₂ Emission:</b> %{y} kg")
                st.plotly_chart(fig, use_container_width=True)

            elif cat == "Bar plot":
                fig = px.bar(df, x="Weight (kg)", y="Emission (kg CO₂)", text="Emission (kg CO₂)", color="Emission (kg CO₂)", color_continuous_scale="blues", labels={"Weight (kg)": "Weight (kg)", "Emission (kg CO₂)": "CO₂ Emission (kg)"}, title="Emission Distribution")
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No records found.")
