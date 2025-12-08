import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Handle database URL for both SQLite (local) and PostgreSQL (Render)
    # Priority: USE_SQLITE env var > existing SQLite file > DATABASE_URL > default SQLite
    use_sqlite = os.environ.get("USE_SQLITE", "").lower() in ("true", "1", "yes")
    sqlite_path = os.path.join(BASE_DIR, "lawyerconnect.db")
    
    # On Render, prefer PostgreSQL unless explicitly using SQLite
    is_render = os.environ.get("RENDER") == "true" or os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    
    if use_sqlite and not is_render:
        # Use SQLite if explicitly requested and not on Render
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"
        print(f"Using SQLite database: {sqlite_path}")
    else:
        database_url = os.environ.get("DATABASE_URL")
        if database_url:
            # Render provides postgres:// but SQLAlchemy needs postgresql://
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
            SQLALCHEMY_DATABASE_URI = database_url
            print(f"Using PostgreSQL database from DATABASE_URL")
        else:
            # Default to SQLite for local development
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"
            print(f"Using SQLite database (default): {sqlite_path}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Session configuration for persistent login
    PERMANENT_SESSION_LIFETIME = 86400 * 30  # 30 days
    # Use secure cookies in production (HTTPS)
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production" or os.environ.get("RENDER") == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'





