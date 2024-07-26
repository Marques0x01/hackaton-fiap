from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound
from src.database.database import get_db
from src.database.models.Entities import EnderecoMedico, Medico


class MedicoRepository:

    def find_all_doctors(self):
        session = next(get_db())
        try:
            # Eager load 'endereco' relationship
            doctors = session.query(Medico).options(joinedload(Medico.endereco)).all()
            return doctors
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()

    def find_doctor_by_crm(self, crm: str):
        session = next(get_db())
        try:
            # Eager load 'endereco' relationship
            return session.query(Medico).options(joinedload(Medico.endereco)).filter(Medico.crm == crm).one()
        except NoResultFound:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()

    def find_by_specialty_and_state(self, specialty: str, state: str):
        session = next(get_db())
        try:
            # Eager load 'endereco' relationship
            query = (
                session.query(Medico)
                .options(joinedload(Medico.endereco))
                .join(EnderecoMedico)
                .filter(
                    and_(
                        Medico.especialidade == specialty,
                        EnderecoMedico.estado == state
                    )
                )
            )
            return query.all()
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()

    def insert_doctor(self, doctor_data):
        try:
            session = next(get_db())
            address = doctor_data.get("endereco")
            novo_medico = Medico(
                nome=doctor_data.get("nome"),
                email=doctor_data.get("email"),
                crm=doctor_data.get("documento"),
                cnpj=doctor_data.get("cnpj"),
                especialidade=doctor_data.get("especialidade")
            )

            novo_endereco = EnderecoMedico(
                cep=address.get("cep"),
                numero=address.get("numero"),
                estado=address.get("estado"),
                municipio=address.get("pais"),
                bairro=address.get("bairro"),
                rua=address.get("rua"),
                medico=novo_medico
            )

            session.add(novo_medico)
            session.add(novo_endereco)
            session.commit()
            session.refresh(novo_medico)
            session.refresh(novo_endereco)
            return {'message': 'doctor has been registered'}
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            return {'message': str(e)}
        finally:
            session.close()
