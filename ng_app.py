from flask import Flask, jsonify
import flask
from flask_restful import Api
import pandas as pd
import sqlite3
import json
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + '.\\ng.db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

columnas = ['id', 'inventory_name', 'contact_name', 'stock', 'last_revenue',
            'current_revenue', 'refund', 'company_name', 'categories', 'rating']


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

engine = db.create_engine('sqlite:///' + '.\\ng.db', {})
ng_data = pd.read_csv('./SampleCSVFile_556kb.csv',
                      engine='python', names=columnas)
ng_data.to_sql('negotiation', engine, if_exists='replace', index=False)

#------ not used -------------------------
class NegotiationSchema(ma.Schema):
    class Meta:
        campos = tuple(columnas)

ng_schema = NegotiationSchema(many=True)


@app.route('/data_2/', methods=['GET'])
def get_all_data():
    ng_data = Negotiation.query.all()
    result = ng_schema.dump(ng_data)
    return jsonify(result)
# ----------------------------------------

@app.route('/data/', methods=['GET'])
def get_all_data_pages(regs_per_page=20):
    page = int(flask.request.args.get('page', default=1))
    reg_ini = (page-1)*regs_per_page
    re_fin = (page)*regs_per_page
    conn = sqlite3.connect('./ng.db')
    c = conn.cursor()
    result = c.execute(
        '''SELECT * from negotiation ''').fetchall()[reg_ini:re_fin]
    if flask.request.content_type == 'application/json':
        return jsonify(result)
    elif flask.request.content_type == 'text/html':
        return str(result)
    elif flask.request.content_type == None:
        return 'set "Content-Type" as application/json or text/html'


if __name__ == '__main__':
    app.run(debug=True)
