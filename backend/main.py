from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

"""
@app.route('/<path:path>')
def hello_world(path):
	print(path)
	return 'Hello, World!'
"""

class HelloWorld(Resource):
	def get(self):
		return {'hello': 'world'}

api.add_resource(HelloWorld, '/api/abcd')

if __name__ == '__main__':
	app.run(debug=True)