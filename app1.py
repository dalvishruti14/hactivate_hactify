from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/data')
def get_data():
    # Connect to the database
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='hacktivate'
    )

    cursor = db.cursor(dictionary=True)

    # Fetch data for the bar chart (Users per Day)
    cursor.execute("SELECT date, COUNT(*) as count FROM home_pg GROUP BY date")
    bar_data = cursor.fetchall()

    # Fetch data for the doughnut chart (Distribution of Users by City)
    cursor.execute("SELECT city, COUNT(*) as count FROM home_pg GROUP BY city")
    doughnut_data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(bar_data=bar_data, doughnut_data=doughnut_data)

@app.route('/')
def index():
    return render_template('charts.html')

if __name__ == '__main__':
    app.run(debug=True)
