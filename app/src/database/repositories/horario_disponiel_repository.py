

from app.src.database.database import SessionLocal
from app.src.database.models.Entities import HorarioDisponivel
from sqlalchemy.exc import NoResultFound


class HorarioDisponivelRepository():

    def get_horario(self, id):
        session = SessionLocal()
        try:
            return session.query(HorarioDisponivel).filter(HorarioDisponivel.horario_id == id).one()
        except NoResultFound:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()
