from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse
import pandas as pd
import json

app = Flask(__name__)
api = Api(app)
columnas = ['id', 'inventory name', 'contact name', 'stock', 'last revenue',
            'current revenue', 'refund', 'company name', 'categories', 'rating']


class Users(Resource):
    def get(self):
        data = pd.read_csv('SampleCSVFile_556kb.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('age', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()

        data = pd.read_csv('SampleCSVFile_556kb.csv')

        new_data = pd.DataFrame({
            'name': [args['name']],
            'age': [args['age']],
            'city': [args['city']]
        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('SampleCSVFile_556kb.csv', index=False)
        return {'data': new_data.to_dict('records')}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        data = data[data['name'] != args['name']]

        data.to_csv('users.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200


# Add URL endpoints
api.add_resource(Users, '/users')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/datos<int:numero>/')
def mostrar(numero):
    data = pd.read_csv('./SampleCSVFile_556kb.csv', engine='python', names=columnas)
    data = data[0:numero].to_json(orient='records')
    parsed = json.loads(data)
    return jsonify(parsed)


if __name__ == '__main__':
    app.run(debug=True)
