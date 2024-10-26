import os
import mysql.connector
import google.generativeai as genai

# Configure Google Generative AI
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

)

# Start a chat session
chat_session = model.start_chat(
    history=[]
)

# Connect to MySQL Database
try:
    db_connection = mysql.connector.connect(
        host="localhost",  # Your host, e.g., "127.0.0.1"
        user="root",  # Your DB username
        password="Sindhu4525@",  # Your DB password
        database="hexaemp"  # Your database name
    )

    cursor = db_connection.cursor()

    # Execute SQL query to get data
    cursor.execute("SELECT * FROM  hexaemp.driver_details;")
    result = cursor.fetchall()
    print(result)
  # print(result)
    
    if result:
        # Convert the SQL result to string for AI input
        data_from_sql = result[0]  # Assuming the result is in the first column

      #  print(f"Data from SQL: {data_from_sql}")

        # Send the SQL data as input to the AI model
        response = chat_session.send_message(f"Process the following data: {result}")
       # print(f"AI Response: {response.text}")

    cursor.close()
    db_connection.close()

except mysql.connector.Error as err:
    #print(f"Error: {err}")
    print("kkss")
