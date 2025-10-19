from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. SQLite Database URL:
# The file 'sql_app.db' will be created in your project directory (./).
# This file will persist all your goal data.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. The Engine: Connects SQLAlchemy to SQLite.
# 'check_same_thread=False' is needed for SQLite when using FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. SessionLocal: Used to talk to the database.
# This is the class that will create a new database session when instantiated.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base: The base class for all your database models (tables).
Base = declarative_base()

# 5. Dependency to get the database session (Crucial for FastAPI)
# This function is used by FastAPI endpoints to open and close a database session automatically.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
