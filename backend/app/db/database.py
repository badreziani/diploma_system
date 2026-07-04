from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a local SQLite file named 'diplomas.db' inside your backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./diplomas.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is required only for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session in your routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()