from database.database import get_db
from sqlalchemy import and_
from database.models.Entities import EnderecoMedico, Medico


class MedicoRepository:

    def __init__(self) -> None:
        self.__session = next(get_db())

    def find_all_doctors(self):
        return self.__session.query(Medico).all()

    def find_doctor_by_crm(self, crm: str):
        return self.__session.query(Medico).filter(Medico.crm == crm).first()

    def find_by_specialty_and_state(self, specialty: str, state: str):
        query = (
            self.__session.query(Medico)
            .join(EnderecoMedico)
            .filter(
                and_(
                    Medico.especialidade == specialty,
                    EnderecoMedico.estado == state
                )
            )
        )
        return query.all()

    def insert_doctor(self, doctor_data):
        try:
            doctor = doctor_data.get("doctor")
            address = doctor_data.get("address")
            print(doctor)
            novo_medico = Medico(
                nome=doctor.get("name"),
                email=doctor.get("email"),
                crm=doctor.get("crm"),
                cnpj=doctor.get("cnpj"),
                especialidade=doctor.get("speciality")
            )

            novo_endereco = EnderecoMedico(
                cep=address.get("cep"),
                numero=address.get("number"),
                estado=address.get("state"),
                municipio=address.get("county"),
                bairro=address.get("neighborhood"),
                rua=address.get("street"),
                medico=novo_medico
            )

            self.__session.add(novo_medico)
            self.__session.add(novo_endereco)

            self.__session.commit()
            return {'message': 'doctor has been registred'}
        except Exception as e:
            self.__session.rollback()
            print(f"An error occurred: {e}")
            return {'message': str(e)}
        finally:
            self.__session.close()
