from database.database import get_db
from sqlalchemy import and_
from database.models.Entities import HorarioDisponivel

class HorarioDisponivelRepository:

    def __init__(self) -> None:
        self.__session = next(get_db())

    def get_horario_disponivel_by_medico_id(self, medico_id: int):
            horario_disponivel = self.__session.query(HorarioDisponivel).filter(
                HorarioDisponivel.medico_id == medico_id
            ).all()
            return horario_disponivel
    def get_horario_disponivel_by_medico_id_and_horario_id(self, medico_id, horario_id):
        try:
            horario_disponivel = self.__session.query(HorarioDisponivel).filter(
                HorarioDisponivel.medico_id == medico_id,
                HorarioDisponivel.horario_id == horario_id
            ).first()
            return horario_disponivel
        except Exception as e:
            print(f"An error occurred while fetching the schedule: {e}")
            return None

    def create_horario_disponivel(self, medico_id, data, hora_inicio, hora_fim):
        try:
            novo_horario = HorarioDisponivel(
                medico_id=medico_id,
                data=data,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim
            )
            self.__session.add(novo_horario)
            self.__session.commit()
            self.__session.refresh(novo_horario)
            return novo_horario
        except Exception as e:
            self.__session.rollback()
            print(f"An error occurred: {e}")
            return {"message": str(e)}
        finally:
            self.__session.close()

    def update_horario_disponivel(self, horario_disponivel):
        try:
            self.__session.commit()
            self.__session.refresh(horario_disponivel)
            return horario_disponivel
        except Exception as e:
            self.__session.rollback()
            print(f"An error occurred while updating the schedule: {e}")
            return None
        finally:
            self.__session.close()