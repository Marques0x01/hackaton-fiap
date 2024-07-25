from src.models.dtos.medico_dto import MedicoDTO, EnderecoMedicoDTO

def medico_to_dto(medico):
    endereco_dto = [endereco_to_dto(endereco).__dict__ for endereco in medico.endereco]
    return MedicoDTO(
        email=medico.email,
        nome=medico.nome,
        especialidade=medico.especialidade,
        crm=medico.crm,
        cnpj=medico.cnpj,
        endereco=endereco_dto
    )

def endereco_to_dto(endereco):
    return EnderecoMedicoDTO(
        cep=endereco.cep,
        numero=endereco.numero,
        estado=endereco.estado,
        municipio=endereco.municipio,
        bairro=endereco.bairro,
        rua=endereco.rua
    )
