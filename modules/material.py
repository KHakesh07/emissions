import streamlit as st
import pandas as pd
import sqlite3


def insert(event, Category, Weight, Quantity, Emission):
    Conn = sqlite3.connect('data/emissions.db')
    con = Conn.cursor()
    con.execute(f"INSERT INTO Materials (event, Category, Weight, Quantity, Emission) VALUES (?, ?, ?, ?, ?)", (event, Category, Weight, Quantity, Emission))
    Conn.commit()
    Conn.close()


def show_material_calculator():
    st.subheader("Material Calculator")
    event = st.text_input("Enter the Event Name: ")

    category = st.selectbox("Select a category", ["Trophies", "Banners", "Momentoes", "Kit"])

    if category == "Trophies":
        weight = st.number_input("Enter trophy weight (kg):", min_value=0.1, step=0.1, value=1.0)
        Quantity = st.number_input(f"For How many {category} do you want to find emission?", min_value=1, step=1, value=1)
        if st.button("Calculate & Save"):
            total_emission = ((3/5)*weight*2.54) + ((2/5)*weight*1.32)
            emission = total_emission*Quantity
            insert(event, category, weight, Quantity, emission)
            st.success(f"Emission for {weight} kg trophy: {emission:.3f} kg CO₂")

    elif category == "Banners":
        weight = st.number_input("Enter weight of banner (kg):", min_value=0.1, step=0.1, value=1.0)
        Quantity = st.number_input(f"For How many {category} do you want to find emission?", min_value=1, step=1, value=1)
        if st.button("Calculate & Save"):
            emission = weight * 7.342 *Quantity
            insert(event, category, weight, Quantity, emission)
            st.success(f"Emission for {weight} kg banner: {emission:.3f} kg CO₂")

    elif category == "Momentoes":
        weight = st.number_input("Enter weight of momento (kg):", min_value=0.1, step=0.1, value=1.0)
        Quantity = st.number_input(f"For How many {category} do you want to find emission?", min_value=1, step=1, value=1)
        if st.button("Calculate & Save"):
            total_emission = ((3/5)*weight*4.98) + ((2/5)*weight*0.425)
            emission = total_emission*Quantity
            insert(event, category, weight, Quantity, emission)
            st.success(f"Emission for {weight} kg momento: {emission:.3f} kg CO₂")
    
    elif category == "Kit":
        st.write("Kit is a combination of Recycled paper kit, seed papers, pen and  palnt for felicitation")
        tab1, tab2 = st.tabs(["Calculate for Full kit", "Calculate for Individual items in kit"])
        with tab1:
            weight = st.number_input("Enter weight of kit (kg):", min_value=0.1, step=0.1, value=1.0)
            Quantity = st.number_input("Enter Quantity of kit:", min_value=1, step=1, value=1)
            if st.button("Calculate & Save", key="kit"):
                emission = (1.58+0.005+2.28+0)*weight*Quantity
                insert(event, category, weight, Quantity, emission)
                st.success(f"Emission for {Quantity} kit: {emission:.3f} kg CO₂")
        with tab2:
            category = st.selectbox("Select a category", ["Recycled paper kit", "Seed papers", "Pen",])
            table = "Kitems"
            if category == "Recycled paper kit":
                weight = st.number_input("Enter weight of item (kg):", min_value=0.1, step=0.1, value=1.0)
                Quantity = st.number_input("Enter Quantity of item:", min_value=1, step=1, value=1)
                emission = Quantity * weight *1.58
                if st.button("Calculate & Save", key="recycled_paper"):
                    insert(event, category, weight, Quantity, emission)
                    st.success(f"Emission for {Quantity} Recycled paper kit: {emission:.3f} kg CO₂")
                    
            elif category == "Seed papers":
                weight = st.number_input("Enter weight of item (kg):", min_value=0.1, step=0.1, value=1.0)   
                Quantity = st.number_input("Enter Quantity of item:", min_value=1, step=1, value=1)
                emission = Quantity * weight * 0.005
                if st.button("Calculate & Save" , key="seed"): 
                    insert(event, category, weight, Quantity, emission)
                    st.success(f"Emission for {Quantity} Seed papers: {emission:.3f} kg CO₂")

            elif category == "Pen":
                weight = st.number_input("Enter weight of item (kg):", min_value=0.1, step=0.1, value=1.0)
                Quantity = st.number_input("Enter Quantity of item:", min_value=1, step=1, value=1)
                emission = Quantity * weight * 2.28
                if st.button("Calculate & Save", key="pen"):
                    insert(event, category, weight, Quantity, emission)
                    st.success(f"Emission for {Quantity} Pen: {emission:.3f} kg CO₂")
