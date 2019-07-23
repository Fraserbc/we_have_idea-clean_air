csv_filenames = [
	"carbonmonoxide.csv",
	"nitricoxide.csv",
	"nitrogendioxide.csv",
	"Nitrogenoxidesasnitrogendioxide.csv",
	"Non-volatile PM10-Hourly measured.csv",
	"Non-volatile PM2_5 -Hourly measured.csv",
	"Ozone.csv",
	"PM10-particulate matter-Hourly measured.csv",
	"PM2.5-particulate matter-Hourly measured.csv",
	"Sulphur-dioxide0.csv",
	"Volatile-PM10-Hourly-measured.csv",
	"Volatile-PM2_5-Hourly-measured.csv"
]

for name in csv_filenames:
	with open(name, "r") as csv_file:
		lines = csv_file.readlines()

		with open("clean/{}".format(name), "w+") as out_clean:
			for line in lines:
				if "," in line:
					out_clean.write(line)