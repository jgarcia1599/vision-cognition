cd ~/FlaskApp

# getting ip address
ipaddress=`dig +short myip.opendns.com @resolver1.opendns.com`

# creating Apache configuration file
sudo bash -c 'echo "<VirtualHost *:80>
    ServerName \$ipaddress
    
    WSGIScriptAlias / /home/ubuntu/FlaskApp/flask_app.wsgi
    WSGIDaemonProcess FlaskApp python-path=/home/ubuntu/FlaskApp:/home/ubuntu/FlaskApp/venv/lib/python3.6/site-packages
    WSGIProcessGroup FlaskApp
     
    <Directory /home/ubuntu/FlaskApp>
        Options FollowSymLinks
        AllowOverride None
        Require all granted
     </Directory>
     ErrorLog \${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>" > FlaskApp.conf'

# Inserting public IP address into configuration file
cat FlaskApp.conf | sed "s/\$ipaddress/$ipaddress/" > /etc/apache2/sites-available/FlaskApp.conf

sudo a2ensite FlaskApp
sudo service apache2 restart