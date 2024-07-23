from database.database import Base, engine
from database.models.Entities import *

Base.metadata.create_all(bind=engine)
