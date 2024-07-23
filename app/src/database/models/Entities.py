from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


# Definir o modelo Medico
class Medico(Base):
    __tablename__ = 'medico'

    medico_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    nome = Column(String(255), nullable=False)
    especialidade = Column(String(255))
    crm = Column(String(50), unique=True, nullable=False)
    cnpj = Column(String(14), nullable=False)

    # Relacionamento com EnderecoMedico
    enderecos = relationship('EnderecoMedico', back_populates='medico')

# Definir o modelo EnderecoMedico


class EnderecoMedico(Base):
    __tablename__ = 'endereco_medico'

    endereco_medico_id = Column(Integer, primary_key=True, autoincrement=True)
    medico_id = Column(Integer, ForeignKey('medico.medico_id'))
    cep = Column(String(50))
    numero = Column(Integer)
    estado = Column(String(200))
    municipio = Column(String(200))
    bairro = Column(String(200))
    rua = Column(String(200))

    # Relacionamento com Medico
    medico = relationship('Medico', back_populates='enderecos')


class Paciente(Base):
    __tablename__ = 'paciente'
    paciente_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    nome = Column(String(255), nullable=False)
    data_nascimento = Column(Date)
    cpf = Column(String(50), unique=True, nullable=False)
    telefone = Column(String(50))

    enderecos = relationship('EnderecoPaciente', back_populates='paciente')
    prontuarios = relationship('Prontuario', back_populates='paciente')
    agendamentos = relationship('Agendamento', back_populates='paciente')
    avaliacoes = relationship('Avaliacao', back_populates='paciente')
    autenticacao = relationship(
        'AutenticacaoPaciente', back_populates='paciente', uselist=False)


class EnderecoPaciente(Base):
    __tablename__ = 'endereco_paciente'
    endereco_paciente_id = Column(
        Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('paciente.paciente_id'))
    cep = Column(String(50))
    numero = Column(Integer)
    estado = Column(String(200))
    municipio = Column(String(200))
    bairro = Column(String(200))
    rua = Column(String(200))

    paciente = relationship('Paciente', back_populates='enderecos')

class HorarioDisponivel(Base):
    __tablename__ = 'horario_disponivel'
    horario_id = Column(Integer, primary_key=True, autoincrement=True)
    medico_id = Column(Integer, ForeignKey('medico.medico_id'))
    data = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    medico = relationship('Medico', back_populates='horarios')
    agendamentos = relationship('Agendamento', back_populates='horario')


class Agendamento(Base):
    __tablename__ = 'agendamento'
    agendamento_id = Column(Integer, primary_key=True, autoincrement=True)
    horario_id = Column(Integer, ForeignKey('horario_disponivel.horario_id'))
    paciente_id = Column(Integer, ForeignKey('paciente.paciente_id'))
    status = Column(String(50))

    horario = relationship('HorarioDisponivel', back_populates='agendamentos')
    paciente = relationship('Paciente', back_populates='agendamentos')