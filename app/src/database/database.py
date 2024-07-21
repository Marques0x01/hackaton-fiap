from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurar a conexão com o banco de dados
DATABASE_URL = "mysql+mysqlconnector://admin:123456789@localhost:3306/dopamina_hospital"  # Atualize com suas credenciais
engine = create_engine(DATABASE_URL, echo=True)

# Definir a base
Base = declarative_base()

# Criar uma sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
