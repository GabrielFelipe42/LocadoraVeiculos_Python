import sys
import json
from flask import Flask, request, jsonify
from psutil import process_iter
from signal import SIGTERM
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId # Importar ObjectId para lidar com IDs do MongoDB

app = Flask(__name__)

# Configuração do MongoDB
mongo_uri = "mongodb://localhost:27017/locadoraveiculos_db"  # Altere para a sua URI do MongoDB
client = MongoClient(mongo_uri)
db = client.locadoraveiculos_db # Nome do seu banco de dados

# =================== ROTAS FUNCIONARIOS  =================== 
@app.route("/get_all_funcionarios", methods=["GET"])
def get_all_funcionarios():
    funcionarios_collection = db.funcionarios
    funcionarios = []
    for funcionario in funcionarios_collection.find():
        funcionario["_id"] = str(funcionario["_id"]) # Converte ObjectId para string
        funcionarios.append(funcionario)

    return jsonify(funcionarios)

@app.route("/cadastrar_funcionario", methods=["POST"])
def cadastrar_funcionario():
    data = request.json
    nome = data.get('nome')
    cpf = data.get('cpf')
    cargo = data.get('cargo')
    endereco = data.get('endereco')
    salario = data.get('salario')
    dt_nasc = data.get('dt_nasc')

    funcionarios_collection = db.funcionarios
    funcionario_data = {
        "nome": nome,
        "cpf": cpf,
        "cargo": cargo,
        "endereco": endereco,
        "salario": salario,
        "dt_nasc": dt_nasc,
        "ativo": True
    }
    funcionarios_collection.insert_one(funcionario_data)

    return jsonify({"message": "Funcionário cadastrado com sucesso!"})

@app.route("/promover_funcionario/<string:cpf>", methods=["PUT"])
def promover_funcionario(cpf):
    data = request.json
    novo_cargo = data.get('cargo')
    novo_salario = data.get('salario')

    funcionarios_collection = db.funcionarios
    result = funcionarios_collection.update_one({"cpf": cpf}, {"$set": {"cargo": novo_cargo, "salario": novo_salario}})

    if result.modified_count > 0:
        return f"Dados do funcionário com CPF {cpf} atualizados com sucesso!"
    else:
        return f"Funcionário com CPF {cpf} não encontrado ou sem alterações." , 404

@app.route("/alterar_endereco_funcionario/<string:cpf>", methods=["PUT"])
def alterar_endereco_funcionario(cpf):
    data = request.json
    novo_endereco = data.get('endereco')
    
    funcionarios_collection = db.funcionarios
    result = funcionarios_collection.update_one({"cpf": cpf}, {"$set": {"endereco": novo_endereco}})

    if result.modified_count > 0:
        return f"Endereço do funcionário com CPF {cpf} alterado com sucesso!"
    else:
        return f"Funcionário com CPF {cpf} não encontrado ou sem alterações.", 404

@app.route("/demitir_funcionario/<string:cpf>", methods=["DELETE"])
def demitir_funcionario(cpf):
    funcionarios_collection = db.funcionarios
    result = funcionarios_collection.update_one({"cpf": cpf}, {"$set": {"ativo": False}})

    if result.modified_count > 0:
        return f"Funcionário com cpf {cpf} foi demitido com sucesso!"
    else:
        return f"Funcionário com CPF {cpf} não encontrado.", 404

# =================== ROTAS TIPO DE VEICULOS =================== 
@app.route("/get_all_tipo_veiculos", methods=["GET"])
def get_all_tipo_veiculos():
    tipo_veiculos_collection = db.tipo_veiculos
    tipos = []
    for tipo in tipo_veiculos_collection.find():
        tipos.append({
            "id_tipo": str(tipo["_id"]), # Converte ObjectId para string
            "modelo": tipo["modelo"],
            "tipo_combustivel": tipo["tipo_combustivel"],
            "capacidade_passageiros": tipo["capacidade_passageiros"]
        })

    return jsonify(tipos)

@app.route("/cadastrar_tipo_veiculo", methods=["POST"])
def cadastrar_tipo_veiculo():
    data = request.json
    modelo = data.get('modelo')
    tipo_combustivel = data.get('tipo_combustivel')
    capacidade_passageiros = data.get('capacidade_passageiros')

    tipo_veiculos_collection = db.tipo_veiculos
    tipo_veiculo_data = {
        "modelo": modelo,
        "tipo_combustivel": tipo_combustivel,
        "capacidade_passageiros": capacidade_passageiros
    }
    tipo_veiculos_collection.insert_one(tipo_veiculo_data)

    return jsonify({"message": "Tipo de veículo cadastrado com sucesso!"})

# =================== ROTAS VEICULOS =================== 
@app.route("/get_all_veiculos", methods=["GET"])
def get_all_veiculos():
    veiculos_collection = db.veiculos
    veiculos = []
    for veiculo in veiculos_collection.find():
        tipo_veiculo = db.tipo_veiculos.find_one({"_id": veiculo["id_tipo"]})
        veiculos.append({
            "_id": str(veiculo["_id"]), # Converte ObjectId para string
            "placa": veiculo["placa"],
            "cor": veiculo["cor"],
            "quilometragem": veiculo["quilometragem"],
            "valor": veiculo["valor"],
            "ar_condicionado": veiculo["ar_condicionado"],
            "marca": veiculo["marca"],
            "id_tipo": str(veiculo["id_tipo"]), # Converte ObjectId para string
            "ativo": veiculo["ativo"],
            "modelo": tipo_veiculo["modelo"],
            "tipo_combustivel": tipo_veiculo["tipo_combustivel"],
            "capacidade_passageiros": tipo_veiculo["capacidade_passageiros"]
        })

    return jsonify(veiculos)

@app.route("/tirar_veiculo_frota/<string:placa>", methods=["DELETE"])
def tirar_veiculo_frota(placa):
    veiculos_collection = db.veiculos
    result = veiculos_collection.update_one({"placa": placa}, {"$set": {"ativo": False}})
    if result.modified_count > 0:
        return f"Veículo com placa {placa} foi retirado da frota com sucesso!"
    else:
        return f"Veículo com placa {placa} não encontrado ou sem alterações.", 404

@app.route("/adicionar_veiculo", methods=["POST"])
def adicionar_veiculo():
    data = request.json
    placa = data.get('placa')
    cor = data.get('cor')
    marca = data.get('marca')
    quilometragem = data.get('quilometragem')
    valor = data.get('valor')
    ar_condicionado = data.get('ar_condicionado')
    id_tipo_str = data.get('id_tipo') # Recebe como string
    ativo = data.get('ativo', True) 

    # Validar e converter id_tipo para ObjectId
    if not ObjectId.is_valid(id_tipo_str):
        return jsonify({"message": "ID do tipo de veículo inválido."}), 400
    id_tipo = ObjectId(id_tipo_str)

    # Verificar se o id_tipo existe
    tipo_veiculo_existente = db.tipo_veiculos.find_one({"_id": id_tipo})
    if not tipo_veiculo_existente:
        return jsonify({"message": "Tipo de veículo não encontrado."}), 404
    
    veiculos_collection = db.veiculos
    veiculo_data = {
        "placa": placa,
        "cor": cor,
        "marca": marca,
        "quilometragem": quilometragem, 
        "valor": valor,
        "ar_condicionado": ar_condicionado,
        "id_tipo": id_tipo, # Agora é um ObjectId
        "ativo": ativo
    }
    veiculos_collection.insert_one(veiculo_data)

    return jsonify({"message": "Veículo adicionado com sucesso!"})

# =========================================================== 

# =================== ROTAS CLIENTES =================== 
@app.route("/get_all_clientes", methods=["GET"])
def get_all_clientes():
    clientes_collection = db.clientes
    clientes = []
    for cliente in clientes_collection.find():
        clientes.append({
            "cod_cliente": str(cliente["_id"]), # Converte ObjectId para string
            "nome": cliente["nome"],
            "cpf": cliente["cpf"],
            "dt_nasc": cliente["dt_nasc"],
            "endereco": cliente["endereco"],
            "cnh": cliente["cnh"]
        })

    return jsonify(clientes)

@app.route("/alterar_endereco_cliente/<string:cpf>", methods=["PUT"])
def alterar_endereco_cliente(cpf):
    data = request.json
    novo_endereco = data.get('endereco')

    clientes_collection = db.clientes
    cliente_data = {"endereco": novo_endereco}
    clientes_collection.update_one({"cpf": cpf}, {"$set": cliente_data})

    return jsonify({"message": f"Endereço do cliente com CPF {cpf} alterado com sucesso!"})

@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():
    data = request.json
    dt_nasc = data.get('dt_nasc')
    cnh = data.get('cnh')
    nome = data.get('nome')
    cpf = data.get('cpf')
    endereco = data.get('endereco')

    clientes_collection = db.clientes
    cliente_data = {
        "dt_nasc": dt_nasc,
        "cnh": cnh,
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco
    }
    clientes_collection.insert_one(cliente_data)
    return jsonify({"message": "Cliente cadastrado com sucesso!"})
# =========================================== 
@app.route("/fazer_reserva", methods=["POST"])
def fazer_reserva():
    # Recebendo os dados da requisição
    data = request.json
    cpf = data.get("cpf")

    cod_cliente = 0

    # Obtendo o código do cliente a partir do CPF
    clientes_collection = db.clientes
    cliente = clientes_collection.find_one({"cpf": cpf})
    if cliente:
        cod_cliente = cliente["_id"]
    else:
        return "Cliente não encontrado", 404

    cpf_funcionario = data.get("cpf_funcionario")

    # Obtendo o ID do funcionário a partir do CPF
    funcionarios_collection = db.funcionarios
    funcionario = funcionarios_collection.find_one({"cpf": cpf_funcionario})
    if funcionario:
        id_funcionario = funcionario["_id"]
    else:
        return "Funcionário não encontrado", 404

    dias = int(data.get("dias"))
    dt_reserva = data.get("dt_reserva")

    # Calcular a data de devolução
    dt_reserva_obj = datetime.fromisoformat(dt_reserva)
    dt_devolucao_obj = dt_reserva_obj + timedelta(days=dias)
    dt_devolucao = dt_devolucao_obj.isoformat()

    # Modificado para receber a placa_veiculo diretamente
    placa_veiculo = data.get("placa_veiculo")

    # Verificar se o veículo existe e está ativo
    veiculos_collection = db.veiculos
    veiculo = veiculos_collection.find_one({"placa": placa_veiculo, "ativo": True})
    if not veiculo:
        return jsonify({"message": "Veículo não encontrado ou inativo."}), 404
    valor_veiculo = veiculo["valor"]

    # Verificar se o veículo já está reservado no período
    reservas_collection = db.reservas
    reserva_existente = reservas_collection.find_one({
        "placa_veiculo": placa_veiculo,
        "status": "Ativa",
        "$or": [
            {"$and": [{"dt_reserva": {"$lte": dt_reserva_obj.isoformat()}}, {"dt_devolucao": {"$gte": dt_reserva_obj.isoformat()}}]},
            {"$and": [{"dt_reserva": {"$lte": dt_devolucao_obj.isoformat()}}, {"dt_devolucao": {"$gte": dt_devolucao_obj.isoformat()}}]},
            {"$and": [{"dt_reserva": {"$gte": dt_reserva_obj.isoformat()}}, {"dt_devolucao": {"$lte": dt_devolucao_obj.isoformat()}}]}
        ]
    })

    if reserva_existente:
        return jsonify({"message": "Veículo já reservado para o período selecionado."}), 409 # Conflict

    # Calcular o valor da reserva com base no valor do veículo específico
    valor = calcular_valor_reserva(valor_veiculo, dias)
    status = data.get("status", "Ativa")

    # Gravar na tabela reservas (com placa_veiculo)
    reservas_collection.insert_one({
        "cod_cliente": cod_cliente,
        "id_funcionario": id_funcionario,
        "placa_veiculo": placa_veiculo,
        "valor": valor,
        "dt_reserva": dt_reserva,
        "dt_devolucao": dt_devolucao,
        "status": status
    })
    print("Reserva realizada com sucesso!")
    return jsonify(valor)

@app.route("/get_all_reservas", methods=["GET"])
def get_all_reservas():
    reservas_collection = db.reservas
    reservas = []
    for reserva in reservas_collection.find():
        veiculo = db.veiculos.find_one({"placa": reserva["placa_veiculo"]})
        tipo_veiculo = db.tipo_veiculos.find_one({"_id": veiculo["id_tipo"]})
        reservas.append({
            "cod_reserva": str(reserva["_id"]),
            "cod_cliente": str(reserva["cod_cliente"]),
            "id_funcionario": str(reserva["id_funcionario"]),
            "placa_veiculo": reserva["placa_veiculo"],
            "valor": reserva["valor"],
            "dt_reserva": reserva["dt_reserva"],
            "dt_devolucao": reserva["dt_devolucao"],
            "status": reserva["status"],
            "modelo": tipo_veiculo["modelo"],
            "tipo_combustivel": tipo_veiculo["tipo_combustivel"]
        })

    return jsonify(reservas)

@app.route("/get_reservas_by_cliente", methods=["POST"])
def get_reservas_by_cliente():
    data = request.json
    cpf_cliente = data.get("cpf")

    if not cpf_cliente:
        return jsonify({"message": "CPF do cliente é obrigatório"}), 400

    clientes_collection = db.clientes
    cliente = clientes_collection.find_one({"cpf": cpf_cliente})
    if not cliente:
        return jsonify({"message": "Cliente não encontrado."}), 404

    reservas_collection = db.reservas
    reservas_cliente = []
    for reserva in reservas_collection.find({"cod_cliente": cliente["_id"]}):
        veiculo = db.veiculos.find_one({"placa": reserva["placa_veiculo"]})
        tipo_veiculo = db.tipo_veiculos.find_one({"_id": veiculo["id_tipo"]})
        reservas_cliente.append({
            "cod_reserva": str(reserva["_id"]),
            "cod_cliente": str(reserva["cod_cliente"]),
            "id_funcionario": str(reserva["id_funcionario"]),
            "placa_veiculo": reserva["placa_veiculo"],
            "valor": reserva["valor"],
            "dt_reserva": reserva["dt_reserva"],
            "dt_devolucao": reserva["dt_devolucao"],
            "status": reserva["status"],
            "modelo": tipo_veiculo["modelo"],
            "tipo_combustivel": tipo_veiculo["tipo_combustivel"],
            "nome_cliente": cliente["nome"]
        })

    if not reservas_cliente:
        return jsonify({"message": "Nenhuma reserva encontrada para o CPF fornecido."}), 404

    return jsonify(reservas_cliente)

@app.route("/relatorio_veiculos_mais_alugados", methods=["GET"])
def relatorio_veiculos_mais_alugados():
    reservas_collection = db.reservas
    relatorio = []
    for result in reservas_collection.aggregate([
        {"$group": {"_id": "$placa_veiculo", "numero_reservas": {"$sum": 1}}},
        {"$sort": {"numero_reservas": -1}}
    ]):
        veiculo_id = result["_id"]
        count = result["numero_reservas"]
        veiculo = db.veiculos.find_one({"placa": veiculo_id})
        if veiculo: # Adicionar verificação para o caso de o veículo não ser encontrado
            tipo_veiculo = db.tipo_veiculos.find_one({"_id": veiculo["id_tipo"]})
            if tipo_veiculo:
                relatorio.append({
                    "placa": veiculo["placa"],
                    "marca": veiculo["marca"],
                    "modelo": tipo_veiculo["modelo"],
                    "tipo_combustivel": tipo_veiculo["tipo_combustivel"],
                    "numero_reservas": count
                })
    
    if not relatorio:
        return jsonify({"message": "Nenhum veículo encontrado em reservas."}), 404

    return jsonify(relatorio)

@app.route("/relatorio_faturamento_por_periodo", methods=["POST"])
def relatorio_faturamento_por_periodo():
    data = request.json
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")
    num_meses = data.get("num_meses")

    # Se num_meses for fornecido, ou se nenhuma data for fornecida, calcula o período
    if num_meses is not None:
        try:
            num_meses = int(num_meses)
            if num_meses <= 0:
                return jsonify({"message": "Número de meses deve ser um valor positivo."}), 400
        except ValueError:
            return jsonify({"message": "Número de meses inválido."}), 400

        end_date_obj = datetime.now()
        start_date_obj = end_date_obj - timedelta(days=num_meses * 30) # Aproximação
        
        start_date_str = start_date_obj.isoformat()
        end_date_str = end_date_obj.isoformat()
    elif not start_date_str or not end_date_str: # Se nenhuma data for fornecida, usa padrão de 3 meses
        end_date_obj = datetime.now()
        start_date_obj = end_date_obj - timedelta(days=3 * 30) # Padrão de 3 meses
        
        start_date_str = start_date_obj.isoformat()
        end_date_str = end_date_obj.isoformat()
    
    # Validação e conversão de datas se foram fornecidas explicitamente
    try:
        start_date = datetime.fromisoformat(start_date_str).date()
        end_date = datetime.fromisoformat(end_date_str).date()
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    reservas_collection = db.reservas
    pipeline = [
        {"$match": {
            "dt_reserva": {"$gte": start_date_str, "$lte": end_date_str}}},
        {"$group": {
            "_id": None,
            "faturamento_total": {"$sum": "$valor"},
            "numero_reservas": {"$sum": 1}
        }}
    ]
    faturamento_result = next(reservas_collection.aggregate(pipeline), {"faturamento_total": 0.0, "numero_reservas": 0})

    return jsonify({
        "periodo_inicio": start_date_str.split('T')[0],
        "periodo_fim": end_date_str.split('T')[0],
        "faturamento_total": faturamento_result["faturamento_total"],
        "numero_reservas": faturamento_result["numero_reservas"]
    })

@app.route("/relatorio_clientes_mais_reservas", methods=["GET"])
def relatorio_clientes_mais_reservas():
    reservas_collection = db.reservas
    relatorio = []
    for result in reservas_collection.aggregate([
        {"$group": {"_id": "$cod_cliente", "numero_reservas": {"$sum": 1}}},
        {"$sort": {"numero_reservas": -1}}
    ]):
        cliente_id = result["_id"]
        count = result["numero_reservas"]
        cliente = db.clientes.find_one({"_id": cliente_id})
        if cliente: # Adicionar verificação para o caso de o cliente não ser encontrado
            relatorio.append({
                "nome_cliente": cliente["nome"],
                "cpf_cliente": cliente["cpf"],
                "numero_reservas": count
            })
    
    if not relatorio:
        return jsonify({"message": "Nenhum cliente encontrado com reservas."}), 404

    return jsonify(relatorio)

@app.route("/get_available_veiculos", methods=["GET"])
def get_available_veiculos():
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    if not start_date_str or not end_date_str:
        return jsonify({"message": "Datas de início e fim são obrigatórias."}), 400

    try:
        start_date = datetime.fromisoformat(start_date_str).date()
        end_date = datetime.fromisoformat(end_date_str).date()
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    # Buscar reservas ativas que se sobrepõem ao período desejado
    reservas_conflitantes = db.reservas.find({
        "status": "Ativa",
        "$or": [
            {"$and": [{"dt_reserva": {"$lte": end_date_str}}, {"dt_devolucao": {"$gte": start_date_str}}]},
            {"$and": [{"dt_reserva": {"$gte": start_date_str}}, {"dt_devolucao": {"$lte": end_date_str}}]}
        ]
    })
    placas_reservadas = [reserva["placa_veiculo"] for reserva in reservas_conflitantes]

    # Buscar veículos ativos que não estão nas placas reservadas
    veiculos_collection = db.veiculos
    available_veiculos = []
    for veiculo in veiculos_collection.find({"ativo": True, "placa": {"$nin": placas_reservadas}}):
        tipo_veiculo = db.tipo_veiculos.find_one({"_id": veiculo["id_tipo"]})
        available_veiculos.append({
            "placa": veiculo["placa"],
            "marca": veiculo["marca"],
            "modelo": tipo_veiculo["modelo"],
            "tipo_combustivel": tipo_veiculo["tipo_combustivel"],
            "valor": veiculo["valor"],
            "ar_condicionado": veiculo["ar_condicionado"]
        })
    
    if not available_veiculos:
        return jsonify({"message": "Nenhum veículo disponível para o período selecionado."}), 404

    return jsonify(available_veiculos)

def calcular_valor_reserva(vlr_carro, dias):
    vlr = float(vlr_carro)
    temp = int(dias)
    valor_por_dia = (0.001 * vlr) + 10
    return valor_por_dia * temp

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True, port=8080)
