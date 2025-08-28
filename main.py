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