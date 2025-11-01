from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Configuração do MongoDB
mongo_uri = "mongodb://localhost:27017/locadoraveiculos_db"  # Altere para a sua URI do MongoDB
client = MongoClient(mongo_uri)
db = client.locadoraveiculos_db

# Limpar coleções existentes (opcional, para garantir um estado limpo a cada execução)
db.tipo_veiculos.drop()
db.veiculos.drop()
db.funcionarios.drop()
db.clientes.drop()
db.reservas.drop()

# Inserir dados na coleção tipo_veiculos
tipo_veiculos_data = [
    {"modelo": "Corolla", "tipo_combustivel": "Gasolina", "capacidade_passageiros": 5},
    {"modelo": "Onix", "tipo_combustivel": "Etanol", "capacidade_passageiros": 5},
    {"modelo": "Ranger", "tipo_combustivel": "Diesel", "capacidade_passageiros": 2},
    {"modelo": "Gol", "tipo_combustivel": "Flex", "capacidade_passageiros": 5},
    {"modelo": "Prisma", "tipo_combustivel": "Gasolina", "capacidade_passageiros": 5},
    {"modelo": "Fiesta", "tipo_combustivel": "Diesel", "capacidade_passageiros": 5},
]
tipo_veiculos_ids = db.tipo_veiculos.insert_many(tipo_veiculos_data).inserted_ids

# Mapear os IDs inseridos para fácil acesso
tipo_veiculos_map = {tv["modelo"]: _id for tv, _id in zip(tipo_veiculos_data, tipo_veiculos_ids)}

# Inserir dados na coleção veiculos
veiculos_data = [
    {"placa": "ABC1234", "cor": "Preto", "quilometragem": 50000, "valor": 35000.00, "ar_condicionado": True, "marca": "Toyota", "id_tipo": tipo_veiculos_map["Corolla"], "ativo": True},
    {"placa": "DEF5678", "cor": "Prata", "quilometragem": 40000, "valor": 30000.00, "ar_condicionado": False, "marca": "Chevrolet", "id_tipo": tipo_veiculos_map["Onix"], "ativo": True},
    {"placa": "GHI91011", "cor": "Branco", "quilometragem": 60000, "valor": 50000.00, "ar_condicionado": True, "marca": "Ford", "id_tipo": tipo_veiculos_map["Ranger"], "ativo": True},
    {"placa": "JKL3456", "cor": "Vermelho", "quilometragem": 40000, "valor": 28000.00, "ar_condicionado": True, "marca": "Volkswagen", "id_tipo": tipo_veiculos_map["Gol"], "ativo": True},
    {"placa": "MNO6789", "cor": "Branco", "quilometragem": 35000, "valor": 25000.00, "ar_condicionado": False, "marca": "Chevrolet", "id_tipo": tipo_veiculos_map["Prisma"], "ativo": True},
    {"placa": "PQR9012", "cor": "Cinza", "quilometragem": 45000, "valor": 30000.00, "ar_condicionado": True, "marca": "Ford", "id_tipo": tipo_veiculos_map["Fiesta"], "ativo": True},
]
veiculos_ids = db.veiculos.insert_many(veiculos_data).inserted_ids

# Mapear as placas para os IDs do MongoDB
veiculos_map = {v["placa"]: _id for v, _id in zip(veiculos_data, veiculos_ids)}

# Inserir dados na coleção funcionarios
funcionarios_data = [
    {"nome": "João Silva", "cpf": "12345678901", "cargo": "Mecânico", "endereco": "Rua das Flores, 123", "salario": 2500.00, "dt_nasc": "1990-05-15", "ativo": True},
    {"nome": "Maria Santos", "cpf": "98765432109", "cargo": "Atendente", "endereco": "Av. Principal, 456", "salario": 2000.00, "dt_nasc": "1995-10-20", "ativo": True},
    {"nome": "José Oliveira", "cpf": "45678912306", "cargo": "Gerente", "endereco": "Rua das Palmeiras, 789", "salario": 3500.00, "dt_nasc": "1985-03-25", "ativo": True},
    {"nome": "Mariana Oliveira", "cpf": "78901234567", "cargo": "Secretária", "endereco": "Rua das Flores, 456", "salario": 1800.00, "dt_nasc": "1992-08-20", "ativo": True},
    {"nome": "Carlos Silva", "cpf": "34567890123", "cargo": "Atendente", "endereco": "Av. Central, 789", "salario": 2000.00, "dt_nasc": "1993-05-10", "ativo": True},
    {"nome": "Leticia Santos", "cpf": "90123456789", "cargo": "Mecânica", "endereco": "Rua dos Coqueiros, 123", "salario": 2200.00, "dt_nasc": "1991-12-15", "ativo": True},
]
funcionarios_ids = db.funcionarios.insert_many(funcionarios_data).inserted_ids

# Mapear CPFs para IDs do MongoDB
funcionarios_map = {f["cpf"]: _id for f, _id in zip(funcionarios_data, funcionarios_ids)}

# Inserir dados na coleção clientes
clientes_data = [
    {"dt_nasc": "1998-01-20", "cnh": "123456789", "nome": "Ana Souza", "cpf": "78945612302", "endereco": "Av. das Oliveiras, 789"},
    {"dt_nasc": "1980-09-05", "cnh": "987654321", "nome": "Pedro Rocha", "cpf": "65498732105", "endereco": "Rua das Pedras, 456"},
    {"dt_nasc": "1975-12-10", "cnh": "654321987", "nome": "Carla Lima", "cpf": "32165498708", "endereco": "Travessa das Flores, 123"},
]
clientes_ids = db.clientes.insert_many(clientes_data).inserted_ids

# Mapear CPFs para IDs do MongoDB
clientes_map = {c["cpf"]: _id for c, _id in zip(clientes_data, clientes_ids)}

# Inserir dados na coleção reservas
# Note que dt_reserva e dt_devolucao são armazenadas como strings ISO para compatibilidade com Flask/JSON
reservas_data = [
    {"cod_cliente": clientes_map["78945612302"], "id_funcionario": funcionarios_map["98765432109"], "placa_veiculo": "ABC1234", "valor": 150.00, "dt_reserva": "2024-05-10", "dt_devolucao": "2024-05-15", "status": "Finalizada"},
    {"cod_cliente": clientes_map["65498732105"], "id_funcionario": funcionarios_map["45678912306"], "placa_veiculo": "DEF5678", "valor": 200.00, "dt_reserva": "2024-06-01", "dt_devolucao": "2024-06-07", "status": "Finalizada"},
    {"cod_cliente": clientes_map["32165498708"], "id_funcionario": funcionarios_map["12345678901"], "placa_veiculo": "GHI91011", "valor": 180.00, "dt_reserva": "2024-07-20", "dt_devolucao": "2024-07-25", "status": "Finalizada"},
    
    # Novas reservas para simular mais atividade e desbalancear para Ana Souza
    # Ana Souza (78945612302) com mais reservas
    {"cod_cliente": clientes_map["78945612302"], "id_funcionario": funcionarios_map["98765432109"], "placa_veiculo": "ABC1234", "valor": 120.00, "dt_reserva": "2024-10-01", "dt_devolucao": "2024-10-03", "status": "Ativa"},
    {"cod_cliente": clientes_map["78945612302"], "id_funcionario": funcionarios_map["98765432109"], "placa_veiculo": "JKL3456", "valor": 250.00, "dt_reserva": "2024-11-10", "dt_devolucao": "2024-11-15", "status": "Ativa"},
    {"cod_cliente": clientes_map["78945612302"], "id_funcionario": funcionarios_map["45678912306"], "placa_veiculo": "PQR9012", "valor": 300.00, "dt_reserva": "2024-12-01", "dt_devolucao": "2024-12-05", "status": "Ativa"},
    {"cod_cliente": clientes_map["78945612302"], "id_funcionario": funcionarios_map["98765432109"], "placa_veiculo": "ABC1234", "valor": 100.00, "dt_reserva": "2025-01-05", "dt_devolucao": "2025-01-07", "status": "Ativa"},

    # Pedro Rocha (65498732105) com mais algumas reservas
    {"cod_cliente": clientes_map["65498732105"], "id_funcionario": funcionarios_map["34567890123"], "placa_veiculo": "MNO6789", "valor": 180.00, "dt_reserva": "2024-09-15", "dt_devolucao": "2024-09-18", "status": "Ativa"},
    {"cod_cliente": clientes_map["65498732105"], "id_funcionario": funcionarios_map["34567890123"], "placa_veiculo": "DEF5678", "valor": 220.00, "dt_reserva": "2025-02-01", "dt_devolucao": "2025-02-05", "status": "Ativa"},

    # Carla Lima (32165498708) com menos reservas
    {"cod_cliente": clientes_map["32165498708"], "id_funcionario": funcionarios_map["78901234567"], "placa_veiculo": "GHI91011", "valor": 160.00, "dt_reserva": "2024-11-20", "dt_devolucao": "2024-11-22", "status": "Ativa"},
]
db.reservas.insert_many(reservas_data)

print("Banco de dados MongoDB populado com sucesso!")
