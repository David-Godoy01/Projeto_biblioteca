from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String)
    alugado = Column(Boolean, default=False)
