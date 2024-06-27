## Problem Statement

Phishing Abhiyan addresses the following challenges:
- Inability to simulate realistic phishing attacks.
- Difficulty in gathering and profiling target email addresses.
- Limited insights into campaign effectiveness and user responses.

## Features and Implementation

### Reconnaissance Dashboard

- *Login and Campaign Management:* Users can log in to a dashboard to manage and monitor phishing campaigns.
- *Campaign Analytics and Visualizations:* Detailed visualizations of campaign metrics and performance analytics.
- *Manual CSV Upload:* Option to manually upload CSV files for emails.

### Email Address Gathering

- *Automated Email Gathering:* Tools and techniques to automate the collection of email addresses.
- *Email Verification:* Verification tools to validate addresses and filter inactive ones.

### AI-Driven Phishing Email Generation

- *Model Tuning:* Tuning LLM models with spam email datasets to generate realistic phishing emails.
- *Phishing Email Creation:* Generating tailored phishing emails that mimic target domain communication styles.
- *Campaign Execution:* Automated bots for sending phishing emails and tracking performance metrics like open rates and click rates.

### Bot Communication and Validation

- *AI Personas:* Creating AI personas to simulate real user responses to phishing emails.
- *Phishing Attempt Refinement:* Iterative refinement of phishing email content based on response evaluations.

### IP Tracking and Geolocation

- *IP Tracking:* Logging IP addresses of phishing email recipients for tracking purposes.
- *Geolocation:* Utilizing IP geolocation services to identify recipient geolocations.

## Installation and Setup

To set up Phishing Abhiyan locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/dalvishruti14/hactivate_hactify.git
    ```
2. Navigate to the project directory:
    ```sh
    cd hactivate_hactify-main
    ```
3. Run the email finder:
    ```sh
    cd Part1
    python main.py
    ```
4. Run the chatbot for sending phishing emails:
    ```sh
    cd ../Send
    python app.py
    ```
5. Run the chatbot for responding to phishing emails:
    ```sh
    cd ../Bot_Response
    streamlit run app.py
    ```
6. Run the chatbot for help:
    ```sh
    cd ../Bot_Response1.0
    streamlit run Doubts.py
    ```
7. Run the live server
   
[Watch the Demo here]()

  
