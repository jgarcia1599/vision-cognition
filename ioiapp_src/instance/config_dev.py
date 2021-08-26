from datetime import timedelta
from instance import secret_keys_dev
# --- Development Config Class ----

# This is the Python Class that will contain the configuration used for development. This file will not be pushed to 
# production and will only be used when developing in your local host.


DEBUG = True

SQLALCHEMY_DATABASE_URI = secret_keys_dev.db_url

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY= secret_keys_dev.session_secret_key

SESSION_REFRESH_EACH_REQUEST = False

SESSION_COOKIE_SECURE = False

PERMANENT_SESSION_LIFETIME = timedelta(minutes=2)

#admin username for dashboard
ADMIN_USERNAME = "some admin"
ADMIN_PASSWORD = "some password"

MAX_TASK_NUMBER = 10

EXPERIMENT_1_ERASER_SIZES = [
    5,
    10,
    16,
    20,
    25,
    40,
    50,
    80,
    100,
    200
]