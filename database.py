from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Conexão com banco SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
