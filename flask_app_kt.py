from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse
import pandas as pd
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app2 = Flask(__name__)
api = Api(app)

app2.config['SQLALCHEMY_DATABASE_URI']='sqlite:///c/Users/migga/kiritech_test/ng.db'

columnas = ['id', 'inventory name', 'contact name', 'stock', 'last revenue',
            'current revenue', 'refund', 'company name', 'categories', 'rating']


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Negotiation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_name = db.Column(db.String(30))
    contact_name = db.Column(db.String(20))

    def __init__(self, inventory_name, contact_name):
        self.inventory_name = inventory_name
        self.contact_name = contact_name

db.create_all()

class NegotiationSchema(ma.Schema):
    class Meta:
        pass

@app.route('/datos<int:numero>/')
def mostrar(numero):
    data = pd.read_csv('./SampleCSVFile_556kb.csv',
                       engine='python', names=columnas)
    data = data[0:numero].to_json(orient='records')
    parsed = json.loads(data)
    return jsonify(parsed)

# Add URL endpoints
# api.add_resource(Negotiation, '/negotiation')
# @app.route('/negotiation')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# app.config['SQLALCHEMY_DATABASE_URI']=
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = True


if __name__ == '__main__':
    app.run(debug=True)
