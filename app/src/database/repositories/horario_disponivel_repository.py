from sqlalchemy import and_, not_
from sqlalchemy.exc import NoResultFound
from src.database.database import get_db
from src.database.models.Entities import HorarioDisponivel, Agendamento

class HorarioDisponivelRepository:

    def get_horario_by_id(self, horario_id: int):
        session = next(get_db())
        try:
            return session.query(HorarioDisponivel).filter(HorarioDisponivel.horario_id == horario_id).one()
        except NoResultFound:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()


    def get_horario_disponivel_by_medico_id(self, medico_id: int):
        session = next(get_db())
        # Subconsulta para obter todos os IDs de horários agendados
        subquery = session.query(Agendamento.horario_id).filter(
            Agendamento.horario_id == HorarioDisponivel.horario_id
        ).subquery()
        
        # Consulta principal para obter os horários disponíveis
        horarios_disponiveis = session.query(HorarioDisponivel).filter(
            HorarioDisponivel.medico_id == medico_id,
            not_(HorarioDisponivel.horario_id.in_(subquery))
        ).all()

        return horarios_disponiveis
    def get_horario_disponivel_by_medico_id_and_horario_id(self, medico_id, horario_id):
        try:
            session = next(get_db())
            horario_disponivel = session.query(HorarioDisponivel).filter(
                HorarioDisponivel.medico_id == medico_id,
                HorarioDisponivel.horario_id == horario_id
            ).first()
            return horario_disponivel
        except Exception as e:
            print(f"An error occurred while fetching the schedule: {e}")
            return None

    def create_horario_disponivel(self, medico_id, data, hora_inicio, hora_fim):
        try:
            session = next(get_db())
            novo_horario = HorarioDisponivel(
                medico_id=medico_id,
                data=data,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim
            )
            session.add(novo_horario)
            session.commit()
            session.refresh(novo_horario)
            return novo_horario
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            return {"message": str(e)}
        finally:
            session.close()

    def update_horario_disponivel(self, horario_disponivel):
        try:
            session = next(get_db())
            session.commit()
            session.refresh(horario_disponivel)
            return horario_disponivel
        except Exception as e:
            session.rollback()
            print(f"An error occurred while updating the schedule: {e}")
            return None
        finally:
            session.close()