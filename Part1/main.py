# from flask import Flask, request, jsonify, render_template
# from mailscout.scout import Scout
# import re
# import urllib.request
# import os
# import subprocess

# app = Flask(__name__, static_url_path='/static')
# scout = Scout()

# # Regular expression for email extraction
# emailRegex = re.compile(r'''
#     ([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)
# ''', re.VERBOSE)

# # Function to extract emails from a given URL text
# def extract_emails_from_text(url_text):
#     extracted_emails = emailRegex.findall(url_text)
#     return extracted_emails

# # Function to read HTML page from URL
# def html_page_read(url):
#     try:
#         headers = {'User-Agent': 'Mozilla/5.0'}
#         request = urllib.request.Request(url, None, headers)
#         response = urllib.request.urlopen(request)
#         url_html_page_read = response.read()
#         url_text = url_html_page_read.decode()
#         return url_text
#     except Exception as e:
#         print(f"Error fetching {url}: {e}")
#         return None

# # Route to render home page
# @app.route('/')
# def home():
#     return render_template('emailfinder.html')

# # Route to fetch emails from URLs
# @app.route('/scrape_emails', methods=['POST'])
# def scrape_emails():
#     data = request.json
#     urls = data.get('urls', [])

#     if not urls:
#         return jsonify({"error": "No URLs provided"}), 400

#     scraped_emails = set()  # Use a set to store unique emails

#     for url in urls:
#         url_text = html_page_read(url)
#         if url_text:
#             emails = extract_emails_from_text(url_text)
#             for email in emails:
#                 scraped_emails.add(email)

#     # Append scraped emails to the existing file
#     with open('scraped_emails.txt', 'a') as file:
#         for email in scraped_emails:
#             file.write(email + '\n')

#     return jsonify({"message": "Emails scraped successfully", "emails": list(scraped_emails)})

# # Route to fetch emails via mailscout
# @app.route('/fetch_emails', methods=['POST'])
# def fetch_emails():
#     data = request.json
#     fetch_type = data.get('fetch_type')
#     domain = data.get('domain')
#     names = data.get('names', None)

#     if fetch_type == 'single':
#         emails = scout.find_valid_emails(domain, names)
#         with open('scraped_emails.txt', 'a') as file:
#             for email in emails:
#                 file.write(email + '\n')
#         return jsonify({"emails": emails})

#     elif fetch_type == 'bulk':
#         email_data = data.get('email_data')
#         valid_emails = scout.find_valid_emails_bulk(email_data)
#         with open('scraped_emails.txt', 'a') as file:
#             for entry in valid_emails:
#                 for email in entry['valid_emails']:
#                     file.write(email + '\n')
#         return jsonify({"valid_emails": valid_emails})

#     else:
#         return jsonify({"error": "Invalid fetch type"}), 400

# # Route to check live emails
# @app.route('/check_emails', methods=['POST'])
# def check_emails():
#     # Run mail.py as a subprocess and wait for it to finish
#     process = subprocess.run(['python', 'mail.py'], check=True)
    
#     # Ensure the process ran without errors
#     if process.returncode != 0:
#         return jsonify({"error": "Failed to run email checking process"}), 500

#     with open('live.txt', 'r') as f:
#         live_emails = f.readlines()
    
#     with open('scraped_emails.txt', 'r') as f:
#         all_emails = f.readlines()
    
#     live_emails = [email.strip() for email in live_emails]
#     all_emails = [email.strip() for email in all_emails]
#     dead_emails = [email for email in all_emails if email not in live_emails]

#     return jsonify(live_emails=live_emails, dead_emails=dead_emails)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from mailscout.scout import Scout
import re
import urllib.request
import os
import subprocess
from data import fetch_domain_info  # Import the function from data.py

app = Flask(__name__, static_url_path='/static')
scout = Scout()

# Regular expression for email extraction
emailRegex = re.compile(r'''
    ([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)
''', re.VERBOSE)

# Function to extract emails from a given URL text
def extract_emails_from_text(url_text):
    extracted_emails = emailRegex.findall(url_text)
    return extracted_emails

# Function to read HTML page from URL
def html_page_read(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        url_html_page_read = response.read()
        url_text = url_html_page_read.decode()
        return url_text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Route to render home page
@app.route('/')
def home():
    return render_template('emailfinder.html')

# Route to fetch emails from URLs
@app.route('/scrape_emails', methods=['POST'])
def scrape_emails():
    data = request.json
    urls = data.get('urls', [])

    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    scraped_emails = set()  # Use a set to store unique emails

    for url in urls:
        url_text = html_page_read(url)
        if url_text:
            emails = extract_emails_from_text(url_text)
            for email in emails:
                scraped_emails.add(email)

    # Append scraped emails to the existing file
    with open('scraped_emails.txt', 'a') as file:
        for email in scraped_emails:
            file.write(email + '\n')

    return jsonify({"message": "Emails scraped successfully", "emails": list(scraped_emails)})

# Route to fetch emails via mailscout
@app.route('/fetch_emails', methods=['POST'])
def fetch_emails():
    data = request.json
    fetch_type = data.get('fetch_type')
    domain = data.get('domain')
    names = data.get('names', None)

    if fetch_type == 'single':
        emails = scout.find_valid_emails(domain, names)
        with open('scraped_emails.txt', 'a') as file:
            for email in emails:
                file.write(email + '\n')
        return jsonify({"emails": emails})

    elif fetch_type == 'bulk':
        email_data = data.get('email_data')
        valid_emails = scout.find_valid_emails_bulk(email_data)
        with open('scraped_emails.txt', 'a') as file:
            for entry in valid_emails:
                for email in entry['valid_emails']:
                    file.write(email + '\n')
        return jsonify({"valid_emails": valid_emails})

    else:
        return jsonify({"error": "Invalid fetch type"}), 400

# Route to check live emails
@app.route('/check_emails', methods=['POST'])
def check_emails():
    # Run mail.py as a subprocess and wait for it to finish
    process = subprocess.run(['python', 'mail.py'], check=True)
    
    # Ensure the process ran without errors
    if process.returncode != 0:
        return jsonify({"error": "Failed to run email checking process"}), 500

    with open('live.txt', 'r') as f:
        live_emails = f.readlines()
    
    with open('scraped_emails.txt', 'r') as f:
        all_emails = f.readlines()
    
    live_emails = [email.strip() for email in live_emails]
    all_emails = [email.strip() for email in all_emails]
    dead_emails = [email for email in all_emails if email not in live_emails]

    return jsonify(live_emails=live_emails, dead_emails=dead_emails)

# Route to fetch domain information using data.py
@app.route('/fetch_domain_info', methods=['POST'])
def fetch_domain_information():
    data = request.json
    domain = data.get('domain')
    api_key = data.get('api_key')

    if not domain:
        return jsonify({"error": "Domain not provided"}), 400

    if not api_key:
        return jsonify({"error": "API key not provided"}), 400

    domain_info = fetch_domain_info(domain, api_key)

    if domain_info:
        return jsonify({"domain_info": domain_info})
    else:
        return jsonify({"error": "Failed to fetch domain information"}), 500

if __name__ == '__main__':
    app.run(debug=True)