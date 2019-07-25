# Import Flask and Flask Restful for the api
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3, uuid, statistics, math, random

# A nice decorator so I can use "@endpoint("/foo")"
def endpoint(endpoint):
	def wrapper(callback):
		class endpoint_class(Resource):
			def post(self):
				json_data = request.get_json(force=True)
				return callback(json_data)
		
		endpoint_class.__name__ = uuid.uuid4().hex
		api.add_resource(endpoint_class, "/api"+endpoint)
	
	return wrapper

# Create the app and api
app = Flask(__name__)
api = Api(app)

# Just an echo endpoint for testing
@endpoint("/echo")
def ping(json_data):
	return {'echo': json_data}

#Inspirational messages
inspiration = {
	"250":	["A1", "A2"],
	"500":	["B1", "B2"],
	"750":	["C1", "C2"],
	"1000":	["D1", "D2"]
}

# The endpoint that takes lat long data and returns a score
@endpoint("/score")
def score(json_data):
	db = sqlite3.connect("air_pollution.db")
	cur = db.cursor()
	cur.execute("SELECT location,lat,lon FROM data")
	data = cur.fetchall()

	# Lambda for sorting the list
	sort = lambda x: (x[1]-json_data["lat"], x[2]-json_data["lon"])

	data.sort(key=sort)
	
	query = """	SELECT carbon_monoxide,\
					nitric_oxide,\
					nitrogen_dioxide,\
					non_volatile_PM25,\
					non_volatile_PM10,\
					ozone,\
					PM25,\
					PM10,\
					sulphur_dioxide,\
					volatile_PM25,\
					volatile_PM10\
				FROM data\
				WHERE location = \"{}\"
			"""
	
	# Loop through to two closest locations and get the average for all the points and get the distance
	average, distances = [], []
	for location in data[:2]:
		# Pythagorean theorem magic
		distances.append(abs( math.sqrt( abs(location[1]-json_data["lat"])**2 + abs(location[2]-json_data["lon"])**2 ) - 1))

		# Get the data from the db
		cur.execute(query.format(location[0]))
		data_points = cur.fetchall()[0]

		# Get the average of the data points
		average.append(statistics.mean(data_points))
	
	# Calculate the scores by making the numbers between 0 and 1 and multiplying them by the distance that has been f
	# Flip them so 1 = 0 and 0 = 1 by taking away 1 and then using abs (absolute value)
	# Multiply by 1000 so the numbers are between 0 and 1000
	# Get the mean on those two numbers
	# Round to the nearest integer
	score = round(statistics.mean([abs(((x*y)/10)-1)*1000 for x, y in zip(average, distances)]))

	#Get the inspirational message
	message = ""
	for score_range in inspiration.keys():
		if score <= int(score_range):
			message = random.choice(inspiration[score_range])

	# Return the score
	return {'score':score, "message":message}

# Start the app
if __name__ == '__main__':
	app.run()