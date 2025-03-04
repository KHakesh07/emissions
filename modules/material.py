import streamlit as st
import pandas as pd
import sqlite3

# Function to calculate emissions for trophies
def calculate_trophies(weight):
    total_emission = ((3/5)*weight*2.54) + ((2/5)*weight*1.32)
    return total_emission

# Function to calculate emissions for banners
def calculate_banners(weight):
    return weight * 7.342  # kg CO₂ per kg

def calculate_PetWB(Quantity):
    return Quantity * 5.8  # kg CO₂ per kg

# Function to calculate emissions for momento
def calculate_momento(weight):
    total_emission = ((3/5)*weight*4.98) + ((2/5)*weight*0.425)
    return total_emission

def calculate_kit(Quantity, weight):
    total_kit_emission = (1.58+0.005+2.28+0)*weight*Quantity
    return total_kit_emission


def insert_into_db(table, weight, emission):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {table} (weight, emission) VALUES (?, ?)", (weight, emission))
    conn.commit()
    conn.close()

def insert_into_PWB(table, Quantity, emission):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {table} (Quantity, emission) VALUES (?, ?)", (Quantity, emission))
    conn.commit()
    conn.close()

def insert_into_kit(table, Quantity, Weight, emission):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {table} (Quantity, Weight, Emission) VALUES (?, ?, ?)", (Quantity, Weight, emission))
    conn.commit()
    conn.close()

def insert_into_kitems(table, Quantity, Weight, emission, category):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {table} (Quantity, Weight, Emission, Category) VALUES (?, ?, ?, ?)", (Quantity, Weight, emission, category))
    conn.commit()
    conn.close()

def show_material_calculator():
    st.subheader("Material Calculator")

    catergoy = st.selectbox("Select a category", ["Trophies", "Banners", "Momentoes", "Pet Water Bottles", "Kit"])
    if catergoy == "Pet Water Bottles":
        Quantity = st.number_input("Enter the Quantity of the Pet Water Bottles:", min_value=1, step=1, value=1)
        if st.button("Calculate & Save"):
            emission = calculate_PetWB(Quantity)
            table = "PetWaterBottle"
            insert_into_PWB(table, Quantity, emission)
            st.success(f"Production Emission for {Quantity} Pet Water Bottles: {emission:.3f} kg CO₂")

    elif catergoy == "Trophies":
        weight = st.number_input("Enter trophy weight (kg):", min_value=0.1, step=0.1, value=1.0)
        if st.button("Calculate & Save"):
            emission = calculate_trophies(weight)
            insert_into_db(catergoy, weight, emission)
            st.success(f"Emission for {weight} kg trophy: {emission:.3f} kg CO₂")

    elif catergoy == "Banners":
        weight = st.number_input("Enter weight of banner (kg):", min_value=0.1, step=0.1, value=1.0)
        if st.button("Calculate & Save"):
            emission = calculate_banners(weight)
            insert_into_db(catergoy, weight, emission)
            st.success(f"Emission for {weight} kg banner: {emission:.3f} kg CO₂")

    elif catergoy == "Momentoes":
        weight = st.number_input("Enter weight of momento (kg):", min_value=0.1, step=0.1, value=1.0)
        if st.button("Calculate & Save"):
            emission = calculate_momento(weight)
            insert_into_db(catergoy, weight, emission)
            st.success(f"Emission for {weight} kg momento: {emission:.3f} kg CO₂")
    
    elif catergoy == "Kit":
        st.write("Kit is a combination of Recycled paper kit, seed papers, pen and  palnt for felicitation")
        tab1, tab2 = st.tabs(["Calculate for Full kit", "Calculate for Individual items in kit"])
        with tab1:
            weight = st.number_input("Enter weight of kit (kg):", min_value=0.1, step=0.1, value=1.0)
            Quantity = st.number_input("Enter Quantity of kit:", min_value=1, step=1, value=1)
            if st.button("Calculate & Save", key="kit"):
                emission = calculate_kit(Quantity, weight)
                insert_into_kit(catergoy, Quantity, weight, emission)
                st.success(f"Emission for {Quantity} kit: {emission:.3f} kg CO₂")
        with tab2:
            catergoy = st.selectbox("Select a category", ["Recycled paper kit", "Seed papers", "Pen",])
            table = "Kitems"
            if catergoy == "Recycled paper kit":
                weight = st.number_input("Enter weight of item (kg):", min_value=0.1, step=0.1, value=1.0)
                Quantity = st.number_input("Enter Quantity of item:", min_value=1, step=1, value=1)
                emission = Quantity * weight *1.58
                if st.button("Calculate & Save", key="recycled_paper"):
                    insert_into_kitems(table, Quantity, weight, emission, catergoy)
                    st.success(f"Emission for {Quantity} Recycled paper kit: {emission:.3f} kg CO₂")
                    
            elif catergoy == "Seed papers":
                weight = st.number_input("Enter weight of item (kg):", min_value=0.1, step=0.1, value=1.0)   
                Quantity = st.number_input("Enter Quantity of item:", min_value=1, step=1, value=1)
                emission = Quantity * weight * 0.005
                if st.button("Calculate & Save" , key="seed"): 
                    insert_into_kitems(table, Quantity, weight, emission, catergoy)
                    st.success(f"Emission for {Quantity} Seed papers: {emission:.3f} kg CO₂")

            elif catergoy == "Pen":
                pen_weight = st.number_input("Enter weight of item (kg):", min_value=0.1, step=0.1, value=1.0)
                Quantity = st.number_input("Enter Quantity of item:", min_value=1, step=1, value=1)
                emission = Quantity * pen_weight * 2.28
                if st.button("Calculate & Save", key="pen"):
                    insert_into_kitems(table, Quantity, pen_weight, emission, catergoy)
                    st.success(f"Emission for {Quantity} Pen: {emission:.3f} kg CO₂")

    if st.button("Back to main menu"):
        st.session_state.page = "main"
        st.rerun() # force the app to show the main menu
