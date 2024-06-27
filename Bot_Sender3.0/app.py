# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# # Fetch the API key from environment variables
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# # Check if the API key is loaded properly
# if GEMINI_API_KEY is None:
#     raise ValueError("No GEMINI_API_KEY found in environment variables")

# genai.configure(api_key=GEMINI_API_KEY)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate_text():
#     data = request.get_json()
#     prompt = f"Generate a text on the topic '{data['topic']}' for {data['name']}, a {data['age']}-year-old {data['gender']} interested in {data['interest']}. The text should have an unfamiliar tone, include grammar errors, mild threats or a sense of urgency, and make unusual requests like seeing something and saying something in response. The text should be at least {data['minWords']} words."
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(prompt)
#     return jsonify({'text': response.text})

# if __name__ == '__main__':
#     app.run(debug=True)


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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = (f"Generate a text on the topic '{data['topic']}' for {data['name']}, a {data['age']}-year-old {data['gender']} "
              f"interested in {data['interest']}. The text should have an unfamiliar tone, include grammar errors, mild threats "
              f"or a sense of urgency, and make unusual requests like seeing something and saying something in response. The text "
              f"should be at least {data['minWords']} words.")
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    gen_text = response.text

    # Path to the PDF file (you can modify this as needed)
    pdf_path = 'pdf.pdf'
    
    # Store data in the database
    store_data_to_db(data['name'], data['age'], data['gender'], data['interest'], data['topic'], gen_text, pdf_path)
    
    return jsonify({'text': gen_text})

if __name__ == '__main__':
    app.run(debug=True)
