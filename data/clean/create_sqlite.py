#Import the needed modules
import sqlite3, csv

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
query = """
CREATE TABLE IF NOT EXISTS (
	'location'	TEXT,
	'carbon_monoxide'	INTEGER,
	'nitric_oxide'	INTEGER,
	'nitrogen_dioxide'	INTEGER,
	'non_volatile_PM25'	INTEGER,
	'non_volatile_PM10'	INTEGER,
	'ozone'	INTEGER,
	'PM25'	INTEGER,
	'PM10'	INTEGER,
	'sulphur_dioxide'	INTEGER,
	'volatile_PM25'	INTEGER,
	'volatile_PM10'	INTEGER
);
"""

cur.execute(query)

#Loop through the files
for filename in csv_filenames.keys():
	with open(filename, "r") as csv_file:
		#Open the csv file and select every other collumn after the 2nd
		csv_reader = csv.reader(csv_file, delimiter=',')
		rows = [row[2:][::2] for row in csv_reader]
		
		#Get rid of the row that includes names as we don't need it
		rows.pop(1)

		print(rows)