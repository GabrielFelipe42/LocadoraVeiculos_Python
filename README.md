# API Locadora de Veículos

## Descrição
Sistema de locadora de veículos com API REST e interface CLI, baseado em modelo relacional atualizado com entidade "Tipo de Veículos".

## Estrutura do Banco de Dados
- **Tipo de Veículos**: Modelo, tipo de combustível, capacidade de passageiros
- **Veículos**: Placa, cor, marca, quilometragem, valor, ar condicionado, tipo (FK)
- **Clientes**: Código, nome, CPF, endereço, CNH, data nascimento
- **Funcionários**: ID, nome, CPF, cargo, endereço, salário, data nascimento, ativo
- **Reservas**: Código, cliente (FK), funcionário (FK), tipo de veículo (FK), valor, datas, status

## Funcionalidades
- Gestão de tipos de veículos
- Gestão de veículos
- Gestão de clientes
- Gestão de funcionários
- Sistema de reservas por tipo de veículo
- Interface CLI interativa

## Set up
Primeiro, instale o packet manager do python com o comando
```bash
$ sudo apt install python3-pip
```
Depois instale as dependencias do projeto da seguinte forma
```bash
$ pip install -r requirements.txt
```
Após instalar as dependencias é necessário matar qualquer processo que esteja presente na porta 8080 do seu computador para poder rodar o servidor localmente
```bash
$ sudo lsof -i :8080
```
Caso após rodar o ```lsof -i :8080``` não listar nenhuma porta, signifca que nenhum processo está ocupando essa porta. 

Caso contrário, pegar o numero do processo e executar o comando abaixo com o número do processo. 
```bash
$ sudo kill -9 998244353
```
ou caso esteja em um ambiente windows
```bash
$ netstat -ano | findstr :8080
$ taskkill /PID 998244353 /F
```

então execute ```python3 app.py``` para rodar o servidor localmente e ter acesso às rotas http no seu navegador no endereço ```http://127.0.0.1:8080```
depois disso, em outro terminal, execute o comando ```python3 main.py```

## Rotas da API
- `/get_all_tipo_veiculos` - Listar tipos de veículos
- `/cadastrar_tipo_veiculo` - Cadastrar tipo de veículo
- `/get_all_veiculos` - Listar veículos
- `/adicionar_veiculo` - Adicionar veículo
- `/get_all_clientes` - Listar clientes
- `/cadastrar_cliente` - Cadastrar cliente
- `/get_all_funcionarios` - Listar funcionários
- `/cadastrar_funcionario` - Cadastrar funcionário
- `/fazer_reserva` - Fazer reserva
- `/get_all_reservas` - Listar reservas
