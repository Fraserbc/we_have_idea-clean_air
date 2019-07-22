sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev nginx
pip3 install flask gunicorn
sudo cp nginx.conf /etc/nginx/nginx.conf
