from menu import *
from operations import *

sair = True

while (sair):
    menu_inicial = Menu(
            #sair
            "Sair",
            
            #clientes
            "Adicionar cliente",
            "Listar clientes",
            "Alterar endereço de cliente",

            #funcionarios 
            "Adicionar funcionario",
            "Listar funcionarios",
            "Alterar endereço de funcionario",
            "Demitir funcionario",
            "Promover funcionario", 

            #tipo de veículos
            "Adicionar tipo de veículo",
            "Listar tipos de veículos",
            
            #veículos 
            "Adicionar veículo",
            "Listar veículos",
            "Tirar Veículo frota",
            
            #reservas
            "Reservar veiculo",
            "Ver reservas feitas"
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
        case 3:
            get_all_clientes()
            print(alterar_endereco_cliente())
        case 4:
            print(cadastrar_funcionario())
        case 5:
            print(get_all_funcionarios())
        case 6:
            print(alterar_endereco_funcionario())
        case 7:
            print(demitir_funcionario())
        case 8:
            print(promover_funcionario())
        case 9:
            print(cadastrar_tipo_veiculo())
        case 10:
            print(get_all_tipo_veiculos())
        case 11:
            print(adicionar_veiculo())
        case 12:
            print(get_all_veiculos())
        case 13:
            print(tirar_veiculo_frota())
        case 14:
            print(fazer_reserva())
        case 15:
            print(get_all_reservas())

