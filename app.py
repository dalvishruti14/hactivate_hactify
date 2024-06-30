from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/hacktivate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ViewCampaign(db.Model):
    __tablename__ = 'view_c'
    c_id = db.Column(db.Integer, primary_key=True)
    campaign = db.Column(db.String(255))

@app.route('/fetch_campaigns', methods=['GET'])
def fetch_campaigns():
    campaigns = ViewCampaign.query.all()
    campaign_list = [{'c_id': campaign.c_id, 'campaign': campaign.campaign} for campaign in campaigns]
    return jsonify(campaign_list)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
