import os
import sqlite3
import streamlit as st

def create_database():
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        conn = sqlite3.connect('data/emissions.db')
        cursor = conn.cursor()
        if os.path.exists('data/emissions.sql'):
            with open('data/emissions.sql', 'r') as file:
                sql_script = file.read()
            cursor.executescript(sql_script)
            conn.commit()
        else:
            st.warning("Database schema file not found. Database may not be properly initialized.")
    except sqlite3.Error as e:
        st.error(f"An error occurred while creating the database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()