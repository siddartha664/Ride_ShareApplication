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

# Function to validate user login and get rider ID
def validate_rider(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT ID FROM rider_login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()  # Fetch the rider ID
        cursor.close()
        connection.close()
        return result  # Return the result row if user is found (only the ID)
    return None

# Function to update rider details
def update_rider_details(rider_id, source, destination, pickup_time):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "UPDATE rider_details SET source = %s, destination = %s, pickup_time = %s WHERE ID = %s"
        cursor.execute(query, (source, destination, pickup_time, rider_id))
        connection.commit()  # Commit the changes
        cursor.close()
        connection.close()
        st.success("Ride details updated successfully!")

# GenAI function to generate available ride orders
def genai(source, destination, pickup_time):
    # This function simulates AI-powered ride suggestions.
    # In actual implementation, this would use a GenAI model to process and return rides.
    # For now, it's returning a placeholder list of rides.
    
    return [
        {"ride_id": 101, "driver_name": "John Doe", "ride_time": "10:30 AM", "price": "$15"},
        {"ride_id": 102, "driver_name": "Jane Smith", "ride_time": "09:00 AM", "price": "$18"},
    ]

# Function to display the rider dashboard after login
def rider_dashboard(rider_id):
    st.title("Rider Dashboard")

    # 1. Source, Destination, Pickup Time, and Submit Button
    st.subheader("Book a Ride")
    source = st.text_input("Enter Source Location")
    destination = st.text_input("Enter Destination Location")
    pickup_time = st.text_input("Select Pickup Time")

    if st.button("Submit"):
        if source and destination and pickup_time:
            st.success(f"Ride from {source} to {destination} at {pickup_time} requested!")
            update_rider_details(rider_id, source, destination, pickup_time)  # Update rider details
            
            # Call the genai function to get available rides
            available_rides = genai(source, destination, pickup_time)
            if available_rides:
                st.subheader("Available Ride Orders")
                for ride in available_rides:
                    ride_id = ride["ride_id"]
                    driver_name = ride["driver_name"]
                    ride_time = ride["ride_time"]
                    price = ride["price"]
                    st.write(f"Ride ID: {ride_id}, Driver: {driver_name}, Time: {ride_time}, Price: {price}")
                    if st.button(f"Request Ride {ride_id}", key=ride_id):
                        st.success(f"Ride requested with {driver_name} at {ride_time}!")
            else:
                st.info("No available rides for the selected route.")
        else:
            st.error("Please enter source, destination, and pickup time.")

    # 3. Request Details Button at the Top Right Corner
    st.sidebar.button("Request Details")

# Rider login page
def rider_page():
    st.title("Rider Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        rider_data = validate_rider(username, password)
        if rider_data:
            st.session_state['logged_in'] = True  # Set login state to True
            st.session_state['rider_id'] = rider_data[0]  # Get the rider ID from the result
            st.success("Login successful! Welcome to the Rider Dashboard!")
        else:
            st.error("Invalid username or password. Please try again.")

# Main function to control the app flow
def main():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False  # Initialize session state for login
    
    if st.session_state['logged_in']:
        rider_id = st.session_state['rider_id']  # Get the rider ID from session state
        rider_dashboard(rider_id)  # Show the dashboard if logged in
    else:
        rider_page()  # Show the login page if not logged in

if __name__ == "__main__":
    main()
