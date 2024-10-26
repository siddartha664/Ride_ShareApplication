import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',         # Change if your database is hosted elsewhere
            user='root',              # Replace with your MySQL username
            password='Sindhu4525@',   # Replace with your MySQL password
            database='hexaemp'        # Replace with your database name
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to validate driver login and get driver ID
def validate_rider(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT ID FROM driver_login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()  # Fetch the driver ID
        cursor.close()
        connection.close()
        return result  # Return the result row if user is found (only the ID)
    return None

# Function to update driver details
def update_rider_details(driver_id, source, destination, pickup_time, date, vehicle_type, seating_capacity):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
            UPDATE driver_details 
            SET source = %s, destination = %s, pickup_time = %s, date_t = %s, vehicle_t = %s, seating_capacity = %s 
            WHERE ID = %s
        """
        cursor.execute(query, (source, destination, pickup_time, date, vehicle_type, seating_capacity, driver_id))
        connection.commit()  # Commit the changes
        cursor.close()
        connection.close()
        st.success("Ride details updated successfully!")

# Function to fetch the last requested ride details based on driver_id
def get_requested_received(driver_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get a dictionary-like result
        query = """
        SELECT * FROM rides 
        WHERE ride_id = %s 
        ORDER BY sno DESC  
        LIMIT 1;
        """
        cursor.execute(query, (driver_id,))
        ride_details = cursor.fetchone()  # Fetch only the last row
        cursor.close()
        connection.close()
        return ride_details  # Return the ride details if found
    else:
        st.error("Failed to connect to the database.")
        return None

# Function to update ride status (Accept or Complete)
def update_ride_status(ride_id, new_status):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "UPDATE rides SET status = %s WHERE ride_id = %s"
        cursor.execute(query, (new_status, ride_id))
        connection.commit()
        cursor.close()
        connection.close()
        st.success(f"Ride status updated to {new_status}.")

# Function to display the driver dashboard after login
def driver_dashboard(driver_id):
    st.title("Driver Dashboard")

    # Input fields for driver details
    with st.form("driver_form"):
        st.subheader("Provide Ride Details")
        
        source = st.text_input("Source")
        destination = st.text_input("Destination")
        time = st.text_input("Time (HH:MM)")
        date = st.date_input("Date")
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Bike", "Van", "Bus"])
        seating_capacity = st.number_input("Seating Capacity", min_value=1, max_value=20, step=1)
        
        # Submit button for the form
        submit_button = st.form_submit_button("Submit")

    # Validate input fields
    if submit_button:
        if not source or not destination or not time or not vehicle_type or seating_capacity <= 0:
            st.error("All fields must be filled correctly.")
        else:
            # Updating the driver details in the database
            update_rider_details(driver_id, source, destination, time, date, vehicle_type, seating_capacity)

    # Fetch and display requested ride details
    requested_ride = get_requested_received(driver_id)

    if requested_ride:
        st.subheader("Requested Ride Details")
        st.write(f"**Ride ID**: {requested_ride['ride_id']}")
        st.write(f"**Driver Name**: {requested_ride['driver_name']}")
        st.write(f"**Source**: {requested_ride['source']}")
        st.write(f"**Destination**: {requested_ride['destination']}")
        st.write(f"**Date**: {requested_ride['date']}")
        st.write(f"**Time**: {requested_ride['time']}")
        st.write(f"**Rating**: {requested_ride['rating']}")
        st.write(f"**Total Trips**: {requested_ride['total_number_of_trips']}")
        st.write(f"**Vehicle**: {requested_ride['Vehicle']}")
        st.write(f"**Seating Capacity**: {requested_ride['seating_capacity']}")
        st.write(f"**Contact**: {requested_ride['contact']}")
        st.write(f"**Distance**: {requested_ride['distance']} km")
        st.write(f"**Price**: ₹{requested_ride['price']}")
        st.write(f"**Status**: {requested_ride['status']}")

        # Display buttons based on ride status
        if requested_ride['status'] == 'pending':
            if st.button("Accept Ride"):
                update_ride_status(requested_ride['ride_id'], 'accepted')
        elif requested_ride['status'] == 'paid':
            if st.button("Complete Ride"):
                update_ride_status(requested_ride['ride_id'], 'completed')

# Function to display the driver login page
def rider_page():
    st.title("Driver Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        rider_data = validate_rider(username, password)
        if rider_data:
            st.session_state['logged_in'] = True  # Set login state to True
            st.session_state['driver_id'] = rider_data[0]  # Get the driver ID from the result
            st.success("Login successful! Welcome to the Driver Dashboard!")
        else:
            st.error("Invalid username or password. Please try again.")

# Main function to control the app flow
def main():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False  # Initialize session state for login
    
    if st.session_state['logged_in']:
        driver_id = st.session_state['driver_id']  # Get the driver ID from session state
        driver_dashboard(driver_id)  # Show the dashboard if logged in
    else:
        rider_page()  # Show the login page if not logged in

if __name__ == "__main__":
    main()
