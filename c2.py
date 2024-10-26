import streamlit as st
import mysql.connector
from datetime import datetime
import pandas as pd
from fpdf import FPDF

# Database connection (MySQL)
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",  # Change as needed
        user="root",
        password="Sindhu4525@",
        database="hexaemp"  # Your database
    )
    return conn

# Fetch login credentials from admin_login table
def authenticate_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# Add employee to the employees table
def add_employee(name, dob, emp_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rider_login (username, dob, id) VALUES (%s, %s, %s)", (name, dob, emp_id))
    conn.commit()
    conn.close()

# Fetch data from the selected table
def get_table_data(table_name):
    conn = create_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Generate PDF for download
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for index, row in data.iterrows():
        pdf.cell(200, 10, txt=f"ID: {row['id']}, Name: {row['username']}, Emp ID: {row['id']}", ln=True)
    return pdf

# Streamlit app starts here
st.title('Admin Page')

# Check if logged in session exists, default is False
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Login section
if not st.session_state['logged_in']:
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Logged in successfully!")
            st.session_state['logged_in'] = True  # Mark as logged in
        else:
            st.error("Invalid credentials.")

# Dashboard section
if st.session_state['logged_in']:
    st.header("Dashboard")

    # Add Employee Section
    st.subheader("Add Employee")
    emp_name = st.text_input("Employee Name")
    emp_dob = st.date_input("Date of Birth", value=datetime.now())
    emp_id = st.text_input("Employee ID")

    if st.button("Add Employee"):
        add_employee(emp_name, emp_dob.strftime('%Y-%m-%d'), emp_id)
        st.success(f"Employee {emp_name} added successfully!")

    # Dropdown for table selection
    st.subheader("Employee Data")
    table_options = ['rides', 'rider_details', 'driver_details']
    selected_table = st.selectbox("Select table to view data", table_options)

    # Fetch and display data based on selected table
    if selected_table:
        df = get_table_data(selected_table)
        st.dataframe(df)

    # Download selected table data as PDF
    if st.button("Download Data as PDF"):
        pdf = generate_pdf(df)
        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button("Download PDF", pdf_output, file_name=f"{selected_table}_data.pdf")
