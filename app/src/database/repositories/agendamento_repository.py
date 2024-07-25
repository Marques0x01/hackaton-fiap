from sqlalchemy.exc import IntegrityError
from src.database.models import Agendamento
from src.database.database import get_db


class AgendamentoRepository:

    def create_agendamento(self, horario_id: int, paciente_id: int, status: str):
        try:
            session = next(get_db())
            novo_agendamento = Agendamento(
                horario_id=horario_id,
                paciente_id=paciente_id,
                status=status
            )
            session.add(novo_agendamento)
            session.commit()
            session.refresh(novo_agendamento)
            return novo_agendamento
        except IntegrityError:
            session.rollback()
            raise ValueError("Erro de integridade ao tentar criar um agendamento.")
        except Exception as e:
            session.rollback()
            raise

    def get_agendamento_by_id(self, agendamento_id: int):
        session = next(get_db())
        return session.query(Agendamento).filter_by(agendamento_id=agendamento_id).first()

    def get_all_agendamentos(self):
        session = next(get_db())
        return session.query(Agendamento).all()

    def update_status(self, agendamento_id: int, **kwargs):
        try:
            session = next(get_db())            
            agendamento = self.get_agendamento_by_id(agendamento_id)
            if not agendamento:
                raise ValueError("Agendamento não encontrado.")

            for key, value in kwargs.items():
                if hasattr(agendamento, key):
                    setattr(agendamento, key, value)

            session.commit()
            return agendamento
        except IntegrityError:
            session.rollback()
            raise ValueError("Erro de integridade ao tentar atualizar o agendamento.")
        except Exception as e:
            session.rollback()
            raise
