import streamlit as st
import os
import google.generativeai as genai
import mysql.connector
from mysql.connector import Error
import re

# Configure the API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCmsZPpSivHy2TqFozAqie-vde4PBLkWGI"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Function to fetch data from the database
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
            cursor.execute("SELECT gender, age, gen_text FROM BOT_S ORDER BY s_id DESC LIMIT 1")
            record = cursor.fetchone()
            return record
    except Error as e:
        print(f"Error fetching data from database: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

# Function to insert the final answer into the database
def insert_final_answer(final_answer):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='hacktivate',
            user='root',
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO bot_r (ans) VALUES (%s)"
            cursor.execute(query, (final_answer,))
            connection.commit()
    except Error as e:
        print(f"Error inserting final answer into database: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

# Function to determine the final answer based on the counts of "Yes" and "No"
def determine_final_answer(text):
    yes_count = len(re.findall(r'\bYes\b', text))
    no_count = len(re.findall(r'\bNo\b', text))
    return "Yes" if yes_count > no_count else "No"

# Initialize Streamlit app
st.title("Human Persona")

# Fetch user data from the database
user_data = fetch_user_data()

# Check if data fetched successfully
if user_data:
    gender = user_data['gender']
    age = user_data['age']
    gen_text = user_data['gen_text']

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I will be responding to the mails"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process and store Query and Response
    def llm_function(query):
        # Add prompts to the query
        prompt = (
            "You are a sophisticated AI text analysis tool. You get an input in the following format:\n"
            "Text followed by few evaluation_questions.\n"
            "The questions will pertain to the quantity of a specific aspect in the email's content.\n"
            "Your goal is to provide a floating-point number that quantifies whether and to what extent the aspect exists in the text.\n"
            "Please approach the analysis in a step-by-step manner, providing up to five sentences of explanation in a next line after presenting your final output.\n"
            "Output your final answer as a Yes if floating point number is less than 0.5 or 0.5, and No if the floating point number is more than 0.5. DO NOT OUTPUT ANY NUMBER IN YOUR RESPONSE OTHER THAN YOUR FINAL ANSWER\n"
            "Begin!\n"
            "YOUR OUTPUT MUST END IN THE FOLLOWING FORMAT:\n"
            "Answering all questions with Yes or No.\n\n"
            f"{query}"
        )

        response = model.generate_content(prompt)

        # Determine and store the final answer
        final_answer = determine_final_answer(response.text)
        if final_answer:
            insert_final_answer(final_answer)

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
