from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy with connection pool settings for PostgreSQL
db = SQLAlchemy(
    engine_options={
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'max_overflow': 10,
    }
)

login_manager = LoginManager()
login_manager.login_view = "main.login"





