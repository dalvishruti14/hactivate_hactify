# import streamlit as st
# import mysql.connector
# from mysql.connector import Error

# # Database configuration
# DB_HOST = '127.0.0.1'
# DB_NAME = 'hacktivate'
# DB_USER = 'root'
# DB_PASSWORD = ''

# # Function to fetch data from the database
# def fetch_data():
#     try:
#         connection = mysql.connector.connect(
#             host=DB_HOST,
#             database=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD
#         )
        
#         if connection.is_connected():
#             cursor = connection.cursor()
#             cursor.execute("SELECT age, gender, gen_text FROM BOT_S")
#             result = cursor.fetchall()
#             return result
    
#     except Error as e:
#         st.error(f"Error: {e}")
    
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

# # Streamlit app layout
# st.title("Fetch Data from Database")

# data = fetch_data()

# if data:
#     for row in data:
#         age, gender, gen_text = row
#         st.write(f"Age: {age}")
#         st.write(f"Gender: {gender}")
#         st.write(f"Generated Text: {gen_text}")
#         st.write("---")
# else:
#     st.write("No data found.")

# import streamlit as st
# import os
# import google.generativeai as genai
# import mysql.connector
# from mysql.connector import Error

# # Load the environment variables
# os.environ['GOOGLE_API_KEY'] = "your_api_key"

# # Configure the Generative AI model
# genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# # Database configuration
# DB_HOST = '127.0.0.1'
# DB_NAME = 'hacktivate'
# DB_USER = 'root'
# DB_PASSWORD = ''

# def fetch_user_data(s_id):
#     try:
#         connection = mysql.connector.connect(
#             host=DB_HOST,
#             database=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD
#         )
        
#         if connection.is_connected():
#             cursor = connection.cursor()
#             cursor.execute("SELECT gender, age, gen_text FROM BOT_S WHERE s_id = %s", (s_id,))
#             result = cursor.fetchone()
#             return result  # Returns a tuple (gender, age, gen_text)
    
#     except Error as e:
#         st.error(f"Error: {e}")
    
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

# def generate_response_prompt(text, gender, age):
#     if "your details" in text.lower():
#         return f"Yes, I can provide my details. I am a {age}-year-old {gender} interested in {interests}. What would you like to know?"
#     elif "do something" in text.lower():
#         return f"Yes, I can help with that. What specifically would you like me to do?"
#     elif "public domain" in text.lower():
#         return "No, I'm sorry, I cannot respond to emails from public domains. Is there anything else I can assist you with?"
#     elif "sensitive information" in text.lower():
#         return "No, I'm sorry, I cannot provide sensitive information via email. Is there anything else I can assist you with?"
#     elif "terrible grammar" in text.lower():
#         return "No, I'm sorry, I cannot respond to emails with poor grammar. Is there anything else I can assist you with?"
#     elif "suspicious attachment" in text.lower():
#         return "No, I'm sorry, I cannot open emails with suspicious attachments. Is there anything else I can assist you with?"
#     elif "panic" in text.lower():
#         return "No, I'm sorry, I cannot respond to messages that cause panic. Is there anything else I can assist you with?"
#     elif "won a" in text.lower():
#         return "Yes, I am interested! Please provide more details about what I have won."
#     elif "government agency" in text.lower():
#         return "Yes, I will respond to emails from government agencies. Please provide more information."
#     else:
#         return "No, I'm sorry, I cannot respond to that. Is there anything else I can assist you with?"

# # Streamlit app
# st.title("Human-Like Chatbot")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "I am here to respond to your generated texts like a human would. Ask me anything."}
#     ]

# # Fetch data from the database (assuming s_id is 0 for demonstration)
# user_data = fetch_user_data(0)  # You can change the s_id as needed
# if user_data:
#     gender, age, gen_text = user_data

#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Process and store Query and Response
#     def llm_function(query):
#         response_text = generate_response_prompt(query, gender, age)
        
#         # Displaying the Assistant Message
#         with st.chat_message("assistant"):
#             st.markdown(response_text)

#         # Storing the User Message
#         st.session_state.messages.append({"role": "user", "content": query})
        
#         # Storing the Assistant Message
#         st.session_state.messages.append({"role": "assistant", "content": response_text})

#     # Accept user input
#     query = st.chat_input("What's up?")

#     # Calling the Function when Input is Provided
#     if query:
#         # Displaying the User Message
#         with st.chat_message("user"):
#             st.markdown(query)

#         llm_function(query)
# else:
#     st.error("Failed to fetch user data.")

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


