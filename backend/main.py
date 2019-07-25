# Import Flask and Flask Restful for the api
from flask import Flask, request
import sqlite3, json, statistics, math, random

# Create the app and api
app = Flask(__name__)

# Just an echo endpoint for testing
@app.route("/api/echo", methods=["POST"])
def ping():
	json_data = json.loads(request.get_data().decode())
	return {'echo': json_data}

# Inspirational messages
inspiration = {
	"250":	["Poor", "Bad", "No"],
	"500":	["Ok", "All Right"],
	"750":	["Good!", "Well Done!"],
	"1000":	["Great!", "Amazing!"]
}

# Things you can do to help
help_messages = [
	"Use public transport or active travel (cycle/walk)",
	"Buy a more efficient car or an electric car",
	"Switch to a renewable energy tariff",
	"Work closer to home and drive less",
	"Join a car share",
	"Don't drive during rush hour",
	"Be more energy efficient and save money by insulating your home",
	"Don't burn things especialy coal or wood",
	"Use electric heating"
]

# The endpoint that takes lat long data and returns a score
@app.route("/api/score", methods=["POST"])
def score():
	# Get the json data from the user
	json_data = json.loads(request.get_data().decode())
	
	# Create a DB connection
	# Can't do it outside this function as it is in a different thread
	db = sqlite3.connect("air_pollution.db")
	cur = db.cursor()

	# Get the locations and corresponding latitudes and longitudes
	cur.execute("SELECT location,lat,lon FROM data")
	data = cur.fetchall()

	# Lambda for sorting the list by how close it is to the user
	sort = lambda x: (x[1]-json_data["lat"], x[2]-json_data["lon"])

	data.sort(key=sort)
	
	# Query for selecting all the data by location
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
		# Gets the location from the monitoring station to the user
		# Flip it so 1 = 0 and 0 = 1
		# We assume the users are in Edinburgh only so we can flip it by taking away one and then using abs
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

	# Get the inspirational message
	inspirational_message = ""
	for score_range in inspiration.keys():
		if score <= int(score_range):
			inspirational_message = random.choice(inspiration[score_range])

	# Select 2 things you can do to help
	abilities = random.sample(help_messages, 2)

	# Return the score
	return {'score':score, "message":inspirational_message, "abilities":abilities}

# Start the app
if __name__ == '__main__':
	app.run()