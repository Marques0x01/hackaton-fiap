from database.database import SessionLocal, get_db
from database.models.Entities import EnderecoMedico, Medico


class MedicoRepository:

    def __init__(self) -> None:
        self.__session = next(get_db())

    def find_doctors(self):
        return self.__session.query(Medico).all()
    # Função para adicionar um médico e um endereço

    def create_doctor(self, doctor_data):
        session = SessionLocal()

        try:
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
                municipio=address.get("municipio"),
                bairro=address.get("bairro"),
                rua=address.get("rua"),
                medico=novo_medico
            )

            session.add(novo_medico)
            session.add(novo_endereco)

            session.commit()

            return {
                "user": doctor_data.get("documento"),
                "cnpj": doctor_data.get("cnpj")
            }
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close()
