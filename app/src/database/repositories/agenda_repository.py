from src.database.database import SessionLocal
from src.database.models.Entities import Agendamento
from src.exception.CustomException import EntityNotFoundException


class AgendaRepository():

    def save_agenda(self, agenda_id, paciente_id, status):
        session = SessionLocal()

        try:
            novo_agendamento = Agendamento(
                horario_id=agenda_id,
                paciente_id=paciente_id,
                status=status
            )

            session.add(novo_agendamento)
            session.commit()

            return {
                "agendamento_id": novo_agendamento.agendamento_id,
                "status": novo_agendamento.status
            }

        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise e

        finally:
            session.close()

    def get_por_id(self, agenda_id):
        session = SessionLocal()
        try:
            schedule = session.query(Agendamento).filter(
                Agendamento.horario_id == agenda_id).first()
            return schedule
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()

    def update_status(self, agenda_id, status):
        session = SessionLocal()
        try:
            # Encontrar o agendamento pelo ID
            appointment = session.query(Agendamento).filter(
                Agendamento.agendamento_id == agenda_id).first()

            if appointment:
                # Atualizar o status
                appointment.status = status
                session.commit()

                return {
                    "agenda_id": appointment.agendamento_id,
                    "status": appointment.status
                }
            else:
                raise EntityNotFoundException("Appointment not found")

        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise e

        finally:
            session.close()
