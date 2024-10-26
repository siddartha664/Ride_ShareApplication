import streamlit as st
import os

st.title("Rideshare Application")

st.write("Select your role:")

if st.button("Rider"):
    st.write("Redirecting to rider interface...")
    os.system("streamlit run rider.py")

if st.button("Driver"):
    st.write("Redirecting to driver interface...")
    os.system("streamlit run driver.py")

if st.button("Admin"):
    st.write("Redirecting to driver interface...")
    os.system("streamlit run admin.py")