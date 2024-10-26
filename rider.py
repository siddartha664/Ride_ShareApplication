import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
def update_rider_details(rider_id, source, destination, pickup_time, pickup_date):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "UPDATE rider_details SET source = %s, destination = %s, pickup_time = %s, date = %s WHERE ID = %s"
        cursor.execute(query, (source, destination, pickup_time, pickup_date, rider_id))
        connection.commit()  # Commit the changes
        cursor.close()
        connection.close()
        st.success("Ride details updated successfully!")

# GenAI function to generate available ride orders (mock)
def genai(source, destination, pickup_time, pickup_date):
    # Returning a list of rides with updated information as per the provided details



    import os
    import google.generativeai as genai
    import mysql.connector
    from mysql.connector import Error


    def fetch_and_format_data():
        # Establishing the connection to the MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Sindhu4525@',
            database='hexaemp'
        )
        
        cursor = conn.cursor()

        # Fetch all data from the 'driver_details' table
        cursor.execute("SELECT * FROM driver_details")
        results = cursor.fetchall()  # Fetch all rows from the query result

        responses = []
        if results:
            for result in results:
                # Convert each row into a formatted string
                response = f"{result} "
                responses.append(response)

            # Close the cursor and connection after fetching the data
            cursor.close()
            conn.close()
            
            return responses  # Return a list of formatted responses
        else:
            cursor.close()
            conn.close()
            
            return ["No matching data found."]

    # Call the function and get the formatted responses
    formatted_responses = fetch_and_format_data()

    # Use join() to efficiently build the result string from all rows
    input_driv = "".join(formatted_responses)

    # Define the value of b
   
    user_in = (source, destination, pickup_time, pickup_date)
    
    user_in = str(user_in)
   
    # Append b to a
    user_in =  input_driv + "match with a "+ user_in
    

    # Print the final result


    import os
    import google.generativeai as genai
    import json

    genai.configure(api_key="AIzaSyCFYC3YudT7STlsvBazCvfkPuyKEyt5jQE")

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "i will provide some details with make best match with low cost ride for rider and shortest distance \n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Please tell me the details! I need information to help you find the best match. \n\nFor example, tell me:\n\n* **Where are you starting from?** (City, state, or specific address)\n* **Where are you going?** (City, state, or specific address)\n* **What time are you traveling?** (This will affect traffic and availability)\n* **How many people are traveling?** (This will influence the size of the vehicle needed)\n* **What kind of luggage do you have?** (This will help determine if you need a car with extra cargo space)\n* **What is your budget?** \n\nOnce I have this information, I can use my knowledge of ride-sharing services and transportation options to recommend the best, low-cost, and shortest distance option for you. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "('a1', 'siddhu', 'chennai', 'warangal', '24/9/2024', '09:00 PM', '4.6', '12', 'car', '7', '8978242155') ('a2', 'hruday', 'avadi', 'chennai, central', '25/9/2024', '02 : pm', '4.1', '10', 'car', '5', '7585411231') ('a3', 'akhil', 'chennai, central', 'veltech university', '28/9/2024', '06 : 00 AM', '4.2', '10', 'car', '5', '7325411231') ('a4', 'ashok', 'chennai', 'hyderabad', '22/9/2024', '05 : 00 pm', '4', '7', 'bike', '5', '9325411231') match with a ('avadi', 'warangal', '11:00 PM'), ....  match with a (avadi, warangal,2024-09-24,10:00pm) \nit is in the format of (id, name, source, destination, date, time,rating, no_of_rides, vechile_type, seating_capacity, contact_details) and make a best  match with (source, destination, date, time)\nfind best match and send it is output ",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Okay, I can help you match these riders with the requested trip based on the provided information.\n\nHere's how we'll approach this:\n\n1. **Data Extraction:** I'll first extract the relevant information from the rider data (source, destination, date, and time) and compare it with the requested trip details.\n2. **Matching Criteria:**  We'll prioritize matching riders whose source and destination closely align with the requested trip. We'll then look for the best date and time match. \n3. **Output:** I'll provide you with the best matching rider based on the information you've given. \n\n**Data Extraction and Matching:**\n\n* **Requested Trip:** (avadi, warangal, 2024-09-24, 10:00 pm)\n\n* **Rider Data Analysis:**\n\n   * **Rider 'a1':**  (chennai, warangal, 24/9/2024, 09:00 PM) - This is a close match, as the destination is the same, and the date and time are very similar.\n   * **Rider 'a2':**  (avadi, chennai, central, 25/9/2024, 02 : pm) - The destination is different, so this is not a good match.\n   * **Rider 'a3':**  (chennai, central, veltech university, 28/9/2024, 06 : 00 AM) - Destination and date are a mismatch.\n   * **Rider 'a4':**  (chennai, hyderabad, 22/9/2024, 05 : 00 pm) - Destination and date are a mismatch.\n\n**Best Match:**\n\nBased on the analysis, **Rider 'a1' (siddhu)** is the best match for the requested trip.  \n\n**Output:**\n\n(a1, siddhu, chennai, warangal, 24/9/2024, 09:00 PM, 4.6, 12, car, 7, 8978242155)\n\nThis rider has the same destination (warangal), a very close date and time match (24/9/2024, 09:00 PM), making them the most suitable candidate for your trip. \n\n**Important Notes:**\n\n* **Additional Factors:**  You might want to consider other factors like the rider's rating, the vehicle type, and seating capacity when making your final decision.\n* **Flexibility:**  If you are flexible with the time, it might be worth reaching out to other riders whose dates and times are slightly off, but who are otherwise a good match. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "i need only output int his format \"\"ride_id\": \"a1\", \"driver_name\": \"John Doe\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"12/07/2024\",\n         \"time\": \"10:00 PM\", \"rating\": \"4.2\", \"total_number_of_trips\": \"10\", \"Vehicle\": \"car\", \"seating_capacity\": \"5\",\n         \"contact\": \"8978242155\", \"price\": \"19\"\"\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "You got it! Here's the output in the format you requested:\n\n```json\n{\n  \"ride_id\": \"a1\",\n  \"driver_name\": \"siddhu\",\n  \"source\": \"chennai\",\n  \"destination\": \"warangal\",\n  \"date\": \"24/9/2024\",\n  \"time\": \"09:00 PM\",\n  \"rating\": \"4.6\",\n  \"total_number_of_trips\": \"12\",\n  \"Vehicle\": \"car\",\n  \"seating_capacity\": \"7\",\n  \"contact\": \"8978242155\",\n  \"price\": \"19\" \n}\n```\n\n**Explanation:**\n\n* **ride_id:**  \"a1\" (from your input data)\n* **driver_name:** \"siddhu\" (from your input data)\n* **source:** \"chennai\" (from your input data)\n* **destination:** \"warangal\" (from your input data)\n* **date:** \"24/9/2024\" (from your input data)\n* **time:** \"09:00 PM\" (from your input data)\n* **rating:** \"4.6\" (from your input data)\n* **total_number_of_trips:** \"12\" (from your input data)\n* **Vehicle:** \"car\" (from your input data)\n* **seating_capacity:** \"7\" (from your input data)\n* **contact:** \"8978242155\" (from your input data)\n* **price:** \"19\"  (This is a placeholder, as you didn't provide pricing information in the input. You would need to determine this price based on factors like distance, time, etc.)\n\n**Remember:** This output is based on the data you provided and the format you specified. To calculate the price, you'll need to develop a pricing model for your rides. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "the output should be in this format only\n=============================\ni need only this format {\"ride_id\": \"a1\", \"driver_name\": \"John Doe\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"12/07/2024\",\n\"time\": \"10:00 PM\", \"rating\": \"4.2\", \"total_number_of_trips\": \"10\", \"Vehicle\": \"car\", \"seating_capacity\": \"5\",\n\"contact\": \"8978242155\", \"price\": \"19\"}\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "You are absolutely right! I apologize for the formatting error in my previous response. \n\nHere is the correct output in the exact format you specified:\n\n```json\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"price\": \"19\"} \n```\n\nThis output follows your exact format, including the double quotes, commas, and colons. I'll be more careful with formatting in the future. \n\nLet me know if you have any other questions! \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "dont print a single text except output",
        ],
        },
        {
        "role": "model",
        "parts": [
            "```json\n{\"",
        ],
        },
        {
        "role": "user",
        "parts": [
            "dont give \"You are absolutely right! I apologize for the formatting error in my previous response.\nHere is the correct output in the exact format you specified:\" such \nfive only this\n===================\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"price\": \"19\"}",
        ],
        },
        {
        "role": "model",
        "parts": [
            "```json\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"price\": \"19\"}\n``` \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "('a1', 'siddhu', 'chennai', 'warangal', '24/9/2024', '09:00 PM', '4.6', '12', 'car', '7', '8978242155') ('a2', 'hruday', 'anai, central', 'veltech university', '28/9/2024', '06 : 00 AM', '4.2', '10', 'car', '5', '7325411231') ('a4', 'ashok', 'chennai', 'hyderabad', '22/9/2024', '05 : 00 pm', '4', '7', 'bike', '5', '9325411231') match with a ('avadi', 'warangal', '11:00 PM') match with (chennai, wrangal,2024-09-25,10:00pm)",
        ],
        },
        {
        "role": "model",
        "parts": [
            "```json\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"price\": \"19\"}\n``` \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "calculate distance average distance between two cities and add new column in above file to km and calcuate the price and update according to that 1 km is 5 update like this in price column",
        ],
        },
        {
        "role": "model",
        "parts": [
            "You're asking for a complex task that requires:\n\n1. **Distance Calculation:**  You need a way to calculate the distance between cities. This usually involves using a mapping API or a database of city distances.\n2. **Data Manipulation:** You need to add a new column to your JSON data and populate it with the calculated distance.\n3. **Price Calculation:**  You need to use the distance and a pricing rule (1 km = 5) to calculate the price for each ride. \n\n**Here's a breakdown of the process (assuming you have a way to calculate distances):**\n\n**1. Calculate Distances:**\n\n*   Use a mapping API like Google Maps API, or a database of city distances to get the distance between the source and destination for each ride. \n\n**2.  Update JSON Data:**\n\n*   You'll need to use a programming language like Python or JavaScript to manipulate the JSON data. \n*   Read the JSON data into a data structure (e.g., a Python dictionary or a JavaScript object).\n*   Add a new key-value pair to each ride object: `\"distance\": <calculated_distance>`. \n*   Calculate the price using: `price = distance * 5`\n*   Update the \"price\" key-value pair in each ride object.\n*   Write the updated JSON data to a file.\n\n**Example Python Code (requires a distance calculation function):**\n\n```python\nimport json\n\ndef calculate_distance(source, destination):\n  # Replace this with your actual distance calculation logic\n  # Using a mapping API or a distance database\n  return 100 # Example distance for now\n\nrides = [\n    {\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"price\": \"19\"}\n]\n\nfor ride in rides:\n  distance = calculate_distance(ride[\"source\"], ride[\"destination\"])\n  ride[\"distance\"] = distance\n  ride[\"price\"] = distance * 5\n\nwith open('updated_rides.json', 'w') as f:\n  json.dump(rides, f, indent=4)\n```\n\n**Remember:**\n\n*   You'll need to replace the placeholder distance calculation function (`calculate_distance`) with your actual distance calculation logic.\n*   The pricing rule (1 km = 5) is an example, you can customize it to fit your needs.\n\nLet me know if you have any more questions, and I'll do my best to help! \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "i need in this format as output dont give me code\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"price\": \"19\"}",
        ],
        },
        {
        "role": "model",
        "parts": [
            "```json\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}\n``` \n\n**Explanation:**\n\n* **distance:** I added a new key \"distance\" with a value of \"500\" (assuming the distance between Chennai and Warangal is 500 km). You would need to replace this with the actual calculated distance.\n* **price:** I updated the \"price\" to \"2500\" based on the distance and the 1 km = 5 price rule (500 * 5 = 2500). \n\n\n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "i aslo don't need explaination just that only\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}",
        ],
        },
        {
        "role": "model",
        "parts": [
            "{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}",
        ],
        },
        {
        "role": "user",
        "parts": [
            "it printing like this \n```json\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}\n```\ni need like this\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}",
        ],
        },
        {
        "role": "model",
        "parts": [
            "You are absolutely right!  I apologize for the formatting issue. I'm still under development and learning to be more precise with my outputs.\n\nHere is the output exactly as you requested:\n\n```json\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}\n```\n\nI will try my best to be more accurate in the future!  Please let me know if you have any other questions. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "just give it dont this\n{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}",
        ],
        },
        {
        "role": "model",
        "parts": [
            "{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}",
        ],
        },
        {
        "role": "user",
        "parts": [
            "{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}",
        ],
        },
        {
        "role": "model",
        "parts": [
            "{\"ride_id\": \"a1\", \"driver_name\": \"siddhu\", \"source\": \"chennai\", \"destination\": \"warangal\", \"date\": \"24/9/2024\", \"time\": \"09:00 PM\", \"rating\": \"4.6\", \"total_number_of_trips\": \"12\", \"Vehicle\": \"car\", \"seating_capacity\": \"7\", \"contact\": \"8978242155\", \"distance\": \"500\", \"price\": \"2500\"}"
        ],
        },
    ]
    )
    response = chat_session.send_message(user_in)

    asp = response.text
    cleaned_a = asp.replace('```json', '').replace('```', '').strip()

    # The response is cleaned and converted to JSON
    a_json = json.loads(cleaned_a)

    # No need to use json.loads() again since a_json is already a dictionary
    available_ride = a_json
    

    # Output the dictionary
    return available_ride

# Function to get requested ride details
def get_requested_ride_details(passenger_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get a dictionary-like result
        query = """
        SELECT * FROM rides 
        WHERE passenger_id = %s 
        ORDER BY sno DESC  
        LIMIT 1;
        """
        cursor.execute(query, (passenger_id,))
        ride_details = cursor.fetchone()  # Fetch only the last row
        cursor.close()
        connection.close()
        return ride_details  # Return the ride details if found
    else:
        st.error("Failed to connect to the database.")
        return None
    
# Rider dashboard function
def rider_dashboard(rider_id):
    st.title("Rider Dashboard")

    # 1. Source, Destination, Pickup Time, Pickup Date, and Submit Button
    st.subheader("Book a Ride")
    source = st.text_input("Enter Source Location")
    destination = st.text_input("Enter Destination Location")
    pickup_time = st.text_input("Select Pickup Time")
    pickup_date = st.date_input("Select Pickup Date", min_value=datetime.today())

    if st.button("Submit"):
        if source and destination and pickup_time and pickup_date:
            st.success(f"Ride from {source} to {destination} at {pickup_time} on {pickup_date} requested!")
            update_rider_details(rider_id, source, destination, pickup_time, pickup_date)

            # Store ride information in session_state
            st.session_state['available_ride'] = genai(source, destination, pickup_time, pickup_date)
            st.session_state['payment_made'] = False  # Reset payment_made flag

    # 2. Display the available ride if it's stored in session state
    if 'available_ride' in st.session_state:
        available_ride = st.session_state['available_ride']

        st.subheader("Available Ride Orders")
        st.write(f"**Ride ID**: {available_ride['ride_id']}")
        st.write(f"**Driver Name**: {available_ride['driver_name']}")
        st.write(f"**Source**: {available_ride['source']}")
        st.write(f"**Destination**: {available_ride['destination']}")
        st.write(f"**Date**: {available_ride['date']}")
        st.write(f"**Time**: {available_ride['time']}")
        st.write(f"**Rating**: {available_ride['rating']}")
        st.write(f"**Total Trips**: {available_ride['total_number_of_trips']}")
        st.write(f"**Vehicle**: {available_ride['Vehicle']}")
        st.write(f"**Seating Capacity**: {available_ride['seating_capacity']}")
        st.write(f"**Contact**: {available_ride['contact']}")
        st.write(f"**Distance**: {available_ride['distance']} km")
        st.write(f"**Price**: ₹{available_ride['price']}")
        st.write("---")  # Divider between rides
        if st.button(f"Request Ride {available_ride['ride_id']}", key='request_ride'):
            update_ride_details(available_ride, rider_id)
        # Button to request the ride
    if st.sidebar.button("Request Details"):
        # Fetch and display requested ride details
        st.session_state['requested_ride'] = get_requested_ride_details(rider_id)

    # 3. Display requested ride details if available
    if 'requested_ride' in st.session_state and st.session_state['requested_ride']:
        requested_ride = st.session_state['requested_ride']
        st.subheader("Requested Ride Details")

        # Ride details to display
        ride_details = {
            "Ride ID": requested_ride['ride_id'],
            "Driver Name": requested_ride['driver_name'],
            "Source": requested_ride['source'],
            "Destination": requested_ride['destination'],
            "Date": requested_ride['date'],
            "Time": requested_ride['time'],
            "Rating": requested_ride['rating'],
            "Total Trips": requested_ride['total_number_of_trips'],
            "Vehicle": requested_ride['Vehicle'],
            "Seating Capacity": requested_ride['seating_capacity'],
            "Contact": requested_ride['contact'],
            "Distance": f"{requested_ride['distance']} km",
            "Price": f"₹{requested_ride['price']}",
            "Status": requested_ride['status']
        }

        # Display ride details in a loop
        for key, value in ride_details.items():
            st.write(f"**{key}**: {value}")

        # Payment section
        if requested_ride['status'] == "accepted":
            if 'payment_made' not in st.session_state:
                st.session_state['payment_made'] = False

            col1, col2 = st.columns([4, 2])

            with col1:
                if not st.session_state['payment_made']:
                    if st.button("Pay", key="pay_button"):
                        if process_payment():
                            st.session_state['payment_made'] = True
                            update_status(requested_ride['ride_id'])
                            st.success("Payment successful!")
                            requested_ride['status'] = "paid"
                        else:
                            st.error("Payment failed.")
                else:
                    st.success("Payment already made!")

# Existing code for requested ride details
        if requested_ride['status'] == "paid":
            st.subheader("Rate and Provide Feedback")

            # Rating input (1 to 5)
            rating = st.selectbox("Rate your ride (1 to 5):", [1, 2, 3, 4, 5])

            # Feedback text input
            feedback = st.text_area("Leave your feedback:")

            # Submit button to record the feedback
            if st.button("Submit Feedback"):
                if rating and feedback:
                    genaifeed(rating,feedback,requested_ride['rating'] ,requested_ride['total_number_of_trips'],requested_ride['ride_id'])
                    st.success("Thank you for your feedback!")
                    # Add your function here to save the rating and feedback to the database
                    #save_feedback(rider_id, requested_ride['ride_id'], rating, feedback)
                else:
                    st.error("Please provide both rating and feedback.")


# Mock payment processing function (replace with actual logic if needed)
def process_payment():
    # Simulate payment processing logic
    return True
def genaifeed(a1, a2, a3, a4,ride_id):
    # Convert integers to strings and add commas where necessary
    a1 = str(a1) + ", "
    a2 = str(a2) + ", "
    a3 = str(a3) + ", "

    # Convert a4 to string as well, if it's an integer
    sumall = a1 + a2 + a3 + str(a4)



    import google.generativeai as genai

    genai.configure(api_key="AIzaSyCFYC3YudT7STlsvBazCvfkPuyKEyt5jQE")

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "i will provide rating and feedback analysis the data and give new rating and this is the rating and feedback after the ride. i will also provide his past rating and no.of rides he completed make average and give that\n ",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Please provide me with the following information so I can analyze the data and give you a new rating:\n\n* **Current Rating:** The rating the rider received after the current ride.\n* **Current Feedback:** The feedback the rider received after the current ride.\n* **Past Rating:** The average rating the rider has received from previous rides.\n* **Number of Past Rides:** The number of rides the rider has completed in the past.\n\nOnce you provide this information, I can calculate a new average rating and provide feedback on how the rider is performing. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "4.2, good but need to reach on time, 4.6, 15",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Okay, here's the analysis based on the information you provided:\n\n**Current Rating:** 4.2\n**Current Feedback:** \"Good but need to reach on time\"\n**Past Rating:** 4.6\n**Number of Past Rides:** 15\n\n**Calculating the New Average Rating:**\n\n1. **Total Rating Points:** (4.6 * 15) + 4.2 = 73.2 \n2. **Total Number of Rides:** 15 + 1 = 16\n3. **New Average Rating:** 73.2 / 16 = **4.575**\n\n**Analysis and Feedback:**\n\nThe current rating of 4.2 is slightly lower than the rider's average rating of 4.6. This suggests that the rider may have had an off day. The feedback indicates that punctuality is an area for improvement. \n\n**Recommendation:**\n\nThe rider should focus on improving their timeliness to maintain a high rating.  Here are some suggestions:\n\n* **Plan Routes Carefully:**  Factor in traffic, potential delays, and a buffer for unexpected events.\n* **Communicate with Passengers:**  If delays are unavoidable, inform passengers promptly and provide an estimated arrival time.\n* **Review Ride History:**  Analyze past trips to identify any recurring patterns that may contribute to tardiness.\n\n**Overall:**\n\nThe rider has a strong track record with an average rating of 4.6.  Addressing the punctuality issue will help maintain their high rating and ensure a positive experience for future passengers. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "in this i only need final answer here which is \"4.6\" ",
        ],
        },
        {
        "role": "model",
        "parts": [
            "You are correct!  My apologies, I got carried away with the analysis. \n\nThe new average rating is **4.58**.  \n\nI'll try to be more concise in the future. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "make it round off\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "You are absolutely right! Rounding off the new average rating to the nearest tenth, we get **4.6**. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "give me like this \"4.6\"",
        ],
        },
        {
        "role": "model",
        "parts": [
            "4.6 \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "5, great ride, 4.6, 12",
        ],
        },
        {
        "role": "model",
        "parts": [
            "4.6 \n",
        ],
        },
    ]
    )

    response = chat_session.send_message(sumall)

    update_rating(response.text,ride_id)
    
def update_rating(sumall,ride_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        UPDATE rides 
        SET rating=%s
        where ride_id=%s
        ORDER BY sno DESC
        LIMIT 1
        """
        cursor.execute(query, (sumall,ride_id,))
        connection.commit()  # Commit the changes
        cursor.close()
        connection.close()
        st.success(f"Ride ID updated successfully!")
    else:
        st.error("Failed to connect to the database.")

def update_ride_details(ride,passenger_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO rides (
            driver_name, 
            source, 
            destination, 
            date, 
            time, 
            rating, 
            total_number_of_trips, 
            Vehicle, 
            seating_capacity, 
            contact, 
            distance, 
            price, 
            ride_id,
            passenger_id
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(query, (
            ride['driver_name'],
            ride['source'],
            ride['destination'],
            ride['date'],
            ride['time'],
            ride['rating'],
            ride['total_number_of_trips'],
            ride['Vehicle'],
            ride['seating_capacity'],
            ride['contact'],
            ride['distance'],
            ride['price'],
            ride['ride_id'],
            passenger_id
        ))
        connection.commit()  # Commit the changes
        cursor.close()
        connection.close()
        st.success(f"Ride ID {ride['ride_id']} updated successfully!")
    else:
        st.error("Failed to connect to the database.")
def update_status(ride_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        UPDATE rides 
        SET status='paid'
        where ride_id=%s
        ORDER BY sno DESC
        LIMIT 1
        """
        cursor.execute(query, (ride_id,))
        connection.commit()  # Commit the changes
        cursor.close()
        connection.close()
        st.success(f"Ride ID updated successfully!")
    else:
        st.error("Failed to connect to the database.")
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
