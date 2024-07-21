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
