from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

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
    endereco = relationship('EnderecoMedico', back_populates='medico')
    horarios_disponiveis = relationship('HorarioDisponivel', back_populates='medico')
    compartilhamentos_prontuario = relationship('CompartilhamentoProntuario', back_populates='medico')
    avaliacoes = relationship('Avaliacao', back_populates='medico')

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
    medico = relationship('Medico', back_populates='endereco')

# Definir o modelo Paciente
class Paciente(Base):
    __tablename__ = 'paciente'
    paciente_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    nome = Column(String(255), nullable=False)
    data_nascimento = Column(Date)
    cpf = Column(String(50), unique=True, nullable=False)
    telefone = Column(String(50))
    
    # Relacionamentos
    endereco = relationship('EnderecoPaciente', back_populates='paciente', uselist=False)
    prontuario = relationship('Prontuario', back_populates='paciente', uselist=False)
    agendamentos = relationship('Agendamento', back_populates='paciente')
    avaliacoes = relationship('Avaliacao', back_populates='paciente')


# Definir o modelo EnderecoPaciente
class EnderecoPaciente(Base):
    __tablename__ = 'endereco_paciente'
    endereco_paciente_id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('paciente.paciente_id'))
    cep = Column(String(50))
    numero = Column(Integer)
    estado = Column(String(200))
    municipio = Column(String(200))
    bairro = Column(String(200))
    rua = Column(String(200))

    paciente = relationship('Paciente', back_populates='endereco')


# Definir o modelo Prontuario
class Prontuario(Base):
    __tablename__ = 'prontuario'
    
    prontuario_id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('paciente.paciente_id'))
    link_arquivo = Column(String(1000))
    
    # Relacionamento com Paciente
    paciente = relationship('Paciente', back_populates='prontuario')
    compartilhamentos = relationship('CompartilhamentoProntuario', back_populates='prontuario')


# Definir o modelo CompartilhamentoProntuario
class CompartilhamentoProntuario(Base):
    __tablename__ = 'compartilhamento_prontuario'
    
    compartilhamento_prontuario_id = Column(Integer, primary_key=True, autoincrement=True)
    prontuario_id = Column(Integer, ForeignKey('prontuario.prontuario_id'))
    medico_id = Column(Integer, ForeignKey('medico.medico_id'))
    data_inicio = Column(Time, nullable=False)
    data_fim = Column(Time, nullable=False)
    
    # Relacionamentos
    prontuario = relationship('Prontuario', back_populates='compartilhamentos')
    medico = relationship('Medico', back_populates='compartilhamentos_prontuario')


# Definir o modelo HorarioDisponivel
class HorarioDisponivel(Base):
    __tablename__ = 'horario_disponivel'
    horario_id = Column(Integer, primary_key=True, autoincrement=True)
    medico_id = Column(Integer, ForeignKey('medico.medico_id'))
    data = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    medico = relationship('Medico', back_populates='horarios_disponiveis')
    agendamentos = relationship('Agendamento', back_populates='horario')

    def to_dict(self):
        return {
            'horario_id': self.horario_id,
            'medico_id': self.medico_id,
            'data': self.data.isoformat(),
            'hora_inicio': str(self.hora_inicio),
            'hora_fim': str(self.hora_fim)
        }

class Agendamento(Base):
    __tablename__ = 'agendamento'
    agendamento_id = Column(Integer, primary_key=True, autoincrement=True)
    horario_id = Column(Integer, ForeignKey('horario_disponivel.horario_id'))
    paciente_id = Column(Integer, ForeignKey('paciente.paciente_id'))
    status = Column(String(50))

    horario = relationship('HorarioDisponivel', back_populates='agendamentos')
    paciente = relationship('Paciente', back_populates='agendamentos')


# Definir o modelo Avaliacao
class Avaliacao(Base):
    __tablename__ = 'avaliacao'
    
    avaliacao_id = Column(Integer, primary_key=True, autoincrement=True)
    medico_id = Column(Integer, ForeignKey('medico.medico_id'))
    paciente_id = Column(Integer, ForeignKey('paciente.paciente_id'))
    nota = Column(Integer, nullable=False)  # Verifique se há suporte para constraints como CHECK em sua versão do SQLAlchemy
    comentario = Column(Text)
    data_avaliacao = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    
    # Relacionamentos
    medico = relationship('Medico', back_populates='avaliacoes')
    paciente = relationship('Paciente', back_populates='avaliacoes')
