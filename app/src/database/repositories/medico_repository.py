from database.database import get_db
from database.models.Entities import EnderecoMedico, Medico


class MedicoRepository:

    def __init__(self) -> None:
        self.__session = next(get_db())

    def find_doctors(self):
        return self.__session.query(Medico).all()
    # Função para adicionar um médico e um endereço

    def create_doctor(self, doctor_data):
        # session = get_db()
        print(doctor_data)
        print(type(doctor_data))

        try:
            address = doctor_data.get("address", {'rua': 'oscaralho'})

            novo_medico = Medico(
                nome=doctor_data.get("nome", 'jamal'),
                email=doctor_data.get("email"),
                crm=doctor_data.get("crm"),
                cnpj=doctor_data.get("cnpj")
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

            self.__session.add(novo_medico)
            self.__session.add(novo_endereco)

            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            print(f"An error occurred: {e}")
        finally:
            self.__session.close()
