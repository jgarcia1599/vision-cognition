#!/usr/bin/bash

launchDir=`pwd`

# 1. Install libraries
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt-get -y install apache2 apache2-dev
sudo apt install python3-pip
sudo apt-get -y install python3.6 python3.6-dev
sudo apt install virtualenv
sudo apt-get -y install mysql-server
sudo apt-get install libmysqlclient-dev

# 2. Link python with version 3
sudo ln -sf /usr/bin/python3 /usr/bin/python

# 3. Configure WSGI
sudo pip3 install mod_wsgi
sudo bash -c 'mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load'
sudo a2enmod wsgi
sudo service apache2 restart

# 4. Create virtual environment
sudo mkdir ~/FlaskApp
cd ~/FlaskApp
sudo virtualenv -p python3 --system-site-packages venv
source venv/bin/activate
sudo pip3 install flask
sudo pip3 install mysql-connector

# 5. Create Apache configuration for Flask App
sudo bash -x ${launchDir}/5-apache-config.sh

# 6. Create Flask app
sudo cp -r ${launchDir}/ioiapp_src/* ~/FlaskApp/.
cd ~/FlaskApp
source venv/bin/activate
sudo pip3 install -r requirements.txt
  
# 7. Setup mysql database server
sudo mysql -u root -e "create user 'username'@'localhost' identified by 'password';"
sudo mysql -u root -e "grant all on *.* to 'username'@'localhost';"
sudo mysql -u root -e "CREATE DATABASE xvision;" 

#Give edit permision
sudo chmod -R 777 ~/FlaskApp/*

# 8. restart apache
sudo service apache2 restart

# 9. initiate db by running the python script
cd ~/FlaskApp
python3 app.py
