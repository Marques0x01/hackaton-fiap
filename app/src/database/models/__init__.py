from database.database import Base, engine
from database.models.Entities import Medico, EnderecoMedico

Base.metadata.create_all(bind=engine)
