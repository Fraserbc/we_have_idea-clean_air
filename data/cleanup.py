csv_filenames = [
	"carbonmonoxide.csv",
	"nitricoxide.csv",
	"nitrogendioxide.csv",
	"Non-volatile PM10-Hourly measured.csv",
	"Non-volatile PM2_5 -Hourly measured.csv",
	"Ozone.csv",
	"PM10-particulate matter-Hourly measured.csv",
	"PM2.5-particulate matter-Hourly measured.csv",
	"Sulphur-dioxide0.csv",
	"Volatile-PM10-Hourly-measured.csv",
	"Volatile-PM2_5-Hourly-measured.csv"
]

#Go through each files
for name in csv_filenames:
	with open(name, "r") as csv_file:
		#Read all the lines
		lines = csv_file.readlines()

		#If it has a comma in it then it is valid csv and write it to a file
		#This is a dirty way to do it but the extra text doesn't have any commas in it
		with open("clean/{}".format(name), "w+") as out_clean:
			for line in lines:
				if "," in line:
					out_clean.write(line)