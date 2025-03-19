import ast
import json
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import plotly.graph_objects as go

def fetch_data():
    conn = sqlite3.connect("data/emissions.db")
    query = "SELECT Category, SUM(Emission) AS TotalEmissions, Timestamp FROM MasterEmissions GROUP BY Category;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

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
        _, SourceTable, Category, Event, Description, Quantity, Weight, Emission, Timestamp = row
        
        # Convert lists
        Description = convert_to_list(Description)
        Quantity = convert_to_list(Quantity)
        Emission = convert_to_list(Emission)

        # If Description is a list, split into multiple rows
        if isinstance(Description, list):
            for desc, qty, emi in zip(Description, Quantity, Emission):
                processed_data.append([SourceTable, Category, Event, desc, qty, Weight, emi, Timestamp])
        else:
            processed_data.append([SourceTable, Category, Event, Description, Quantity, Weight, Emission, Timestamp])
    
    # Convert to DataFrame
    transformed_df = pd.DataFrame(processed_data, columns=["SourceTable", "Category", "Event", "Description", "Quantity", "Weight", "Emission", "Timestamp"])

    # Compute cumulative emissions per event
    for event in transformed_df["Event"].unique():
        event_cumulative[event] = transformed_df[transformed_df["Event"] == event]["Emission"].sum()

    # Add cumulative emissions column
    transformed_df["Cumulative Emission"] = transformed_df["Event"].map(event_cumulative)

    # Assign unique row numbers
    transformed_df.insert(0, "ID", range(1, len(transformed_df) + 1))

    return transformed_df

#############################################################################################################################
#------------------------------MAIN FUNCTION STARTS HERE--------------------------------------------------------------------#
#############################################################################################################################
def vis():

    col1, col2, col3 = st.columns(3)
    with col1:
        df = fetch_data()
        dff = pd.DataFrame(df, columns=['Category', 'Timestamp','TotalEmissions'])
        Scope1_Emission = dff[dff['Category'] == 'Scope1']['TotalEmissions'].sum()
        Scope2_Emission = dff[dff['Category'] == 'Scope2']['TotalEmissions'].sum()
        Scope3_Emission = dff[dff['Category'] == 'Scope3']['TotalEmissions'].sum()

        st.write("Emissions by Category")
        st.markdown(f"""
            <div style="padding:1px; border-radius:7px; background-color:white; color:black; text-align:center; 
            max-width: 350px; margin-bottom: 10px  ">
                <h4>Scope 1 Emissions</h4>
                <h2>{Scope1_Emission:.2f} kg CO₂</h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style="padding:1px; border-radius:7px; background-color:red; color:white; text-align:center; 
            max-width: 350px; margin-bottom: 10px ">
                <h4>Scope 2 Emissions</h4>
                <h2>{Scope2_Emission:.2f} kg CO₂</h2>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="padding:1px; border-radius:7px; background-color:white; color:black; text-align:center; 
            max-width: 350px;">
                <h4>Scope 3 Emissions</h4>
                <h2>{Scope3_Emission:.2f} kg CO₂</h2>
            </div>
        """, unsafe_allow_html=True)
        

    with col2:
        st.subheader("Emissions Breakdown by Scope")

        data = fetch_data()
        if not data.empty:
            # Create Pie Chart
            custom_colors = {
                "Scope1": "#c53b3b",
                "Scope2": "#f48080", 
                "Scope3": "white"
                }
            fig = px.pie(
                data, 
                values='TotalEmissions', 
                names='Category', 
                title='Scope 1, 2, and 3 Emissions Distribution',
                color='Category',  # Assign colors by category
                color_discrete_map=custom_colors  # Map categories to colors
            )
            st.plotly_chart(fig)
        else:
            st.warning("No records found.")
    with col3:
        st.write("Highest Emissions recorded on")
        day_Scope1_Emission = dff[dff['Category'] == 'Scope1']['Timestamp'].max()
        day_Scope2_Emission = dff[dff['Category'] == 'Scope2']['Timestamp'].max()
        day_Scope3_Emission = dff[dff['Category'] == 'Scope3']['Timestamp'].max()

        st.markdown(f"""
            <div style="padding:1px; border-radius:7px; background-color:white; color:black; text-align:center; 
            max-width: 350px; margin-bottom: 10px  ">
                <h4>Scope 1 Emissions</h4>
                <h2>{day_Scope1_Emission}</h2>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="padding:1px; border-radius:7px; background-color:red; color:white; text-align:center; 
            max-width: 350px; margin-bottom: 10px ">
                <h4>Scope 2 Emissions</h4>
                <h2>{day_Scope2_Emission}</h2>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="padding:1px; border-radius:7px; background-color:white; color:black; text-align:center; 
            max-width: 350px;">
                <h4>Scope 3 Emissions</h4>
                <h2>{day_Scope3_Emission}</h2>
            </div>
        """, unsafe_allow_html=True)

    #####################################################
    #------------TRANSFORMED DATA USED HERE-------------#
    #####################################################
    c, co = st.columns(2)
    with c:
        data = fetch_Total_data()
        transformed = process_data(data)
        d = st.selectbox("SElect", ["SourceTable", "Category", "Event", "Description"])
        fig1 = px.bar(transformed, x=d, y="Emission", title="Emissions by Category")
        fig1.update_traces(marker_color="#ffffff")
        st.plotly_chart(fig1, use_container_width=True, key="f1")
    with co:
        ###############
        # Guage Chart #
        ###############
        def get_latest_emission():
            return transformed["Cumulative Emission"].iloc[-1]  # Get latest emission value

        st.title("Total Emission")

        # Create a placeholder for the gauge chart
        gauge_placeholder = st.empty()

        # Real-time update loop (Simulating live data)
        for _ in range(100):  # Adjust this to control refresh cycles
            latest_emission = get_latest_emission()

            fig2 = go.Figure(go.Indicator(mode="gauge+number", value=latest_emission, title={'text': "Emission Levels"}, 
            gauge={'axis': {'range': [0, transformed["Cumulative Emission"].max()]}, 'bar': {'color': "red"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [50, 100], 'color': "yellow"},
                {'range': [100, transformed["Cumulative Emission"].max()], 'color': "red"}],

            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': latest_emission}
            }
        ))

        # Display the updated chart
        gauge_placeholder.plotly_chart(fig2)

        # Simulate live update (Adjust time interval for real data)
        time.sleep(2)  # Refresh every 2 seconds



    conn = sqlite3.connect("data/emissions.db")
    query = "SELECT Category, Event, SUM(Emission) AS TotalEmissions FROM MasterEmissions GROUP BY Event;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    df2 = pd.DataFrame(df,columns=['Category','Event','TotalEmissions'])
    col4, col5 = st.columns(2)
    with col4:
        st.write("Emission breakdown")
        category = st.selectbox("select", ["SourceTable", "Category", "Event", "Description","Cumulative Emission", "Timestamp"])
        fig1 = px.bar(transformed, x="Cumulative Emission", y=category, title="Emission Trend", color_discrete_sequence=["red", "blue", "green", "purple"])
        st.plotly_chart(fig1, use_container_width=True, key="f2")
    with col5:
        st.subheader("📈 Emissions Over Time")
        fig2 = px.line(transformed, x="Timestamp", y="Cumulative Emission", title="Emission Trend", color_discrete_sequence=["red", "blue", "green", "purple"],markers=True)

        # Make it interactive
        fig2.update_layout(hovermode="x unified", xaxis_title="Timestamp",yaxis_title="Cumulative Emission",legend_title="Legend",hoverlabel=dict(bgcolor="black", font_size=12, font_family="Arial"))
        st.plotly_chart(fig2, use_container_width=True)
    

    #####################################
    #---------|CHAT BOT CODE|-----------#
    ####################################
    def query_database(query):
        conn = sqlite3.connect("data/emissions.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def chatbot_response(user_input):
        if "total emissions" in user_input.lower():
            query = "SELECT SUM(Emission) AS TotalEmissions FROM MasterEmissions;"
            result = query_database(query)
            return f"Total emissions recorded: {result.iloc[0]['TotalEmissions']} kg CO₂"
    
        elif "scope" in user_input.lower():
            query = "SELECT Category, SUM(Emission) AS TotalEmissions FROM MasterEmissions GROUP BY Category;"
            result = query_database(query)
            return result.to_string(index=False)
    
        elif "event" in user_input.lower():
            query = "SELECT Event, SUM(Emission) AS TotalEmissions FROM MasterEmissions GROUP BY Event;"
            result = query_database(query)
            return result.to_string(index=False)
        
        elif "date" or "time" in user_input.lower():
            query = "SELECT Timestamp, MAX(Emission) AS TotalEmissions FROM MasterEmissions GROUP BY Event;"
            result = query_database(query)
            return result.to_string(index=False)
    
        else:
            return "I'm not sure about that. Try asking about 'total emissions', 'scope emissions', or 'event emissions'."

    # Streamlit UI
    st.title("Emissions Chatbot")

    st.subheader("Chat with Art about Emissions Data")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "clear_chat" not in st.session_state:
        st.session_state.clear_chat = False

    col1,col2, col3 = st.columns(3)
    with col1, col2:
        user_input = st.text_input("Ask about emissions:", value="" if st.session_state.clear_chat else None, key="user_input")
    
    with col3:
        if st.button("clear chat"):
            st.session_state.chat_history = []
            st.session_state.clear_chat = True
            st.rerun()

    st.session_state.clear_chat = False
    
    if user_input:
        response = chatbot_response(user_input)
        st.session_state.chat_history.append(f"  You:   {user_input}")
        st.session_state.chat_history.append(f"  Art:   {response}")
  
    
    for chat in st.session_state.chat_history[-5:]:  # Show last 5 interactions
        st.markdown(f"<div style='margin-bottom: 10px; padding: 10px; border-radius: 5px; background-color: #ba0909;'>{chat}</div>", unsafe_allow_html=True)

