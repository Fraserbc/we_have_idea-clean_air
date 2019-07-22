from flask import Flask, request
from flask_restful import Resource, Api

#A nice decorator so I can use "@endpoint("/foo")"
def endpoint(endpoint):
    def wrapper(callback):
        class resource(Resource):
            def post(self):
                json_data = request.get_json(force=True)
                return callback(json_data)
        
        api.add_resource(resource, "/api"+endpoint)
    
    return wrapper

app = Flask(__name__)
api = Api(app)

@endpoint("/ping")
def ping(json):
	return {'yeet': json}

if __name__ == '__main__':
	app.run()