#Import the needed modules
import sqlite3, csv, statistics, random

#Names of the files
csv_filenames = {
	'carbonmonoxide.csv':'carbon_monoxide',
	'nitricoxide.csv':'nitric_oxide',
	'nitrogendioxide.csv':'nitrogen_dioxide',
	'Non-volatile PM10-Hourly measured.csv':'non_volatile_PM25',
	'Non-volatile PM2_5 -Hourly measured.csv':'non_volatile_PM10',
	'Ozone.csv':'ozone',
	'PM10-particulate matter-Hourly measured.csv':'PM10',
	'PM2.5-particulate matter-Hourly measured.csv':'PM25',
	'Sulphur-dioxide0.csv':'sulphur_dioxide',
	'Volatile-PM10-Hourly-measured.csv':'volatile_PM10',
	'Volatile-PM2_5-Hourly-measured.csv':'volatile_PM25'
}

#Setup the db connection
db = sqlite3.connect("air_pollution.db")
cur = db.cursor()

#Create the table if it doen't exist
create_db = """
CREATE TABLE IF NOT EXISTS data (
	location	TEXT UNIQUE,
	carbon_monoxide	INTEGER,
	nitric_oxide	INTEGER,
	nitrogen_dioxide	INTEGER,
	non_volatile_PM25	INTEGER,
	non_volatile_PM10	INTEGER,
	ozone	INTEGER,
	PM25	INTEGER,
	PM10	INTEGER,
	sulphur_dioxide	INTEGER,
	volatile_PM25	INTEGER,
	volatile_PM10	INTEGER
);
"""

cur.execute(create_db)

#Loop through the files
for filename in csv_filenames.keys():
	with open(filename, "r") as csv_file:
		#Open the csv file and select every other collumn after the 2nd
		csv_reader = csv.reader(csv_file, delimiter=',')
		rows = [row[2:][::2] for row in csv_reader]
		
		#Get rid of the row that includes names as we don't need it
		rows.pop(1)

		locations = rows.pop(0)

		#Go through the rows and average the data
		for x in range(len(rows[0])):
			try:
				average = statistics.mean( [abs(float(row[x])) for row in rows if row[x] != "No data"] )
			except statistics.StatisticsError:
				continue
			
			#Generate the query for inserting the data into the db
			add_data = """
			INSERT OR IGNORE INTO data (location) VALUES ("{location}");
			UPDATE data SET {point_name}={data} WHERE location="{location}";
			"""

			#Put the data into the query and execute it
			add_data = add_data.format(point_name=csv_filenames[filename], location=locations[x], data=average)
			cur.executescript(add_data)
		
			print("LOCATION - {}\nPOLLUTANT - {}\nAVERAGE - {}".format(locations[x], csv_filenames[filename], average))

#Mock the rest of the data
collumns = [csv_filenames[col] for col in csv_filenames.keys()]

#Fetch the locations
cur.execute("SELECT location FROM data")
rows = [x[0] for x in cur.fetchall()]

#Get the data from all the collumns
for col in collumns:
	#Get the data from the db
	cur.execute("SELECT {} FROM data".format(col))
	data = cur.fetchall()

	#Get the cells that contain data
	#If they don't have any data add the name of the location it came from to a list
	cells = []
	rows_to_update = []
	for x in range(len(data)):
		if data[x] == (None,):
			rows_to_update.append( rows[x] )
		else:
			cells.append(data[x][0])
	
	
	#If there is more than one cell, get the range and use that for mocking the data
	#If there is only one cell then the range is 0 to double the only cells value
	if len(cells) > 1:
		minimum = min(cells)
		maximum = max(cells)
	else:
		minimum = 0
		maximum = cells[0]*2
	
	#Get the random numbers to fill the db
	mocked_cells = [random.uniform(minimum, maximum) for x in range( len(csv_filenames.keys()) - len(cells) )]
	
	#Loop through the location names and the mocked data
	for row, cell in zip(rows_to_update, mocked_cells):
		#Fill in the empty cells with mocked data
		query = "UPDATE data SET \"{}\"={} WHERE location=\"{}\"".format(col, cell, row)
		#print(query)
		cur.execute(query)

#Close the DB and write the changes
db.commit()
db.close()