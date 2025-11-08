import json
import requests
from datetime import datetime, timedelta

local_host = "http://127.0.0.1:8080"

def tirar_veiculo_frota():
    placa = input("Qual a placa do veiculo: ")
    response = requests.delete(local_host + f"/tirar_veiculo_frota/{placa}")

    if response.status_code == 200:
        return "Veiculo retirado com sucesso!"
    else:
        return "Erro ao retirar o veiculo"

def get_all_tipo_veiculos():
    response = requests.get(local_host + "/get_all_tipo_veiculos")
    
    if response.status_code == 200:
        tipos = response.json()
        for tipo in tipos:
            print("ID:", tipo["id_tipo"])
            print("Modelo:", tipo["modelo"])
            print("Tipo de combustível:", tipo["tipo_combustivel"])
            print("Capacidade de passageiros:", tipo["capacidade_passageiros"])
            print("#####################################")
    else:
        return "Erro ao listar tipos de veículos"

def cadastrar_tipo_veiculo():
    modelo = input("Modelo: ")
    tipo_combustivel = input("Tipo de combustível: ")
    capacidade_passageiros = int(input("Capacidade de passageiros: "))

    novo_tipo = {
        "modelo": modelo,
        "tipo_combustivel": tipo_combustivel,
        "capacidade_passageiros": capacidade_passageiros
    }

    response = requests.post(local_host + "/cadastrar_tipo_veiculo", json=novo_tipo)
    
    if response.status_code == 200:
        return "Tipo de veículo cadastrado com sucesso!"
    else:
        return "Erro ao cadastrar o tipo de veículo."

def adicionar_veiculo():
    get_all_tipo_veiculos()
    id_tipo = input("ID do tipo de veículo: ") # Alterado para receber como string
    placa = input("Placa do veículo: ")
    cor = input("Cor: ")
    marca = input("Marca: ")
    quilometragem = int(input("Quilometragem: "))
    valor = int(input("Valor carro: "))
    ar_condicionado = bool(int(input("Possui ar condicionado ? [1/0]: ")))
    ativo = bool(int(input("Participa da frota ativa ? [1/0]: ")))

    novo_veiculo = {
        "placa": placa,
        "cor": cor,
        "marca": marca,
        "quilometragem": quilometragem,
        "valor": valor,
        "ar_condicionado": ar_condicionado,
        "id_tipo": id_tipo, # Enviado como string para a API
        "ativo": ativo
    }

    response = requests.post(local_host + "/adicionar_veiculo", json=novo_veiculo)
    
    if response.status_code == 200:
        return "Veículo cadastrado com sucesso!"
    elif response.status_code == 400:
        return response.json().get("message", "Erro ao cadastrar o veículo: ID do tipo de veículo inválido.")
    elif response.status_code == 404:
        return response.json().get("message", "Erro ao cadastrar o veículo: Tipo de veículo não encontrado.")
    else:
        return "Erro ao cadastrar o veículo."


def get_all_veiculos():
    response = requests.get(local_host + "/get_all_veiculos");

    if response.status_code == 200:
        veiculos = response.json()
        for veiculo in veiculos:
            if (veiculo["ativo"] == False):
                continue
            else:
                print("Marca:", veiculo["marca"])
                print("Modelo:", veiculo["modelo"])
                print("Valor:", veiculo["valor"])
                print("Tipo de combustível:", veiculo["tipo_combustivel"])
                print("Capacidade de passageiros:", veiculo["capacidade_passageiros"])
                print("Ar condicionado:", veiculo["ar_condicionado"])
                print("Placa:", veiculo["placa"])
                print("Quilometragem:", veiculo["quilometragem"])
                print("#####################################") 
    else:
        return "Erro ao listar veículos"

def get_all_funcionarios():
    response = requests.get(local_host + "/get_all_funcionarios")

    if response.status_code == 200:
        funcionarios = response.json()
        print("\n--- Lista de Funcionários ---")
        for i, funcionario in enumerate(funcionarios):
            if funcionario["ativo"] == True:
                print(f"{i+1}. Nome: {funcionario['nome']}, CPF: {funcionario['cpf']}, Cargo: {funcionario['cargo']}")
        print("---------------------------")
        return funcionarios
    else:
        print("Erro ao listar funcionários")
        return None


def get_all_clientes():
    response = requests.get(local_host + "/get_all_clientes")

    if response.status_code == 200:
        clientes = response.json()
        print("\n--- Lista de Clientes ---")
        for i, cliente in enumerate(clientes):
            print(f"{i+1}. Nome: {cliente['nome']}, CPF: {cliente['cpf']}")
        print("---------------------------")
        return clientes
    else:
        print("Erro ao listar clientes")
        return None

def alterar_endereco_cliente():
    clientes = get_all_clientes()
    if not clientes:
        return "Não foi possível listar clientes para alterar o endereço."

    while True:
        try:
            escolha_cliente = int(input("Selecione o número do cliente para alterar o endereço: "))
            if 1 <= escolha_cliente <= len(clientes):
                cpf = clientes[escolha_cliente - 1]['cpf']
                break
            else:
                print("Seleção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    novo_endereco = input("Novo endereço: ")

    cliente_data = {"endereco": novo_endereco }
    
    response = requests.put(local_host + f"/alterar_endereco_cliente/{cpf}", json=cliente_data)
    if response.status_code == 200:
        return "Endereço do cliente alterado com sucesso!"
    elif response.status_code == 404:
        return response.json().get("message", f"Cliente com CPF {cpf} não encontrado.")
    else:
        return response.json().get("message", "Erro ao alterar o endereço do cliente.")


def cadastrar_cliente():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    dt_nasc = input("Data de nascimento (no formato YYYY-MM-DD): ")
    endereco = input("Endereço: ")
    cnh = input("CNH: ") # Corrigido o erro de digitação

    # Criar o dicionário com os dados do cliente
    cliente_data = {
        "nome": nome,
        "cpf": cpf,
        "dt_nasc": dt_nasc,
        "endereco": endereco,
        "cnh": cnh
    }

    response = requests.post(local_host + "/cadastrar_cliente", json=cliente_data)
    
    # Verificar o status da resposta
    if response.status_code == 200:
        return "Cliente cadastrado com sucesso!"
    else:
        return response.json().get("message", "Erro ao cadastrar o cliente.")

def cadastrar_funcionario():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    dt_nasc = input("Data de nascimento (no formato YYYY-MM-DD): ")
    endereco = input("Endereço: ")
    cargo = input("Cargo: ")
    salario = input("Salario: ")

    cliente_data = {
        "nome": nome,
        "cpf": cpf,
        "dt_nasc": dt_nasc,
        "endereco": endereco,
        "cargo": cargo,
        "salario": salario
    }

    response = requests.post(local_host + "/cadastrar_funcionario", json=cliente_data)
    
    # Verificar o status da resposta
    if response.status_code == 200:
        return "Funcionário cadastrado com sucesso!"
    else:
        return "Erro ao cadastrar o funcionario."

def promover_funcionario():
    listar_funcionarios()
    cpf = input("CPF do funcionario: ")
    novo_cargo = input("Novo cargo: ")
    novo_salario = input("Novo salario: ")

    # Criar o dicionário com os dados do cliente
    func_data = {
        "cargo": novo_cargo,
        "salario": novo_salario
    }

    response = requests.put(local_host + f"/promover_funcionario/{cpf}", json=func_data)
    
    # Verificar o status da resposta
    if response.status_code == 200:
        return "funcionario promovido com sucesso!"
    else:
        return "Erro ao promover o funcionario."

def listar_funcionarios():
    response = requests.get(local_host + "/get_all_funcionarios")
    if response.status_code == 200:
        funcionarios = response.json()
        print("\n--- Lista de Funcionários ---")
        for f in funcionarios:
            print(f"Nome: {f['nome']}, CPF: {f['cpf']}, Cargo: {f['cargo']}")
        print("---------------------------")
    else:
        print("Erro ao listar funcionários.")

def alterar_endereco_funcionario():
    listar_funcionarios()
    cpf = input("CPF do funcionario: ")
    novo_endereco = input("Novo endereco: ")

    # Criar o dicionário com os dados do cliente
    cliente_data = { "endereco": novo_endereco }

    response = requests.put(local_host + "/alterar_endereco_funcionario/" + cpf, json=cliente_data)
    if response.status_code == 200:
        return "endereco do funcionario alterado com sucesso!"
    else:
        return "Erro ao alterar o endereco do funcionario."

def calcular_valor_reserva_local(vlr_carro, dias):
    vlr = float(vlr_carro)
    temp = int(dias)
    valor_por_dia = (0.001 * vlr) + 10
    return valor_por_dia * temp

def demitir_funcionario():
    listar_funcionarios()
    cpf = input("CPF do funcionario: ")

    response = requests.delete(local_host + "/demitir_funcionario/" + cpf);

    if response.status_code == 200:
        return "Funcionario demitido com sucesso"
    else:
        return "Erro ao demitir funcionario."

def get_all_reservas():
    response = requests.get(local_host + "/get_all_reservas")

    if response.status_code == 200:
        reservas = response.json()
        for reserva in reservas:
            print("Código da reserva:", reserva["cod_reserva"])
            print("Código do cliente:", reserva["cod_cliente"])
            print("ID do funcionário:", reserva["id_funcionario"])
            print("Placa do veículo:", reserva["placa_veiculo"])
            print("Tipo de veículo:", reserva["modelo"], "(" + reserva["tipo_combustivel"] + ")")
            print("Valor:", reserva["valor"])
            print("Data da reserva:", reserva["dt_reserva"])
            print("Data de devolução:", reserva["dt_devolucao"])
            print("Status:", reserva["status"])
            print("#####################################")
    else:
        return "Erro ao listar reservas"


def get_reservas_by_cliente_cli():
    get_all_clientes() # Adicionado para listar os clientes antes de pedir o CPF
    cpf_cliente = input("Digite o CPF do cliente para ver as reservas: ")
    
    payload = {"cpf": cpf_cliente}
    response = requests.post(local_host + "/get_reservas_by_cliente", json=payload)

    if response.status_code == 200:
        reservas = response.json()
        print(f"\n--- Relatório de Reservas para o Cliente (CPF: {cpf_cliente}) ---")
        for reserva in reservas:
            print("Código da reserva:", reserva["cod_reserva"])
            print("Nome do Cliente:", reserva["nome_cliente"])
            print("Placa do veículo:", reserva["placa_veiculo"])
            print("Tipo de veículo:", reserva["modelo"], "(" + reserva["tipo_combustivel"] + ")")
            print("Valor:", reserva["valor"])
            print("Data da reserva:", reserva["dt_reserva"])
            print("Data de devolução:", reserva["dt_devolucao"])
            print("Status:", reserva["status"])
            print("#####################################")
        return "Relatório gerado com sucesso!"
    elif response.status_code == 404:
        return response.json().get("message", "Nenhuma reserva encontrada para o CPF fornecido.")
    else:
        return response.json().get("message", "Erro ao gerar relatório de reservas por cliente.")


def relatorio_veiculos_mais_alugados_cli():
    response = requests.get(local_host + "/relatorio_veiculos_mais_alugados")

    if response.status_code == 200:
        relatorio = response.json()
        print("\n--- Relatório de Veículos Mais Alugados ---")
        for veiculo in relatorio:
            print("Placa:", veiculo["placa"])
            print("Marca:", veiculo["marca"])
            print("Modelo:", veiculo["modelo"])
            print("Tipo de combustível:", veiculo["tipo_combustivel"])
            print("Número de Reservas:", veiculo["numero_reservas"])
            print("#####################################")
        return "Relatório gerado com sucesso!"
    elif response.status_code == 404:
        return response.json().get("message", "Nenhum veículo encontrado em reservas.")
    else:
        return response.json().get("message", "Erro ao gerar relatório de veículos mais alugados.")


def relatorio_faturamento_por_periodo_cli():
    print("\n--- Relatório de Faturamento por Período ---")
    
    payload = {}
    escolha = input("Deseja informar um período (P) ou o número de meses (M)? [P/M]: ").upper()

    if escolha == 'P':
        start_date = input("Digite a data de início (YYYY-MM-DD): ")
        end_date = input("Digite a data de fim (YYYY-MM-DD): ")
        payload = {"start_date": start_date, "end_date": end_date}
    elif escolha == 'M':
        num_meses = input("Digite o número de meses para o relatório (ex: 3 para últimos 3 meses): ")
        payload = {"num_meses": num_meses}
    else:
        print("Opção inválida. Gerando relatório padrão para os últimos 3 meses.")
        # API já tem um padrão, então podemos enviar um payload vazio ou apenas para indicar a intenção
        payload = {"num_meses": 3} # Enviando explicitamente 3 meses como padrão

    response = requests.post(local_host + "/relatorio_faturamento_por_periodo", json=payload)

    if response.status_code == 200:
        relatorio = response.json()
        periodo_inicio = relatorio.get("periodo_inicio")
        periodo_fim = relatorio.get("periodo_fim")
        faturamento_total = relatorio.get("faturamento_total")
        numero_reservas = relatorio.get("numero_reservas")
        
        print(f"Período: {periodo_inicio} a {periodo_fim}")
        print(f"Faturamento Total: R$ {faturamento_total:.2f}")
        print(f"Número Total de Reservas: {numero_reservas}")
        print("#####################################")
        return "Relatório de faturamento gerado com sucesso!"
    else:
        return response.json().get("message", "Erro ao gerar relatório de faturamento por período.")


def relatorio_clientes_mais_reservas_cli():
    response = requests.get(local_host + "/relatorio_clientes_mais_reservas")

    if response.status_code == 200:
        relatorio = response.json()
        print("\n--- Relatório de Clientes com Mais Reservas ---")
        for cliente in relatorio:
            print("Nome do Cliente:", cliente["nome_cliente"])
            print("CPF do Cliente:", cliente["cpf_cliente"])
            print("Número de Reservas:", cliente["numero_reservas"])
            print("#####################################")
        return "Relatório gerado com sucesso!"
    elif response.status_code == 404:
        return response.json().get("message", "Nenhum cliente encontrado com reservas.")
    else:
        return response.json().get("message", "Erro ao gerar relatório de clientes com mais reservas.")

def get_available_veiculos_cli(start_date=None, end_date=None):
    print("\n--- Verificar Veículos Disponíveis ---")
    
    if start_date is None:
        start_date = input("Data de início da reserva (YYYY-MM-DD): ")
    if end_date is None:
        end_date = input("Data de fim da reserva (YYYY-MM-DD): ")

    params = {"start_date": start_date, "end_date": end_date}
    response = requests.get(local_host + "/get_available_veiculos", params=params)

    if response.status_code == 200:
        veiculos = response.json()
        print("\nVeículos Disponíveis para o período:")
        for veiculo in veiculos:
            print("Placa:", veiculo["placa"])
            print("Marca:", veiculo["marca"])
            print("Modelo:", veiculo["modelo"])
            print("Tipo de Combustível:", veiculo["tipo_combustivel"])
            print("Valor:", veiculo["valor"])
            print("Ar Condicionado:", "Sim" if veiculo["ar_condicionado"] else "Não")
            print("#####################################")
        return veiculos
    elif response.status_code == 404:
        print(response.json().get("message", "Nenhum veículo disponível para o período selecionado."))
        return []
    else:
        print(response.json().get("message", "Erro ao listar veículos disponíveis."))
        return []

def fazer_reserva():
    
    clientes = get_all_clientes()
    if not clientes:
        return "Não foi possível listar clientes para a reserva."

    while True:
        try:
            escolha_cliente = int(input("Selecione o número do cliente: "))
            if 1 <= escolha_cliente <= len(clientes):
                cpf_cliente = clientes[escolha_cliente - 1]['cpf']
                break
            else:
                print("Seleção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    funcionarios = get_all_funcionarios()
    if not funcionarios:
        return "Não foi possível listar funcionários para a reserva."

    while True:
        try:
            escolha_funcionario = int(input("Selecione o número do funcionário: "))
            if 1 <= escolha_funcionario <= len(funcionarios):
                cpf_funcionario = funcionarios[escolha_funcionario - 1]['cpf']
                break
            else:
                print("Seleção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    dt_reserva = input("Data inicio da reserva (no formato YYYY-MM-DD): ")
    dias = input("Quantidade de dias:")
    
    # Calcular a data de devolução para listar veículos disponíveis
    # (A validação de data e conversão para objeto datetime já é feita na API)
    # Mas precisamos de uma data de fim para a requisição de veículos disponíveis
    try:
        dt_reserva_obj = datetime.fromisoformat(dt_reserva)
        dt_devolucao_obj = dt_reserva_obj + timedelta(days=int(dias))
        dt_devolucao_str = dt_devolucao_obj.isoformat()
    except ValueError:
        return "Erro: Formato de data ou dias inválido. Use YYYY-MM-DD para a data."
    except Exception as e:
        return f"Erro inesperado ao calcular data de devolução: {e}"

    available_veiculos = get_available_veiculos_cli(start_date=dt_reserva, end_date=dt_devolucao_str)
    if not available_veiculos:
        return "Não foi possível realizar a reserva, pois não há veículos disponíveis para o período."

    while True:
        try:
            print("\n--- Veículos Disponíveis ---")
            for i, veiculo in enumerate(available_veiculos):
                print(f"{i+1}. Placa: {veiculo['placa']}, Modelo: {veiculo['modelo']}, Marca: {veiculo['marca']}, Valor: {veiculo['valor']}")
            print("---------------------------")
            
            escolha_veiculo = int(input("Selecione o número do veículo para reservar: "))
            if 1 <= escolha_veiculo <= len(available_veiculos):
                placa_veiculo = available_veiculos[escolha_veiculo - 1]['placa']
                break
            else:
                print("Seleção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    # Obter o valor do veículo selecionado
    valor_veiculo_selecionado = 0
    for veiculo in available_veiculos:
        if veiculo['placa'] == placa_veiculo:
            valor_veiculo_selecionado = veiculo['valor']
            break

    # Calcular o valor da reserva localmente
    valor_reserva_calculado = calcular_valor_reserva_local(valor_veiculo_selecionado, dias)
    print(f"\nO valor estimado da reserva é: R$ {valor_reserva_calculado:.2f}")

    confirmacao = input("Deseja confirmar a reserva? (s/n): ").lower()
    if confirmacao != 's':
        return "Reserva cancelada pelo usuário."

    status = input("Status da reserva (padrão: Ativa): ") or "Ativa"

    reserva_data = { 
            "cpf": cpf_cliente,
            "cpf_funcionario": cpf_funcionario,
            "dias": dias,
            "dt_reserva": dt_reserva,
            "placa_veiculo": placa_veiculo, # Agora passamos a placa do veículo
            "status": status
            }

    response = requests.post(local_host + "/fazer_reserva", json=reserva_data)

    if response.status_code == 200:
        valor = response.json()  # Extracting the value from the JSON response
        print("Valor da reserva:", valor)
        return "Reserva realizada com sucesso!"
    elif response.status_code == 404:
        return response.json().get("message", "Cliente, funcionário ou veículo não encontrado.")
    elif response.status_code == 409:
        return response.json().get("message", "Veículo já reservado para o período selecionado.")
    else:
        return response.json().get("message", "Erro ao realizar a reserva.")

