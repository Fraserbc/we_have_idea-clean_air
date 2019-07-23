sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev gunicorn nginx
python3 -m pip install flask gunicorn flask-restful
sudo cp nginx.conf /etc/nginx/nginx.conf
