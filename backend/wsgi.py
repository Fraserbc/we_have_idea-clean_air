#Invoke this with "gunicorn --bind 127.0.0.1:5000 wsgi" or "./run.sh"

#Import as application becuase gunicorn complains otherwise
from main import app as application

#Run it
if __name__ == "__main__":
	application.run()