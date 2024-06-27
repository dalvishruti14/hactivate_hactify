import streamlit as st
import os
import google.generativeai as genai
import mysql.connector
from mysql.connector import Error

# Configure the API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCmsZPpSivHy2TqFozAqie-vde4PBLkWGI"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Function to fetch data from database
def fetch_user_data():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='hacktivate',
            user='root',
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT gender, age, gen_text FROM BOT_S WHERE s_id = %s", (0,))
            record = cursor.fetchone()
            return record
    except Error as e:
        print(f"Error fetching data from database: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

# Initialize Streamlit app
st.title("Doubt Solving Chatbot")

# Fetch user data from database
user_data = fetch_user_data()

# Check if data fetched successfully
if user_data:
    gender = user_data['gender']
    age = user_data['age']
    gen_text = user_data['gen_text']

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I help you today?"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process and store Query and Response
    def llm_function(query):
        response = model.generate_content(query)

        # Displaying the Assistant Message
        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Storing the User Message
        st.session_state.messages.append({"role": "user", "content": query})

        # Storing the Assistant Message
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    # Select the model
    model = genai.GenerativeModel('gemini-pro')

    # Automatically use the fetched gen_text as the initial query
    initial_query = gen_text

    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(initial_query)

    # Call llm_function with the initial query
    llm_function(initial_query)
else:
    st.error("Failed to fetch user data from database.")


