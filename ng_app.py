from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse
import pandas as pd
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

columnas = ['id', 'inventory_name', 'contact_name', 'stock', 'last_revenue',
            'current_revenue', 'refund', 'company_name', 'categories', 'rating']

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c/Users/migga/kiritech_test/ng_new.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'C:\\Users\\migga\\kiritech_test\\ng.db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False


class Negotiation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_name = db.Column(db.String)
    contact_name = db.Column(db.String)
    stock = db.Column(db.Integer)
    last_revenue = db.Column(db.Float)
    current_revenue = db.Column(db.Float)
    refund = db.Column(db.Float)
    company_name = db.Column(db.String)
    categories = db.Column(db.String)
    rating = db.Column(db.Float)

    def __init__(self, inventory_name, contact_name, stock, last_revenue, current_revenue, refund, company_name, categories, rating):
        self.inventory_name = inventory_name
        self.contact_name = contact_name
        self.stock = stock
        self.last_revenue = last_revenue
        self.current_revenue = current_revenue
        self.refund = refund
        self.company_name = company_name 
        self.categories = categories
        self.rating = rating


db.create_all()
engine=db.create_engine('sqlite:///' + 'C:\\Users\\migga\\kiritech_test\\ng.db',{})

ng_data = pd.read_csv('./SampleCSVFile_556kb.csv', engine='python', names=columnas)
ng_data.to_sql('negotiation', engine , if_exists='replace', index=False)

class NegotiationSchema(ma.Schema):
    class Meta:
        campos = tuple(columnas)

ng_schema = NegotiationSchema(many=True)

@app.route('/data/', methods=['GET'])
def get_all_data():
    ng_data = Negotiation.query.all()
    result = ng_schema.dump(ng_data)
    return jsonify(result)



@app.route('/datos<int:numero>/')
def mostrar(numero):
    data = pd.read_csv('./SampleCSVFile_556kb.csv',
                       engine='python', names=columnas)
    data = data[0:numero].to_json(orient='records')
    parsed = json.loads(data)
    return jsonify(parsed)


if __name__ == '__main__':
    app.run(debug=True)
