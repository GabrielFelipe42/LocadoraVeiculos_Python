from menu import *
from operations import *

sair = True

while (sair):
    menu_inicial = Menu(
            #sair
            "Sair",
            
            #clientes
            "Adicionar cliente",
            "Alterar endereço de cliente",
            "Listar clientes",

            #funcionarios 
            "Adicionar funcionario",
            "Alterar endereço de funcionario",
            "Demitir funcionario",
            "Promover funcionario", 
            "Listar funcionarios",

            #tipo de veículos
            "Adicionar tipo de veículo",
            "Listar tipos de veículos",
            
            #veículos 
            "Adicionar veículo",
            "Tirar Veículo frota",
            "Listar veículos",
            "Listar veículos disponíveis para reserva",
            
            #reservas
            "Reservar veiculo",
            "Listar todas as reservas",
            "Listar reservas por cliente",

            #relatórios
            "Listar veículos mais alugados",
            "Listar faturamento por período",
            "Listar clientes com mais reservas"
            )

    menu_inicial.interface()
    escolha = menu_inicial.input()
    
    match escolha:
        case 0:
            print("Saindo do aplicativo")
            sair = False;
        case 1:
            print(cadastrar_cliente())
        case 2:
            get_all_clientes()
            print(alterar_endereco_cliente())
        case 3:
            get_all_clientes()
        case 4:
            print(cadastrar_funcionario())
        case 5:
            print(alterar_endereco_funcionario())
        case 6:
            print(demitir_funcionario())
        case 7:
            print(promover_funcionario())
        case 8:
            get_all_funcionarios()
        case 9:
            print(cadastrar_tipo_veiculo())
        case 10:
            print(get_all_tipo_veiculos())
        case 11:
            print(adicionar_veiculo())
        case 12:
            print(tirar_veiculo_frota())
        case 13:
            print(get_all_veiculos())
        case 14:
            get_available_veiculos_cli()
        case 15:
            print(fazer_reserva())
        case 16:
            print(get_all_reservas())
        case 17:
            print(get_reservas_by_cliente_cli())
        case 18:
            print(relatorio_veiculos_mais_alugados_cli())
        case 19:
            print(relatorio_faturamento_por_periodo_cli())
        case 20:
            print(relatorio_clientes_mais_reservas_cli())

