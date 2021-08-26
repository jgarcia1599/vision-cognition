
from datetime import timedelta
import secret_keys

# --- Production Config Class ----

# This is the Python Class that will contain the configuration used for production.

# SQLALCHEMY_DATABASE_URI, SECRET_KEY ,MTUKUSER_AWS_ACCESS_KEY_ID and , MTURKUSER_AWS_SECRET_ACCESS_KEY contain
# sensitive information that cannot and should not be pushed to github. As such, they are all contained in a git-ignored file called secret_keys.py

DEBUG = True

SQLALCHEMY_DATABASE_URI = secret_keys.db_url

SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_COOKIE_SECURE = False

SESSION_REFRESH_EACH_REQUEST = False

SECRET_KEY= secret_keys.session_secret_key

PERMANENT_SESSION_LIFETIME = timedelta(minutes=7200)

# secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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