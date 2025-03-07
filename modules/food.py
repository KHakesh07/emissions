import streamlit as st
import sqlite3

# 🍲 Food Emission Factors (kg CO₂ per kg)
FOOD_EMISSION_FACTORS = {
    "Beef": 27.0,
    "Chicken": 6.9,
    "Rice": 2.7,
    "Vegetables": 2.0,
    "Corn": 0.8,
    "Capsicum": 0.07,
    "Pine-apple": 0.12,
    "Curd": 2.66,
    "Sugar": 0.58,
    "Kaju": 2.13,
    "magach": 1.8,
    "tomato": 2.90,
    "onion": 0.5,
    "paneer": 5.1,
    "ghee": 4.2,
    "oil (l)": 1.98,
    "fresh cream": 3.94,
    "butter" : 11.52

}

# 🧮 Calculate Food Emission
def calculate_food_emission(food_item, quantity):
    if food_item in FOOD_EMISSION_FACTORS:
        return quantity * FOOD_EMISSION_FACTORS[food_item]
    return 0

options = {
    "Spicy corn salaad": (0.8*0.07), #corn and capsicum
    "Pine apple raita": (0.12*2.66*0.58), # pine apple, curd, sugar
    "Paneer tikka masala": (2.13*1.8*2.09*0.5*0.07*5.1), #kaju, magach, tomato, onion, capsicum, paneer
    "Vegetable Jalfrez": 0.72, #mix of vegetables
    "Kashmiri pulaao": (4.2*2.44*0.5), #Ghee, rice, cocktail fruit
    "Strawberry ice cream": (1.98*3.94*11.52) #oil, fresh cream, butter
}

def calculate_cur(food, quantity):
    if food in options:
        return quantity*options[food]

# 📌 Insert Food Data into DB
def insert_food_data(table, food_item, quantity, emission):
    try:
        conn = sqlite3.connect("data/emissions.db")
        c = conn.cursor()
        c.execute(f"INSERT INTO {table} (FoodItem, Quantity, Emission) VALUES (?, ?, ?)", 
                  (food_item, quantity, emission))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()


# 🥗 Show Food Calculator   
def show_food_calculator():
    tab1, tab2 = st.tabs(["Food Items", "Dishes"])
    with tab1:
        st.subheader("🥗 Food Emission Calculator")

        food_item = st.selectbox("Select Food Item", list(FOOD_EMISSION_FACTORS.keys()))
        quantity = st.number_input("Enter Quantity (kg):", min_value=0.1, step=0.1, value=1.0, key="quantity2")

        if st.button("Calculate & Save", key="btn1"):
            table = "FoodEmissions"
            emission = calculate_food_emission(food_item, quantity)
            insert_food_data(table, food_item, quantity, emission)
            st.success(f"Emission for {quantity} kg of {food_item}: {emission:.3f} kg CO₂")

    
    with tab2:
        st.subheader("Dishes& Curries")
        Curries = st.selectbox('Select the Item:', ["Spicy corn salaad", "Pine apple raita", "Paneer tikka masala", "Vegetable Jalfrez", "Kashmiri pulaao", "Strawberry ice cream"])
        Quantity = st.number_input("Enter Quantity (kg):", min_value=0.1, step=0.1, value=1.0, key="Quantity1")
        if st.button("Calculate & Save", key="bt2"):
            table = "FoodItems"
            emission = calculate_cur(Curries, Quantity)
            insert_food_data(table, Curries, Quantity, emission)
            st.success(f"Emission for {Quantity} kg of {Curries}: {emission:.3f} kg CO₂")
        