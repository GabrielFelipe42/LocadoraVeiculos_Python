import sys
import json
from flask import Flask, request, jsonify
from psutil import process_iter
from signal import SIGTERM
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

app = Flask(__name__)
engine = create_engine('postgresql://neondb_owner:npg_S8TCvi2xVwzP@ep-shy-heart-acwxgxm7-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

# =================== ROTAS FUNCIONARIOS  =================== 
@app.route("/get_all_funcionarios", methods=["GET"])
def get_all_funcionarios():
    query = text("SELECT nome, cpf, cargo, salario, endereco, dt_nasc, ativo FROM funcionarios")
    with engine.connect() as connection:
        result = connection.execute(query)
        funcionarios = []
        for row in result.fetchall():
            # Convert each row to a dictionary manually
            funcionario = {
                    "nome": row[0],
                    "cpf": row[1],
                    "cargo": row[2],
                    "salario": row[3],
                    "endereco": row[4],
                    "dt_nasc": row[5],
                    "ativo": row[6]
                    # Add more fields as needed
                    }
            funcionarios.append(funcionario)

    return jsonify(funcionarios)

@app.route("/cadastrar_funcionario", methods=["POST"])
def cadastrar_funcionario():
    # Obter os dados do funcionário a partir do corpo da requisição
    data = request.json
    nome = data.get('nome')
    cpf = data.get('cpf')
    cargo = data.get('cargo')
    endereco = data.get('endereco')
    salario = data.get('salario')
    dt_nasc = data.get('dt_nasc')

    # Utilize parâmetros na consulta SQL para evitar injeção de SQL
    query = text("INSERT INTO funcionarios (nome, cpf, cargo, endereco, salario, dt_nasc, ativo) "
                 "VALUES (:nome, :cpf, :cargo, :endereco, :salario, :dt_nasc, true)")

    # Inserir os dados do funcionário na tabela 'funcionario'
    with engine.connect() as connection:
        connection.execute(query, {
            'nome': nome,
            'cpf': cpf,
            'cargo': cargo,
            'endereco': endereco,
            'salario': salario,
            'dt_nasc': dt_nasc
        })
        connection.commit()

    return jsonify({"message": "Funcionário cadastrado com sucesso!"})


@app.route("/promover_funcionario/<string:cpf>", methods=["PUT"])
def promover_funcionario(cpf):
    # Obter os novos dados do funcionário a partir do corpo da requisição
    data = request.json
    novo_cargo = data.get('cargo')
    novo_salario = data.get('salario')

    query = text("""UPDATE funcionarios
                    SET cargo = :novo_cargo, salario = :novo_salario
                    WHERE cpf = :cpf""")

    # Atualizar o cargo e o salário do funcionário na tabela 'funcionario'
    with engine.connect() as connection:
        connection.execute(query, {
            'novo_cargo': novo_cargo,
            'novo_salario': novo_salario,
            'cpf': cpf
        })
        connection.commit()

    return f"Dados do funcionário com CPF {cpf} atualizados com sucesso!"


@app.route("/alterar_endereco_funcionario/<string:cpf>", methods=["PUT"])
def alterar_endereco_funcionario(cpf):
    data = request.json
    novo_endereco = data.get('endereco')
    
    query = text("UPDATE funcionarios SET endereco = :novo_endereco WHERE cpf = :cpf")

    # Atualizar o endereço do funcionário na tabela 'funcionarios'
    with engine.connect() as connection:
        connection.execute(query, {'novo_endereco': novo_endereco, 'cpf': cpf})
        connection.commit()

    return f"Endereço do funcionário com CPF {cpf} alterado com sucesso!"

@app.route("/demitir_funcionario/<string:cpf>", methods=["DELETE"])
def demitir_funcionario(cpf):
    query = text("UPDATE funcionarios SET ativo = false WHERE cpf = :cpf")

    with engine.connect() as connection:
        connection.execute(query, {'cpf': cpf})
        connection.commit()

    return f"Funcionário com cpf {cpf} foi demitido com sucesso!"


# =================== ROTAS TIPO DE VEICULOS =================== 
@app.route("/get_all_tipo_veiculos", methods=["GET"])
def get_all_tipo_veiculos():
    query = text("SELECT id_tipo, modelo, tipo_combustivel, capacidade_passageiros FROM tipo_veiculos")

    with engine.connect() as connection:
        result = connection.execute(query)
        tipos = []
        for row in result.fetchall():
            tipo = {
                "id_tipo": row[0],
                "modelo": row[1],
                "tipo_combustivel": row[2],
                "capacidade_passageiros": row[3]
            }
            tipos.append(tipo)

    return jsonify(tipos)

@app.route("/cadastrar_tipo_veiculo", methods=["POST"])
def cadastrar_tipo_veiculo():
    data = request.json
    modelo = data.get('modelo')
    tipo_combustivel = data.get('tipo_combustivel')
    capacidade_passageiros = data.get('capacidade_passageiros')

    query = text("INSERT INTO tipo_veiculos (modelo, tipo_combustivel, capacidade_passageiros) "
                 "VALUES (:modelo, :tipo_combustivel, :capacidade_passageiros)")

    with engine.connect() as connection:
        connection.execute(query, {
            'modelo': modelo,
            'tipo_combustivel': tipo_combustivel,
            'capacidade_passageiros': capacidade_passageiros
        })
        connection.commit()

    return jsonify({"message": "Tipo de veículo cadastrado com sucesso!"})

# =================== ROTAS VEICULOS =================== 
@app.route("/get_all_veiculos", methods=["GET"])
def get_all_veiculos():
    query = text("""
        SELECT v.placa, v.cor, v.quilometragem, v.valor, v.ar_condicionado, 
               v.marca, v.id_tipo, v.ativo, tv.modelo, tv.tipo_combustivel, tv.capacidade_passageiros
        FROM veiculos v 
        JOIN tipo_veiculos tv ON v.id_tipo = tv.id_tipo
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        veiculos = []
        for row in result.fetchall():
            veiculo = {
                "placa": row[0],
                "cor": row[1],
                "quilometragem": row[2],
                "valor": row[3],
                "ar_condicionado": row[4],
                "marca": row[5],
                "id_tipo": row[6],
                "ativo": row[7],
                "modelo": row[8],
                "tipo_combustivel": row[9],
                "capacidade_passageiros": row[10]
            }
            veiculos.append(veiculo)

    return jsonify(veiculos)


@app.route("/tirar_veiculo_frota/<string:placa>", methods=["DELETE"])
def tirar_veiculo_frota(placa):
    query = text("UPDATE veiculos SET ativo = False WHERE placa = :placa")
    with engine.connect() as connection:
        connection.execute(query, {
            "placa": placa
            })
        connection.commit()
        
    return f"Veículo com placa {placa} foi retirado da frota com sucesso!"

@app.route("/adicionar_veiculo", methods=["POST"])
def adicionar_veiculo():
    data = request.json
    placa = data.get('placa')
    cor = data.get('cor')
    marca = data.get('marca')
    quilometragem = data.get('quilometragem')
    valor = data.get('valor')
    ar_condicionado = data.get('ar_condicionado')
    id_tipo = data.get('id_tipo')
    ativo = data.get('ativo', True) 
    
    query = text("""INSERT INTO veiculos (placa, cor, marca, quilometragem, valor, ar_condicionado, id_tipo, ativo) VALUES
            (:placa, :cor, :marca, :quilometragem, :valor, :ar_condicionado, :id_tipo, :ativo)""")
    
    with engine.connect() as connection:
        connection.execute(query, {
                'placa': placa,
                'cor': cor,
                'marca': marca,
                'quilometragem': quilometragem, 
                'valor': valor,
                'ar_condicionado': ar_condicionado,
                'id_tipo': id_tipo,
                'ativo': ativo
            })
        connection.commit()

    return jsonify({"message": "Veículo adicionado com sucesso!"})
# =========================================================== 

# =================== ROTAS CLIENTES =================== 
@app.route("/get_all_clientes", methods=["GET"])
def get_all_clientes():
    query = text("SELECT cod_cliente, nome, cpf, dt_nasc, endereco, cnh FROM clientes")
    with engine.connect() as connection:
        result = connection.execute(query)
        clientes = []
        for row in result.fetchall():
            # Convert each row to a dictionary manually
            cliente = {
                    "cod_cliente": row[0],
                    "nome": row[1],
                    "cpf": row[2],
                    "dt_nasc": row[3],
                    "endereco": row[4],
                    "cnh": row[5],
                    # Add more fields as needed
                    }
            clientes.append(cliente)

    return jsonify(clientes)

@app.route("/alterar_endereco_cliente/<string:cpf>", methods=["PUT"])
def alterar_endereco_cliente(cpf):
    data = request.json
    novo_endereco = data.get('endereco')

    query = text("UPDATE clientes SET endereco = :novo_endereco WHERE cpf = :cpf")

    with engine.connect() as connection:
        connection.execute(query, {'cpf': cpf, 'novo_endereco': novo_endereco})
        connection.commit()

    return jsonify({"message": f"Endereço do cliente com CPF {cpf} alterado com sucesso!"})

@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():
    data = request.json
    dt_nasc = data.get('dt_nasc')
    cnh = data.get('cnh')
    nome = data.get('nome')
    cpf = data.get('cpf')
    endereco = data.get('endereco')

    query = text("INSERT INTO clientes (dt_nasc, cnh, nome, cpf, endereco) "
                 "VALUES (:dt_nasc, :cnh, :nome, :cpf, :endereco)")

    with engine.connect() as connection:
        connection.execute(query,{
            'dt_nasc': dt_nasc,
            'cnh': cnh,
            'nome': nome,
            'cpf': cpf,
            'endereco': endereco
        })
        connection.commit()
    return jsonify({"message": "Cliente cadastrado com sucesso!"})
# =========================================== 
@app.route("/fazer_reserva", methods=["POST"])
def fazer_reserva():
    # Recebendo os dados da requisição
    data = request.json
    cpf = data.get("cpf")

    cod_cliente = 0

    # Obtendo o código do cliente a partir do CPF
    query_cod_cliente = text("SELECT cod_cliente FROM clientes WHERE cpf = :cpf")
    with engine.connect() as connection:
        result = connection.execute(query_cod_cliente, {"cpf": cpf})
        row = result.fetchone()
        if row:
            cod_cliente = row[0]
        else:
            return "Cliente não encontrado", 404

    cpf_funcionario = data.get("cpf_funcionario")

    # Obtendo o ID do funcionário a partir do CPF
    query_id_funcionario = text("SELECT id_funcionario FROM funcionarios WHERE cpf = :cpf_funcionario")
    with engine.connect() as connection:
        result = connection.execute(query_id_funcionario, {"cpf_funcionario": cpf_funcionario})
        row = result.fetchone()
        if row:
            id_funcionario = row[0]
        else:
            return "Funcionário não encontrado", 404

    dias = int(data.get("dias"))
    dt_reserva = data.get("dt_reserva")

    # Calcular a data de devolução
    dt_reserva_obj = datetime.fromisoformat(dt_reserva)
    dt_devolucao_obj = dt_reserva_obj + timedelta(days=dias)
    dt_devolucao = dt_devolucao_obj.isoformat()

    id_tipo = data.get("id_tipo")
    
    # Obter valor médio dos veículos deste tipo para cálculo
    query_valor_tipo = text("SELECT AVG(valor) FROM veiculos WHERE id_tipo = :id_tipo AND ativo = true")
    with engine.connect() as connection:
        result = connection.execute(query_valor_tipo, {"id_tipo": id_tipo})
        row = result.fetchone()
        if row and row[0]:
            vlr_medio_tipo = row[0]
        else:
            return "Tipo de veículo não encontrado ou sem veículos disponíveis", 404

    # Calcular o valor da reserva
    valor = calcular_valor_reserva(vlr_medio_tipo, dias)
    status = data.get("status", "Ativa")

    # Gravar na tabela reservas
    query_reservas = text("INSERT INTO reservas (cod_cliente, id_funcionario, id_tipo, valor, dt_reserva, dt_devolucao, status) VALUES (:cod_cliente, :id_funcionario, :id_tipo, :valor, :dt_reserva, :dt_devolucao, :status)")
    with engine.connect() as connection:
        connection.execute(query_reservas, {
            "cod_cliente": cod_cliente,
            "id_funcionario": id_funcionario,
            "id_tipo": id_tipo,
            "valor": valor,
            "dt_reserva": dt_reserva,
            "dt_devolucao": dt_devolucao,
            "status": status
        })
        connection.commit()
    print("Reserva realizada com sucesso!")
    return jsonify(valor)


@app.route("/get_all_reservas", methods=["GET"])
def get_all_reservas():
    query = text("""
        SELECT r.cod_reserva, r.cod_cliente, r.id_funcionario, r.id_tipo, r.valor, 
               r.dt_reserva, r.dt_devolucao, r.status, tv.modelo, tv.tipo_combustivel
        FROM reservas r 
        JOIN tipo_veiculos tv ON r.id_tipo = tv.id_tipo
    """)
    with engine.connect() as connection:
        result = connection.execute(query)
        reservas = []
        for row in result.fetchall():
            reserva = {
                "cod_reserva": row[0],
                "cod_cliente": row[1],
                "id_funcionario": row[2],
                "id_tipo": row[3],
                "valor": row[4],
                "dt_reserva": row[5],
                "dt_devolucao": row[6],
                "status": row[7],
                "modelo": row[8],
                "tipo_combustivel": row[9]
            }
            reservas.append(reserva)

    return jsonify(reservas)

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
