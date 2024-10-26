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

# Add data to rider or driver table
def add_rider_or_driver(name, dob, emp_id, table_name):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"INSERT INTO {table_name} (username, dob, id) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, dob, emp_id))
    conn.commit()
    conn.close()

# Fetch data from the selected table
def get_table_data(table_name):
    conn = create_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Generate PDF for download in grid format
def generate_pdf(data, table_name):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=8)

    # Add table name as title
    pdf.cell(200, 10, txt=f"Data from {table_name} table", ln=True, align='C')
    pdf.ln(10)  # Line break

    # Set column headers
    col_width = pdf.w / (len(data.columns) + 1)  # Divide page width by the number of columns
    for col in data.columns:
        pdf.cell(col_width, 10, col, border=1, align='C')
    pdf.ln()

    # Add table rows in grid format
    for index, row in data.iterrows():
        for col in data.columns:
            pdf.cell(col_width, 10, str(row[col]), border=1, align='C')
        pdf.ln()

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

    # Add Driver and Rider Section
    st.subheader("Add Driver or Rider")
    emp_name = st.text_input("Name")
    emp_dob = st.date_input("Date of Birth", value=datetime.now())
    emp_id = st.text_input("ID")

    # Two buttons for adding Driver or Rider
    if st.button("Add Driver"):
        if not emp_name or not emp_dob or not emp_id:
            st.error("All fields are mandatory. Please fill in all the details.")
        else:
            add_rider_or_driver(emp_name, emp_dob.strftime('%Y-%m-%d'), emp_id, "driver_details")
            st.success(f"Driver {emp_name} added successfully!")

    if st.button("Add Rider"):
        if not emp_name or not emp_dob or not emp_id:
            st.error("All fields are mandatory. Please fill in all the details.")
        else:
            add_rider_or_driver(emp_name, emp_dob.strftime('%Y-%m-%d'), emp_id, "rider_details")
            st.success(f"Rider {emp_name} added successfully!")

    # Dropdown for table selection
    st.subheader("View Data")
    table_options = ['rides', 'rider_details', 'driver_details']
    selected_table = st.selectbox("Select table to view data", table_options)

    # Fetch and display data based on selected table
    if selected_table:
        df = get_table_data(selected_table)
        st.dataframe(df)

        # Download selected table data as PDF
        if st.button(f"Download {selected_table} Data as PDF"):
            pdf = generate_pdf(df, selected_table)
            pdf_output = pdf.output(dest='S').encode('latin1')
            st.download_button("Download PDF", pdf_output, file_name=f"{selected_table}_data.pdf")
