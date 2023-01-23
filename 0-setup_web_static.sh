#!/usr/bin/env bash
# script that configures a Nginx server
# 	- create folders
#	- create a fake HTML file
#	- create a symbolic link linked to test folder
#	- change the ownership of the /data/ folder
#	- use Alias in the configuration file

# update apt-get
apt-get update
apt-get install -y nginx

# mmake necessary folders and config changes
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Ceci n'est pas une page" > /var/www/html/404.html

# create a test HTML page
printf "%s" "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/current /data/web_static/releases/test/
chown -R ubuntu:ubuntu /data/

printf "%s" "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbtn_static {
      alias /data/web_static/current;
      index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
