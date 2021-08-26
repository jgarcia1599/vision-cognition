# Flask libraries
from flask import Flask,session
from flask_cors import CORS, cross_origin
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Everything else
from flask_bootstrap import Bootstrap

# Setting up the Flask app
app = Flask(__name__, instance_relative_config=True)

# Choose confing varables based on type of environrment
if app.config["ENV"] == "production":
    print("Production Environment")
    app.config.from_object('config')
else:
    print("Development environment")
    app.config.from_pyfile('config_dev.py')




# instantiate db 
db = SQLAlchemy(app)
# setup migrations with flask-migrate
migrate = Migrate(app, db)


# Wrapp app in Bootstrap
bootstrap = Bootstrap(app)

# Allow Cross-Origin Resource Sharing
cors = CORS(app)

# import routes
from image_occlusion import routes
