# Vision-Occlusion

A data collection tool for the study of how humans recognize shapes and objects in images using Machine Learning. This web applications was created to collect data on users' ability to recognize occluded objects.  Below is an explanation of the app's architecture, dependencies, and conventions.

## Project Dependencies

### Frontend

**HTML, CSS**: For templating and styling

* Libraries
  * Bootstrap: Used through pip using [Flask-Bootstrap ](https://pythonhosted.org/Flask-Bootstrap/) instead of a CDN. It facilitates the implementation of responsive web-design practices.

**Javascript** : For interactivity and data collection functionality on the client side.

* Libraries
  * [p5.js :](https://) For interactivy and easier canvas manipulation
  * [Jquery ](https://api.jqueryui.com/dialog/): For easier DOM manipulation and for creating the instructions pop up.

### Backend

[Flask: ](https://flask.palletsprojects.com/en/1.1.x/)For server-side programming, data collection,serving, and manipulation, and for serving the front end content to the users. We relied on several python libraries (all listed in the requirements.txt file) and some of the most important ones are:

* Libraries
  * [Boto: ](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)Amazon's Python Software Development Kit. Used to validate user's tasks done in the app  on Amazon Mechanical Turk.
  * [Flask-SQLAlchemy:](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) To create Database Models and Relationships using Python Classes. Facilitates Flask-Database interactions.

### Database

[MySQL: ](https://www.mysql.com/)World's most famous open source relational database.

## Setup

This app is designed for two types of environments: Development and Production. Both environments have different configurations (databases, secret_keys, etc.) and you must first create the configuration files for both environments for this app to run properly.

### Production Setup
In this directory, there is a ```config.py``` file which obtains some of its information from a module called ```secret_keys.py```:
```python
# config.py
from datetime import timedelta
import secret_keys

```
The ```secret_keys.py``` file  in this directory includes the secret infoprmation necessary for this app to run. Feel free to modify it at your convenience:

```python
#secret_keys.py

db_url = 'mysql://username:password@1.11.111.111:3306/db_name'
#url_convention = 'mysql://[DB-USERNAME]:[DB-PASSWORD]@[DB-IP-ADDRESS]:[DB-PORT-NUMBER]/[DB-NAME]'
session_secret_key = "a large random string"


```
### Development Setup
The configuration file for the development environment resides in the ```instance/``` folder. Please modify the ```secret_keys_dev.py``` file if you wish to change your database name or the secret key.

```python

#secret_keys_dev.py


#use a sql lite databse for development. It is very easy to use.
db_url = 'sqlite:///data.sqlite3'

# during development, your secret key doesnt need to be that 'secret'
session_secret_key = "secret keey"

```
## To Change Models

We use Flask-SQLAlchemy to create database models . However, Flask-SQLAlchemy doesn't provide database migrations (updating the existing database when there is a change in the ```models.py``` file) out of the box. For migrations, we use [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) . As such, whenever you modify the database models, you must run the following commands on the terminal so that the database migrations are reflected in the database:

## First Time 
Create migrations folder with the following command:

```
flask db init
```
You only need to do this the first time you want to run migrations. 



```
flask db migrate -m"update models"
flask db upgrade
```

When there is an error in the migrations and you must revert and restart the migration:

```
flask db stamp head
flask db migrate -m"update models"
flask db upgrade
```

**Note:** Please make sure that your migrations are reflected on both your production and development databases. The aforementioned commands will only modify the database of whatever environment you were in when you ran them.


## To run Production Server

```
export FLASK_ENV=production
python app.py
```

## To run Development Server

```
export FLASK_ENV=development
python app.py
```

## To setup your virtual environment with the necessary dependencies

```
virtualenv your_environment_name
source your_environment_name/bin/activate
pip install -r requirements.txt
```

Note: We will create bash script that will simplify this process later in the development process.

## Resources and Examples

- Flask Documentation:
  - https://flask-doc.readthedocs.io/en/latest/
  - https://flask.palletsprojects.com/en/1.1.x/quickstart/
  - https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment
  - https://github.com/jitsejan/python-flask-with-javascript
- MNIST Flask Apps
  - https://github.com/marcotompitak/mnist-canvas
- Deployment
  - Heroku
  - Flask integration wth Amazon S3: https://www.youtube.com/watch?v=rmpSPEzgVp4
- Flask-SQL Alchemy
  - https://www.youtube.com/watch?v=cYWiDiIUxQc
  - https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
  - https://www.youtube.com/watch?v=uZnp21fu8TQ
  - https://www.youtube.com/watch?v=1nxzOrLWiic
- MNIST Library
  - https://github.com/datapythonista/mnist

## When contributing to this project

If you are contributing to this project, you will probably have to install new python libraries. If so, make sure you record the libraries on the requirements.txt file by running the following command:

```
pip freeze > requirements.txt
```
