from src.database.database import Base, engine
from src.database.models.Entities import *

Base.metadata.create_all(bind=engine)
