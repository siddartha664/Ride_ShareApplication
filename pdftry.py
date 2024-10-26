import streamlit as st
import pymysql  # MySQL connector
from fpdf import FPDF
import pandas as pd

# 1. Fetch data from MySQL and add Serial Number
def get_data_from_sql():
    # Set up your MySQL connection
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Sindhu4525@",
        database="hexaemp"
    )
    query = "SELECT * FROM rides"  # Modify the query according to your need
    df = pd.read_sql(query, connection)
    connection.close()

    # Add a 'Serial Number' column starting from 1
    df.insert(0, 'Serial Number', range(1, 1 + len(df)))
    return df

# 2. Generate PDF using FPDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'SQL Data Report', 0, 1, 'C')

    def table(self, data):
        self.set_font('Arial', 'B', 10)
        # Add table header
        for col in data.columns:
            self.cell(40, 10, col, 1)
        self.ln()
        
        # Add table data
        self.set_font('Arial', '', 10)
        for i, row in data.iterrows():
            for col in data.columns:
                self.cell(40, 10, str(row[col]), 1)
            self.ln()

def generate_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.table(data)

    # Save the generated PDF to a file
    pdf_file = "output.pdf"
    pdf.output(pdf_file)
    return pdf_file

# 3. Streamlit Interface
st.title("SQL Data to PDF with Serial Numbers")
st.write("This app fetches SQL data and generates a table format PDF with Serial Numbers.")

# Fetch data from SQL
data = get_data_from_sql()

# Show the data in Streamlit
st.write("Here is the data from SQL:")
st.dataframe(data)

# Generate PDF on button click
if st.button("Generate PDF"):
    pdf_file = generate_pdf(data)

    # Provide a download link for the PDF
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name="sql_data_report_with_serial_numbers.pdf")
