class MedicoDTO:
    def __init__(self, email, nome, especialidade, crm, cnpj, endereco):
        self.email = email
        self.nome = nome
        self.especialidade = especialidade
        self.crm = crm
        self.cnpj = cnpj
        self.endereco = endereco

class EnderecoMedicoDTO:
    def __init__(self, cep, numero, estado, municipio, bairro, rua):
        self.cep = cep
        self.numero = numero
        self.estado = estado
        self.municipio = municipio
        self.bairro = bairro
        self.rua = rua

class HorarioDisponivelDTO:
    def __init__(self, medico_id, data, hora_inicio, hora_fim) -> None:
        self.medico_id=medico_id,
        self.data=data,
        self.hora_inicio=hora_inicio,
        self.hora_fim=hora_fim