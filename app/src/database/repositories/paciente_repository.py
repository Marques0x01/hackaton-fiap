from sqlalchemy.exc import NoResultFound
from src.database.database import get_db
from src.database.models.Entities import EnderecoPaciente, Paciente

class PacienteRepository():
    
    def save_paciente(self, paciente_data):
        session = next(get_db())

        try:
            endereco = paciente_data.get("endereco")

            novo_paciente = Paciente(
                nome=paciente_data.get("nome"),
                email=paciente_data.get("email"),
                data_nascimento=paciente_data.get("data_nascimento"),
                telefone=paciente_data.get("telefone"),
                cpf=paciente_data.get("documento")
            )

            novo_endereco = EnderecoPaciente(
                cep=endereco.get("cep"),
                numero=endereco.get("numero"),
                estado=endereco.get("estado"),
                municipio=endereco.get("municipio"),
                bairro=endereco.get("bairro"),
                rua=endereco.get("rua"),
                paciente=novo_paciente
            )

            session.add(novo_paciente)
            session.add(novo_endereco)
            session.commit()
            session.refresh(novo_paciente)
            session.refresh(novo_endereco)

            return {
                "user": paciente_data.get("documento"),
                "email": paciente_data.get("email")
            }
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()

    def get_paciente_por_id(self, cpf):
        session = next(get_db())
        try:
            return session.query(Paciente).filter(Paciente.cpf == cpf).one()
        except NoResultFound:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()
