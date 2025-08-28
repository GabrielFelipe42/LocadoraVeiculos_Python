CREATE TABLE veiculos (
    placa VARCHAR(10) PRIMARY KEY,
    tipo_comb VARCHAR(255),
    cor VARCHAR(255),
    marca VARCHAR(255),
    modelo VARCHAR(255),
    kms NUMERIC,
    vlr_car NUMERIC,
    ar_cond BOOLEAN,
    ativo BOOLEAN
);

CREATE TABLE funcionarios (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(255),
    cpf VARCHAR(11),
    cargo VARCHAR(255),
    endereco VARCHAR(255),
    salario NUMERIC,
    dt_nasc DATE,
    ativo BOOLEAN
);


CREATE TABLE clientes (
    cod_cliente SERIAL PRIMARY KEY,
    dt_nasc DATE,
    cnh VARCHAR(50),
    nome VARCHAR(255),
    cpf VARCHAR(11),
    endereco VARCHAR(255)
);

CREATE TABLE reservas (
    cod_reserva SERIAL PRIMARY KEY,
    cod_cliente INTEGER,
    id_funcionario INTEGER,
    valor NUMERIC,
    dt_reserva DATE,
    dt_devolucao DATE,
    FOREIGN KEY (cod_cliente) REFERENCES clientes(cod_cliente),
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);

CREATE TABLE veiculos_reservados (
    cod_reserva INTEGER,
    placa VARCHAR(50),
    PRIMARY KEY (cod_reserva, placa),
    FOREIGN KEY (cod_reserva) REFERENCES reservas(cod_reserva),
    FOREIGN KEY (placa) REFERENCES veiculos(placa)
);


-- Inserir dados na tabela de veículos
INSERT INTO veiculos (placa, tipo_comb, cor, marca, modelo, kms, vlr_car, ar_cond, ativo) 
VALUES 
    ('ABC1234', 'Gasolina', 'Preto', 'Toyota', 'Corolla', 50000, 35000.00, true, true),
    ('DEF5678', 'Etanol', 'Prata', 'Chevrolet', 'Onix', 40000, 30000.00, false, true),
    ('GHI91011', 'Diesel', 'Branco', 'Ford', 'Ranger', 60000, 50000.00, true, true),
    ('JKL3456', 'Flex', 'Vermelho', 'Volkswagen', 'Gol', 40000, 28000.00, true, true),
    ('MNO6789', 'Gasolina', 'Branco', 'Chevrolet', 'Prisma', 35000, 25000.00, false, true),
    ('PQR9012', 'Diesel', 'Cinza', 'Ford', 'Fiesta', 45000, 30000.00, true, true);

-- Inserir dados na tabela de funcionários
INSERT INTO funcionarios (nome, cpf, cargo, endereco, salario, dt_nasc, ativo) 
VALUES 
    ('João Silva', '12345678901', 'Mecânico', 'Rua das Flores, 123', 2500.00, '1990-05-15', true),
    ('Maria Santos', '98765432109', 'Atendente', 'Av. Principal, 456', 2000.00, '1995-10-20', true),
    ('José Oliveira', '45678912306', 'Gerente', 'Rua das Palmeiras, 789', 3500.00, '1985-03-25', true),
    ('Mariana Oliveira', '78901234567', 'Secretária', 'Rua das Flores, 456', 1800.00, '1992-08-20', true),
    ('Carlos Silva', '34567890123', 'Atendente', 'Av. Central, 789', 2000.00, '1993-05-10', true),
    ('Leticia Santos', '90123456789', 'Mecânica', 'Rua dos Coqueiros, 123', 2200.00, '1991-12-15', true);


-- Inserir dados na tabela de clientes
INSERT INTO clientes (dt_nasc, cnh, nome, cpf, endereco) 
VALUES 
    ('1998-01-20', '123456789', 'Ana Souza', '78945612302', 'Av. das Oliveiras, 789'),
    ('1980-09-05', '987654321', 'Pedro Rocha', '65498732105', 'Rua das Pedras, 456'),
    ('1975-12-10', '654321987', 'Carla Lima', '32165498708', 'Travessa das Flores, 123');

-- Inserir dados na tabela de reservas
INSERT INTO reservas (cod_cliente, id_funcionario, valor, dt_reserva, dt_devolucao) 
VALUES 
    (1, 2, 150.00, '2024-05-10', '2024-05-15'),
    (2, 3, 200.00, '2024-06-01', '2024-06-07'),
    (3, 1, 180.00, '2024-07-20', '2024-07-25');

-- Inserir dados na tabela de veículos reservados
INSERT INTO veiculos_reservados (cod_reserva, placa) 
VALUES 
    (1, 'ABC1234'),
    (2, 'DEF5678'),
    (3, 'GHI91011');