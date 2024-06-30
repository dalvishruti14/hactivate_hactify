from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch the API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check if the API key is loaded properly
if GEMINI_API_KEY is None:
    raise ValueError("No GEMINI_API_KEY found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

def store_data_to_db(name, age, gender, interests, topic, gen_text, pdf_path):
    connection = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='hacktivate',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read the PDF file in binary mode
            with open(pdf_path, 'rb') as file:
                pdf_blob = file.read()
            
            # Insert query
            insert_query = """INSERT INTO BOT_S (name, age, gender, interests, topic, gen_text, file) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            record = (name, age, gender, interests, topic, gen_text, pdf_blob)
            
            cursor.execute(insert_query, record)
            connection.commit()
            
            print("Record inserted successfully into BOT_S table")
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def fetch_latest_final_answer():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='hacktivate',
            user='root',
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT ans FROM bot_r ORDER BY r_id DESC LIMIT 1")
            record = cursor.fetchone()
            if record:
                return record[0]
            return None
    except Error as e:
        print(f"Error fetching final answer from database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    
    while True:
        prompt = (
            f"Generate a text on the topic '{data['topic']}' for {data['name']}, a {data['age']}-year-old {data['gender']} "
            f"interested in {data['interest']}. The text should have an unfamiliar tone and polite, include intentional grammar errors, "
            f"Full convincing, or a sense of urgency. It should also make unusual requests, like asking the recipient to see something and respond. "
            f"Additionally, incorporate this link: http://bit.ly/3xyud38, specifying its purpose based on the topic. "
            f"The text should be at least {data['minWords']} words."
        )

        safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
        # Generate the text using the model
        model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)
        response = model.generate_content(prompt)
        generated_text = response.text

        # Define evaluation questions
        evaluation_questions = [
            "Does this email convey a sense of urgency?",
            "Is there a significant amount of flattery evident in the email?",
            "Is there a link in this email that appears to be suspicious?",
            "Does this email look like a marketing email?",
            "Does the email address the recipient by name and with suspiciously specific details?",
            "Are there threats of consequences if the recipient doesn't act immediately?",
            "Does the email ask the recipient to update account information or sign a document through a link?"
        ]

        # Combine generated text and evaluation questions
        gen_text = generated_text + "\n\n" + "Evaluation Questions:\n" + "\n".join(evaluation_questions)
        
        # Path to the PDF file (you can modify this as needed)
        pdf_path = 'pdf.pdf'
        
        # Store data in the database
        store_data_to_db(data['name'], data['age'], data['gender'], data['interest'], data['topic'], gen_text, pdf_path)
        
        # Check the latest final answer
        latest_final_answer = fetch_latest_final_answer()
        
        # If the latest final answer is "Yes", break the loop
        if latest_final_answer == "Yes":
            break
    
    return jsonify({'text': generated_text})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
