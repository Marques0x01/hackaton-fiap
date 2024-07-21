# Hackathon FIAP 2024

## Criação de MVP para agendamento e consulta com médicos


## Docker para DB do projeto 
``` bash
docker run --name dopamina_hospital -e MYSQL_ROOT_PASSWORD=123456789 -e MYSQL_DATABASE=dopamina_hospital -e MYSQL_USER=admin -e MYSQL_PASSWORD=123456789 -p 3306:3306 -d mysql:latest
```
### Criação de tabelas
``` sql

CREATE TABLE medico (
    medico_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    especialidade VARCHAR(255),
    crm VARCHAR(50) UNIQUE NOT NULL,
    cnpj VARCHAR(14) NOT NULL
);

-- 1 medico para 1 autenticacao_medico
CREATE TABLE autenticacao_medico (
    auth_id INT PRIMARY KEY AUTO_INCREMENT,
    medico_id INT,
    crm VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medico_id) REFERENCES medico(medico_id)
);

-- 1 endereco_medico para 1 medico
CREATE TABLE endereco_medico (
    endereco_medico_id INT PRIMARY KEY AUTO_INCREMENT,
    medico_id INT, -- Coluna adicionada para a chave estrangeira
    cep VARCHAR(50),
    numero INT,
    estado VARCHAR(200),
    municipio VARCHAR(200),
    bairro VARCHAR(200),
    rua VARCHAR(200),
    FOREIGN KEY (medico_id) REFERENCES medico(medico_id)
);

CREATE TABLE paciente (
    paciente_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(50)
);

-- 1 paciente para 1 autenticacao_paciente
CREATE TABLE autenticacao_paciente (
    auth_id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT,
    usuario VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES paciente(paciente_id)
);

-- 1 endereco_paciente para 1 paciente
CREATE TABLE endereco_paciente (
    endereco_paciente_id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT, -- Coluna adicionada para a chave estrangeira
    cep VARCHAR(50),
    numero INT,
    estado VARCHAR(200),
    municipio VARCHAR(200),
    bairro VARCHAR(200),
    rua VARCHAR(200),
    FOREIGN KEY (paciente_id) REFERENCES paciente(paciente_id)
);

-- 1 prontuario para 1 paciente
CREATE TABLE prontuario (
    prontuario_id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT,
    link_arquivo VARCHAR(1000),
    FOREIGN KEY (paciente_id) REFERENCES paciente(paciente_id)
);

-- 1 prontuario para 1 compartilhamento_prontuario e um medico para um compartilhamento_prontuario
CREATE TABLE compartilhamento_prontuario (
    compartilhamento_prontuario_id INT PRIMARY KEY AUTO_INCREMENT,
    prontuario_id INT,
    medico_id INT,
    data_inicio TIME NOT NULL,
    data_fim TIME NOT NULL,
    FOREIGN KEY (prontuario_id) REFERENCES prontuario(prontuario_id),
    FOREIGN KEY (medico_id) REFERENCES medico(medico_id)
);

-- 1 medico para muitos horario_disponivel
CREATE TABLE horario_disponivel (
    horario_id INT PRIMARY KEY AUTO_INCREMENT,
    medico_id INT,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES medico(medico_id)
);

-- 1 paciente para muitos agendamento e 1 horario_disponivel para 1 agendamento
CREATE TABLE agendamento (
    agendamento_id INT PRIMARY KEY AUTO_INCREMENT,
    horario_id INT,
    paciente_id INT,
    status VARCHAR(50),
    FOREIGN KEY (horario_id) REFERENCES horario_disponivel(horario_id),
    FOREIGN KEY (paciente_id) REFERENCES paciente(paciente_id)
);

-- 1 medico para muitas avaliacao e muitos pacientes para muitas avaliacao
CREATE TABLE avaliacao (
    avaliacao_id INT PRIMARY KEY AUTO_INCREMENT,
    medico_id INT,
    paciente_id INT,
    nota INT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medico_id) REFERENCES medico(medico_id),
    FOREIGN KEY (paciente_id) REFERENCES paciente(paciente_id)
);

```